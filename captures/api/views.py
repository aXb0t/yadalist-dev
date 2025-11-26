"""
API views for the captures app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from captures.models import CapturedItem
from .serializers import CapturedItemSerializer


class CapturedItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CapturedItem.

    - POST creates an empty capture with owner=request.user
    - GET /{short_uuid}/ returns capture with nested images
    - PATCH /{short_uuid}/ updates voice_transcript
    - DELETE /{short_uuid}/ deletes capture (cascades to images)
    - Returns user's own captures only (via queryset filtering)
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
