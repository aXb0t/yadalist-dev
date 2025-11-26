"""
URL routing for captures API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import CapturedItemViewSet, CapturedImageViewSet

# Main router for captures
router = DefaultRouter()
router.register(r'items', CapturedItemViewSet, basename='captureditem')

# Nested router for images within captures
# URL pattern: /api/captures/items/{capture_short_uuid}/images/{image_short_uuid}/
images_router = routers.NestedSimpleRouter(router, r'items', lookup='capture')
images_router.register(r'images', CapturedImageViewSet, basename='captureditem-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(images_router.urls)),
]
