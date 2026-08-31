from django.urls import path

from .views import CategoryIndexView


app_name = "catalog"
urlpatterns = [path("", CategoryIndexView.as_view(), name="category-index")]