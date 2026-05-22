from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.products.models import Product


class Cart(TimeStampedModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        db_table = "cart"

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(TimeStampedModel):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
