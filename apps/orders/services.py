from django.db import transaction
from .models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(user, cart, address):

    cart_items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=user,
        total_amount=total,
        address=address
    )

    order_items = [
        OrderItem(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
        for item in cart_items
    ]
    OrderItem.objects.bulk_create(order_items)

    cart.items.all().delete()

    return order
