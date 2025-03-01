from django.db import models
from django.contrib.auth.models import User
from magnusplus.models import Package
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from .utils import send_otp_email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='profile')
    phone_number = models.CharField(max_length=25, blank=False, unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=40, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    magnusplus_sub = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name='profiles', verbose_name='Magnus Plus Subscription')
    magnusplus_start_date = models.DateField(null=True, blank=True) 
    
    def generate_otp(self):
        """ تولید کد OTP و تنظیم زمان انقضا """
        import random
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expiration = now() + timedelta(minutes=2)  
        self.save()

    def resend_otp(self):
        """ ارسال مجدد کد در صورت انقضا """
        self.generate_otp()
        send_otp_email(self.email, self.otp_code)


    def is_otp_valid(self, entered_otp):
        """ بررسی صحت کد وارد شده """
        return self.otp_code == entered_otp and self.otp_expiration > now()
    
    def get_magnusplus_end_date(self):
        if self.magnusplus_sub and self.magnusplus_start_date:
            return self.magnusplus_start_date + timezone.timedelta(days=self.magnusplus_sub.days)
        return None

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
   

class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='adresses')
    address = models.CharField(max_length=250, blank=True)
    province = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=25, blank=True)
    house_number = models.CharField(max_length=4, blank=True)
    unit_number = models.CharField(max_length=4, blank=True)
    zipcode = models.CharField(max_length=25, blank=True)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.profile.user.username if self.profile else 'بدون پروفایل'} - {self.city}"
