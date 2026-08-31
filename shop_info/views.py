from django.views.generic import TemplateView

from .models import ShopInfo


class AboutView(TemplateView):
    template_name = "shop_info/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_info"] = ShopInfo.objects.first()
        return context
