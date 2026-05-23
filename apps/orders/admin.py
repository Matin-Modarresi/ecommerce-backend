from django.contrib import admin
from .models import OrderItem, Order


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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_realted('items')
