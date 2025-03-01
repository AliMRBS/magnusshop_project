from django.db import models
from shop.models import Product
from account.models import Profile  
from django.contrib.auth.models import User
from finance.models import Payment

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    ]

    profile = models.ForeignKey(Profile, related_name='orders', on_delete=models.CASCADE)  # ارتباط با مدل Profile
    full_name = models.CharField(max_length=250)
    shipping_address = models.CharField(max_length=600) 
    zipcode = models.CharField(max_length=25)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, null=True)

    payment =  models.ForeignKey(Payment, related_name='orders', on_delete=models.PROTECT, null=True)


    def __str__(self):
        return f"Order {self.id} - {self.profile.first_name} {self.profile.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    unit_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="قیمت واحد")
    total_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="مجموع قیمت")

    def __str__(self):
        return f"OrderItem ID: {str(self.id)} - توسط: {self.user}"
