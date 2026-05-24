from django.contrib import admin, messages
from .models import OrderItem, Order, OrderStatus
from django.db import transaction
from django.utils.translation import gettext_lazy as _


@admin.action(description=_("Mark selected orders as shipped (only paid)"))
def mark_paid_orders_as_shipped(model_admin, request, queryset):
    shipped = 0
    skipped = 0

    with transaction.atomic():
        for order in queryset.select_for_update():
            if order.status != OrderStatus.PAID:
                skipped += 1
                continue
            order.status = OrderStatus.SHIPPED
            order.save(update_fields=["status"])
            shipped += 1
    if shipped:
        model_admin.message_user(request, _(f"{shipped} order(s) shipped."), messages.SUCCESS)
    if skipped:
        model_admin.message_user(request, _(f"{skipped} order(s) skipped (not paid)."), messages.WARNING)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'price', 'quantity')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_select_related = ('user',)
    inlines = [OrderItemInline]
    actions = [mark_paid_orders_as_shipped]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')
