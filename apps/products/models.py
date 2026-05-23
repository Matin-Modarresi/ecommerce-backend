from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel
from .managers import ActiveProductManager


class Category(TimeStampedModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=100)

    slug = models.SlugField(
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    description = models.TextField(blank=True)

    price = models.PositiveBigIntegerField()

    sku = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    stock = models.PositiveIntegerField(default=0)

    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True
    )

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveProductManager()

    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    review_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")

    alt_text = models.CharField(max_length=255, blank=True)

    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_primary"]

    def __str__(self):
        return f"Image for {self.product.name}"
