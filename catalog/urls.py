from django.urls import path

from .views import CategoryIndexView, CategoryListView, ItemDetailView


app_name = "catalog"
urlpatterns = [
	path("", CategoryIndexView.as_view(), name="category-index"),
	path("<slug:category_slug>/", CategoryListView.as_view(), name="category-list"),
	path("<slug:category_slug>/<slug:item_slug>/", ItemDetailView.as_view(), name="item-detail"),
]