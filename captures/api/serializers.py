"""
Serializers for the captures API.
"""
from rest_framework import serializers
from captures.models import CapturedItem, CapturedImage


class CapturedItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CapturedItem.

    For POST: Creates empty capture, auto-sets owner from request.user
    Returns: id, short_uuid, created_at
    """

    class Meta:
        model = CapturedItem
        fields = ['id', 'short_uuid', 'created_at', 'voice_transcript', 'is_complete']
        read_only_fields = ['id', 'short_uuid', 'created_at', 'owner']
