from catalog.models import Category
from shop_info.models import ShopInfo


def site_context(request):
    return {
        "site_name": "Manglam Furniture",
        "nav_categories": Category.objects.filter(is_active=True),
        "shop_info": ShopInfo.objects.first(),
    }