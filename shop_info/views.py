from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "shop_info/about.html"


class ContactView(TemplateView):
    template_name = "shop_info/contact.html"