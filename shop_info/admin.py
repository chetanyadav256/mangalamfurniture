from django.contrib import admin

from .models import ContactMessage, ShopInfo


@admin.register(ShopInfo)
class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ("store_name", "phone_number", "updated_at")
    fieldsets = (
        ("Store profile", {
            "description": "Keep the public store identity and location details up to date.",
            "fields": ("store_name", "address", "map_embed_url"),
        }),
        ("Contact details", {
            "description": "These details power the Call, WhatsApp, and email contact options.",
            "fields": ("phone_number", "whatsapp_number", "email"),
        }),
        ("Opening hours and story", {
            "description": "Use plain text by day for opening hours and a short store introduction.",
            "fields": ("opening_hours", "about_text"),
        }),
    )

    def has_add_permission(self, request):
        return not ShopInfo.objects.exists()


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_or_email", "submitted_at", "is_read")
    list_filter = ("is_read", "submitted_at")
    search_fields = ("name", "phone_or_email", "message")
    readonly_fields = ("name", "phone_or_email", "message", "submitted_at")
    fieldsets = (
        ("Customer inquiry", {
            "description": "Review the customer message and mark it read after follow-up.",
            "fields": ("name", "phone_or_email", "message"),
        }),
        ("Follow-up", {
            "fields": ("submitted_at", "is_read"),
        }),
    )