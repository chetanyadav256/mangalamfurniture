from django.contrib import admin

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
    list_display = ("name", "is_active", "display_order", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_status", "is_featured", "is_active")
    list_filter = ("category", "stock_status", "is_featured", "is_active")
    search_fields = ("name", "description", "material", "color_variants")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("category",)
    inlines = (ItemImageInline,)


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    form = ItemImageAdminForm
    list_display = ("item", "is_primary", "display_order", "alt_text")
    list_filter = ("is_primary",)
    search_fields = ("item__name", "alt_text")