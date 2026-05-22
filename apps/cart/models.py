from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


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

