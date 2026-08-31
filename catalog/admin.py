from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .forms import CategoryAdminForm, ItemImageAdminForm
from .models import Category, Item, ItemImage


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    form = ItemImageAdminForm
    extra = 1
    fields = ("image_preview", "image", "alt_text", "is_primary", "display_order")
    readonly_fields = ("image_preview",)
    verbose_name_plural = "Photos"

    @admin.display(description="Current photo")
    def image_preview(self, obj):
        if not obj.pk or not obj.image:
            return "No photo uploaded"
        return format_html(
            '<img src="{}" alt="{}" style="width: 96px; height: 72px; object-fit: cover; border-radius: 6px;">',
            obj.image.url,
            obj.alt_text or obj.item.name,
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ("image_thumbnail", "name", "quick_add_item", "is_active", "display_order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Basic information", {
            "description": "Set the category name and the image customers will see in the shop.",
            "fields": ("name", "slug", "description", "image", "image_preview"),
        }),
        ("Visibility and ordering", {
            "description": "Control whether this category appears publicly and where it is listed.",
            "fields": ("is_active", "display_order"),
        }),
    )

    @admin.display(description="Photo")
    def image_thumbnail(self, obj):
        if not obj.image:
            return "-"
        return format_html(
            '<img src="{}" alt="{}" style="width: 56px; height: 42px; object-fit: cover; border-radius: 5px;">',
            obj.image.url,
            obj.name,
        )

    @admin.display(description="Current photo")
    def image_preview(self, obj):
        if not obj.pk or not obj.image:
            return "No photo uploaded"
        return format_html(
            '<img src="{}" alt="{}" style="max-width: 240px; max-height: 180px; object-fit: cover; border-radius: 8px;">',
            obj.image.url,
            obj.name,
        )

    @admin.display(description="Quick add")
    def quick_add_item(self, obj):
        if not obj.is_active:
            return format_html('<span class="quiet">Activate category first</span>')
        url = reverse("admin:catalog_item_add")
        return format_html(
            '<a class="button" href="{}?category={}" title="Add an item to {}">+ Add item</a>',
            url,
            obj.pk,
            obj.name,
        )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("primary_thumbnail", "name", "category", "price", "discount", "stock_status", "is_featured", "is_active")
    list_filter = ("category", "stock_status", "is_featured", "is_active")
    search_fields = ("name", "description", "material", "color_variants")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("category",)
    inlines = (ItemImageInline,)
    fieldsets = (
        ("Basic information", {
            "description": "Name the piece and place it in the correct category.",
            "fields": (
                "category", "name", "description",
            ),
        }),
        ("Pricing and availability", {
            "description": "Set the regular price, optional discount, and current availability.",
            "fields": ("price", "discount", "stock_status"),
        }),
        ("Product specifications", {
            "description": "Add the customer-facing warranty and dimensions.",
            "fields": ("warranty_info", "dimensions"),
        }),
        ("Additional details", {
            "description": "Optional catalog details used for richer product information.",
            "classes": ("collapse",),
            "fields": ("slug", "material", "color_variants", "delivery_info", "is_featured", "is_active"),
        }),
    )

    @admin.display(description="Photo")
    def primary_thumbnail(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if not image:
            return "-"
        return format_html(
            '<img src="{}" alt="{}" style="width: 56px; height: 42px; object-fit: cover; border-radius: 5px;">',
            image.image.url,
            image.alt_text or obj.name,
        )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        category_id = request.GET.get("category")
        if category_id and Category.objects.filter(pk=category_id, is_active=True).exists():
            initial["category"] = category_id
        return initial

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        category_id = request.GET.get("category")
        if obj is None and category_id and Category.objects.filter(pk=category_id, is_active=True).exists():
            form.base_fields["category"].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        category_id = request.GET.get("category")
        if not change and category_id:
            category = Category.objects.filter(pk=category_id, is_active=True).first()
            if category:
                obj.category = category
        super().save_model(request, obj, form, change)


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    form = ItemImageAdminForm
    list_display = ("item", "is_primary", "display_order", "alt_text")
    list_filter = ("is_primary",)
    search_fields = ("item__name", "alt_text")