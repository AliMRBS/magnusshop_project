from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from finance.models import Payment
import datetime

@receiver(post_save, sender=Order)
def update_last_status(sender, instance, created, **kwargs):
    if not created: 
        old_status = Order.objects.get(id=instance.pk).status
        if old_status != instance.status:
            instance.last_update = datetime.datetime.now()
            instance.save()


