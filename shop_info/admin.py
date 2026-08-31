from django.contrib import admin

from .models import ContactMessage, ShopInfo


@admin.register(ShopInfo)
class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ("store_name", "phone_number", "updated_at")
    fieldsets = (
        (None, {"fields": ("store_name", "address", "map_embed_url")}),
        ("Contact", {"fields": ("phone_number", "whatsapp_number", "email")}),
        ("Opening hours and story", {"fields": ("opening_hours", "about_text")}),
    )

    def has_add_permission(self, request):
        return not ShopInfo.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_or_email", "submitted_at", "is_read")
    list_filter = ("is_read", "submitted_at")
    search_fields = ("name", "phone_or_email", "message")
    readonly_fields = ("name", "phone_or_email", "message", "submitted_at")
    fields = ("name", "phone_or_email", "message", "submitted_at", "is_read")