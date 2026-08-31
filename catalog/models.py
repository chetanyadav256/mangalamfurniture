from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    STOCK_STATUS_CHOICES = [
        (IN_STOCK, "In stock"),
        (OUT_OF_STOCK, "Out of stock"),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="discount (INR)",
    )
    description = models.TextField()
    material = models.CharField(max_length=150, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    color_variants = models.CharField(max_length=255, blank=True)
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default=IN_STOCK)
    warranty_info = models.CharField(max_length=255, blank=True)
    delivery_info = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        return max(self.price - (self.discount or 0), 0)


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        upload_to="items/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    alt_text = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def save(self, *args, **kwargs):
        if self.is_primary:
            ItemImage.objects.filter(item=self.item, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
        if not ItemImage.objects.filter(item=self.item, is_primary=True).exists():
            ItemImage.objects.filter(pk=self.pk).update(is_primary=True)

    def delete(self, *args, **kwargs):
        was_primary = self.is_primary
        item = self.item
        super().delete(*args, **kwargs)
        if was_primary:
            replacement = item.images.order_by("display_order", "id").first()
            if replacement:
                replacement.is_primary = True
                replacement.save(update_fields=["is_primary"])

    def __str__(self):
        return self.alt_text or "Image for {}".format(self.item.name)