from django.core.exceptions import ValidationError
from django.db import models


class ShopInfo(models.Model):
    store_name = models.CharField(max_length=150)
    address = models.TextField()
    map_embed_url = models.URLField()
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    opening_hours = models.JSONField(default=dict)
    about_text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.pk is None and ShopInfo.objects.exists():
            raise ValidationError("Only one shop information record is allowed.")

    def __str__(self):
        return self.store_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone_or_email = models.CharField(max_length=150)
    message = models.TextField(max_length=2000)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return "{} - {}".format(self.name, self.phone_or_email)