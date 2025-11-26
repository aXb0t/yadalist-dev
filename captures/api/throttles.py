"""
Custom throttle classes for the captures API.
"""
from rest_framework.throttling import UserRateThrottle


class ImageUploadThrottle(UserRateThrottle):
    """
    Throttle class for image upload endpoints.
    Uses the 'upload' scope from settings.

    Production: 100/hour
    Development: 1000/hour
    Testing: disabled
    """
    scope = 'upload'
