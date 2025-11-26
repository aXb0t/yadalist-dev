"""
Central API router for all app APIs.

Each app owns its own API in app/api/urls.py.
This router aggregates them under /api/.
"""
from django.urls import path, include

urlpatterns = [
    path("captures/", include("captures.api.urls")),
    # Future APIs will be added here:
    # path("items/", include("items.api.urls")),
    # path("accounts/", include("accounts.api.urls")),
]
