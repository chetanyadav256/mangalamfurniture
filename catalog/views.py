from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Item


class CategoryIndexView(ListView):
    template_name = "catalog/category_index.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class CategoryListView(ListView):
    template_name = "catalog/category_list.html"
    context_object_name = "items"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["category_slug"], is_active=True)
        return Item.objects.filter(category=self.category, is_active=True).prefetch_related("images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ItemDetailView(DetailView):
    template_name = "catalog/item_detail.html"
    context_object_name = "item"
    slug_url_kwarg = "item_slug"

    def get_queryset(self):
        return Item.objects.filter(
            category__slug=self.kwargs["category_slug"],
            category__is_active=True,
            is_active=True,
        ).prefetch_related("images")