from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import ContactMessageForm
from .models import ShopInfo


class AboutView(TemplateView):
    template_name = "shop_info/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_info"] = ShopInfo.objects.first()
        return context


class ContactView(TemplateView):
    template_name = "shop_info/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_info"] = ShopInfo.objects.first()
        context["form"] = getattr(self, "form", ContactMessageForm())
        return context

    def post(self, request, *args, **kwargs):
        self.form = ContactMessageForm(request.POST)
        if self.form.is_valid():
            if not self.form.cleaned_data.get("website"):
                self.form.save()
                messages.success(request, "Your message has been received. We will be in touch shortly.")
            return redirect("shop_info:contact")
        return self.render_to_response(self.get_context_data(**kwargs))