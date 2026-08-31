from django.views.generic import TemplateView

from catalog.models import Category, Item


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_items"] = Item.objects.filter(
            is_active=True, is_featured=True
        ).prefetch_related("images")[:8]
        context["categories"] = Category.objects.filter(is_active=True)[:6]
        return context