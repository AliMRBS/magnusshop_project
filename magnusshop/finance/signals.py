from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.models import Payment
from payment.models import Order

@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    if instance.is_paid:  
        try:
            order = Order.objects.get(payment=instance)
            order.status = 'paid'
            order.save()
        except Order.DoesNotExist:
            pass  