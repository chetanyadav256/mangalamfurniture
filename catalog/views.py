from django.views.generic import TemplateView


class CategoryIndexView(TemplateView):
    template_name = "catalog/category_index.html"