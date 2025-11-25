from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for YadaList.

    Starting empty - extends AbstractUser without modifications.
    This gives us flexibility to add fields later without painful migrations.

    Potential future fields:
    - business_name
    - subscription_tier
    - phone
    - timezone
    - onboarding_completed
    """

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email or self.username
