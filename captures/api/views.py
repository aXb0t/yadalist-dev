"""
API views for the captures app.
"""
from django.db import transaction
from django.db.models import Max
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from captures.models import CapturedItem, CapturedImage
from .serializers import (
    CapturedItemSerializer,
    CapturedImageSerializer,
    ImageUploadSerializer,
    ImageReorderSerializer,
)


class CapturedItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CapturedItem.

    - POST creates an empty capture with owner=request.user
    - GET /{short_uuid}/ returns capture with nested images
    - PATCH /{short_uuid}/ updates voice_transcript
    - DELETE /{short_uuid}/ deletes capture (cascades to images)
    - Returns user's own captures only (via queryset filtering)

    Custom actions:
    - POST /{short_uuid}/upload_images/ - Upload one or more images
    - PATCH /{short_uuid}/reorder/ - Reorder images
    - POST /{short_uuid}/complete/ - Mark capture as complete
    """
    serializer_class = CapturedItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'short_uuid'

    def get_queryset(self):
        """Return only captures owned by the current user."""
        return CapturedItem.objects.for_user(self.request.user).prefetch_related('images')

    def perform_create(self, serializer):
        """Set owner to current user on create."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload_images')
    def upload_images(self, request, short_uuid=None):
        """
        Upload one or more images to a capture.

        Enforces 20-image limit per capture.
        Auto-assigns order by appending to the end.
        Returns array of created images.
        """
        capture = self.get_object()

        # Check current image count
        current_count = capture.images.count()

        # Validate upload using serializer
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images_to_upload = serializer.validated_data['images']
        new_count = len(images_to_upload)

        # Enforce 20-image limit
        if current_count + new_count > 20:
            return Response(
                {
                    'error': f'Cannot upload {new_count} images. Capture already has {current_count} images. Maximum is 20.',
                    'current_count': current_count,
                    'max_allowed': 20
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get current max order
        max_order_result = capture.images.aggregate(max=Max('order'))
        max_order = max_order_result['max'] if max_order_result['max'] is not None else -1

        # Create images with auto-incrementing order
        created_images = []
        for i, image_file in enumerate(images_to_upload):
            image = CapturedImage.objects.create(
                owner=request.user,
                captured_item=capture,
                image=image_file,
                order=max_order + 1 + i
            )
            created_images.append(image)

        # Serialize and return created images
        response_serializer = CapturedImageSerializer(created_images, many=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def reorder(self, request, short_uuid=None):
        """
        Reorder images within a capture.

        Accepts JSON body: {"order": ["uuid1", "uuid2", "uuid3"]}
        Updates order field on each image in a transaction.
        """
        capture = self.get_object()

        # Validate input
        serializer = ImageReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ordered_uuids = serializer.validated_data['order']

        # Get all images for this capture, keyed by uuid (not id or short_uuid)
        images = {img.uuid: img for img in capture.images.all()}

        # Validate that all provided UUIDs belong to this capture
        for uuid in ordered_uuids:
            if uuid not in images:
                return Response(
                    {'error': f'Image {uuid} does not belong to this capture'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Update order in a transaction
        with transaction.atomic():
            for new_order, uuid in enumerate(ordered_uuids):
                image = images[uuid]
                image.order = new_order
                image.save(update_fields=['order'])

        return Response({'reordered': True, 'count': len(ordered_uuids)})

    @action(detail=True, methods=['post'])
    def complete(self, request, short_uuid=None):
        """
        Mark a capture as complete.

        Sets is_complete=True and returns completion status with image count.
        """
        capture = self.get_object()
        capture.is_complete = True
        capture.save(update_fields=['is_complete'])

        return Response({
            'completed': True,
            'image_count': capture.images.count()
        })


class CapturedImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CapturedImage.

    Provides deletion of individual images.
    All operations are scoped to the current user's captures.
    """
    serializer_class = CapturedImageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'short_uuid'
    http_method_names = ['delete']  # Only allow DELETE

    def get_queryset(self):
        """
        Return only images that belong to captures owned by the current user.
        Also filters by the capture's short_uuid from the URL.
        """
        capture_uuid = self.kwargs.get('capture_short_uuid')
        return CapturedImage.objects.filter(
            owner=self.request.user,
            captured_item__short_uuid=capture_uuid
        )
