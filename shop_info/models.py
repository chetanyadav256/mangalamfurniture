from django.core.exceptions import ValidationError
from django.db import models


class ShopInfo(models.Model):
    store_name = models.CharField(max_length=150, help_text="Name displayed across the website.")
    address = models.TextField(help_text="Full store address customers can use to visit.")
    map_embed_url = models.URLField(help_text="Google Maps embed URL, not a regular maps share link.")
    phone_number = models.CharField(max_length=20, help_text="Store phone number used by the Call buttons.")
    whatsapp_number = models.CharField(max_length=20, help_text="WhatsApp number with country code, digits only where possible.")
    email = models.EmailField(blank=True, help_text="Optional store email address.")
    opening_hours = models.TextField(default="{}", help_text="Enter opening hours by day, for example: Monday-Friday: 10:00 AM-8:00 PM.")
    about_text = models.TextField(blank=True, help_text="Short story or introduction for the About page.")
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.pk is None and ShopInfo.objects.exists():
            raise ValidationError("Only one shop information record is allowed.")

    def __str__(self):
        return self.store_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, help_text="Customer name.")
    phone_or_email = models.CharField(max_length=150, help_text="A phone number or email address for your reply.")
    message = models.TextField(max_length=2000, help_text="Customer inquiry, up to 2,000 characters.")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return "{} - {}".format(self.name, self.phone_or_email)