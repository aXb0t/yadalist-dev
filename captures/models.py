from django.db import models
from core.models import OwnedModel


class CapturedItem(OwnedModel):
    """
    A capture session. Just the raw material.

    Design: Write-optimized, minimal validation.
    Goal: Save and get out of user's way in <10 seconds.
    """
    voice_transcript = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['owner', 'is_complete']),
        ]

    def __str__(self):
        preview = (self.voice_transcript[:50] + '...') if self.voice_transcript else 'Empty'
        return f"Capture {self.short_uuid}: {preview}"


class CapturedImage(OwnedModel):
    """
    Images attached to a capture.
    Independently mutable (add/remove/reorder).
    """
    captured_item = models.ForeignKey(
        CapturedItem,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='captures/%Y/%m/%d/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['captured_item', 'order']),
        ]
