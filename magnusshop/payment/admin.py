from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'user', 'quantity', 'unit_price', 'total_price')
    search_fields = ('order__id', 'product__title', 'user__username')
    list_filter = ('product', 'user')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('profile', 'full_name', 'shipping_address', 'total_amount', 'date_ordered', 'status', 'last_update')
    readonly_fields = ('date_ordered', 'last_update')
    search_fields = ('zipcode', 'status')
    list_filter = ('status', 'date_ordered')
    ordering = ('-date_ordered',)
    inlines = [OrderItemInline]


admin.site.register(OrderItem, OrderItemAdmin)