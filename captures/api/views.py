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
    - Returns user's own captures only (via queryset filtering)
    """
    serializer_class = CapturedItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only captures owned by the current user."""
        return CapturedItem.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        """Set owner to current user on create."""
        serializer.save(owner=self.request.user)
