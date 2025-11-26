from django.contrib import admin
from .models import CapturedItem, CapturedImage


class CapturedImageInline(admin.TabularInline):
    model = CapturedImage
    extra = 1


@admin.register(CapturedItem)
class CapturedItemAdmin(admin.ModelAdmin):
    list_display = ['short_uuid', 'owner', 'is_complete', 'created_at']
    list_filter = ['is_complete', 'created_at']
    inlines = [CapturedImageInline]
