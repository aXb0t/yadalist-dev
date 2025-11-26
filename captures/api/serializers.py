"""
Serializers for the captures API.
"""
from rest_framework import serializers
from captures.models import CapturedItem, CapturedImage
from captures.validators import validate_image_file


class CapturedImageSerializer(serializers.ModelSerializer):
    """
    Serializer for CapturedImage (nested in CapturedItem).
    """

    class Meta:
        model = CapturedImage
        fields = ['id', 'short_uuid', 'image', 'order', 'created_at']
        read_only_fields = ['id', 'short_uuid', 'created_at']


class CapturedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CapturedItem.

    For POST: Creates empty capture, auto-sets owner from request.user
    For GET: Returns capture with nested images
    For PATCH: Updates voice_transcript
    """
    images = CapturedImageSerializer(many=True, read_only=True)

    class Meta:
        model = CapturedItem
        fields = ['id', 'short_uuid', 'created_at', 'voice_transcript', 'is_complete', 'images']
        read_only_fields = ['id', 'short_uuid', 'created_at', 'owner']


class ImageUploadSerializer(serializers.Serializer):
    """
    Serializer for uploading multiple images to a capture.
    Accepts multipart form data with 'images' field containing one or more files.

    Validation includes:
    - File size (max 10MB per image)
    - File extension (jpg, jpeg, png, gif, webp)
    - MIME type verification (magic bytes)
    - Image integrity (can be opened by Pillow)
    - Image dimensions (max 50 megapixels)
    """
    images = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            validators=[validate_image_file]
        ),
        allow_empty=False,
        max_length=20,
        help_text="Upload one or more images (max 20 per capture, max 10MB each)"
    )


class ImageReorderSerializer(serializers.Serializer):
    """
    Serializer for reordering images within a capture.
    Accepts an array of image UUIDs in the desired order.
    """
    order = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        help_text="Array of image UUIDs in desired order"
    )
