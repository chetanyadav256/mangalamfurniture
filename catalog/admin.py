from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .forms import CategoryAdminForm, ItemImageAdminForm
from .models import Category, Item, ItemImage


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    form = ItemImageAdminForm
    extra = 1
    fields = ("image", "alt_text", "is_primary", "display_order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ("name", "quick_add_item", "is_active", "display_order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")

    @admin.display(description="Quick add")
    def quick_add_item(self, obj):
        url = reverse("admin:catalog_item_add")
        return format_html(
            '<a class="button" href="{}?category={}" title="Add an item to {}">+ Add item</a>',
            url,
            obj.pk,
            obj.name,
        )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount", "stock_status", "is_featured", "is_active")
    list_filter = ("category", "stock_status", "is_featured", "is_active")
    search_fields = ("name", "description", "material", "color_variants")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("category",)
    inlines = (ItemImageInline,)
    fieldsets = (
        ("Item essentials", {
            "fields": (
                "category", "name", "price", "discount", "warranty_info",
                "dimensions", "description", "stock_status",
            ),
        }),
        ("Additional details", {
            "classes": ("collapse",),
            "fields": ("slug", "material", "color_variants", "delivery_info", "is_featured", "is_active"),
        }),
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