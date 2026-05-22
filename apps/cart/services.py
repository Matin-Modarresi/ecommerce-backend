from .models import CartItem


def add_product_to_cart(cart, product, quantity=1):

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return cart_item


def remove_product_from_cart(cart, product):

    CartItem.objects.filter(
        cart=cart,
        product=product,
    ).delete()


def update_cart_item_quantity(cart, product, quantity):

    cart_item = CartItem.objects.get(
        cart=cart,
        product=product,
    )

    cart_item.quantity = quantity
    cart_item.save()

    return cart_item

