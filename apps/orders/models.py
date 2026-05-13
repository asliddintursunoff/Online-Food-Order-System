from django.db import models
from django.utils import timezone

from apps.common.choices import OrderStatus


class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    location = models.ForeignKey("users.UserLocation", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    created_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):

        if self.status == OrderStatus.PENDING and not self.created_at:
            self.created_at = timezone.now()

        elif self.status == OrderStatus.DONE and not self.delivered_at:
            self.delivered_at = timezone.now()

        elif self.status == OrderStatus.CANCELED and not self.canceled_at:
            self.canceled_at = timezone.now()

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="order_items")

    quantity = models.IntegerField(default=1)