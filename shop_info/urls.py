from django.urls import path

from .views import AboutView


app_name = "shop_info"
urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
]