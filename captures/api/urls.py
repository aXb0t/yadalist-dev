"""
URL routing for captures API endpoints.
"""
from rest_framework.routers import DefaultRouter
from .views import CapturedItemViewSet

router = DefaultRouter()

# Register viewsets
router.register(r'items', CapturedItemViewSet, basename='captureditem')

urlpatterns = router.urls
