import uuid
import shortuuid
from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """Identity and timestamps for all models."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    short_uuid = models.CharField(max_length=22, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.short_uuid:
            self.short_uuid = shortuuid.uuid()
        super().save(*args, **kwargs)


class OwnedModelManager(models.Manager):
    """Manager that provides user-scoped queries."""
    def for_user(self, user):
        return self.filter(owner=user)


class OwnedModel(BaseModel):
    """Base for any model that belongs to a user."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    objects = OwnedModelManager()

    class Meta:
        abstract = True
