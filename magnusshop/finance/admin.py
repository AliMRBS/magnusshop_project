from django.contrib import admin
from django.contrib.admin import register
from .models import Gateway, Payment

@register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('title', 'gateway_code', 'is_enable')
    list_filter = ('is_enable', )


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'amount', 'user', 'is_paid']
    list_filter = ['is_paid']