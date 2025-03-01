from django.contrib import admin
from account.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_phone', 'province', 'city', 'zipcode')

    def user(self, obj):
        return obj.profile.user.username if obj.profile and obj.profile.user else 'بدون کاربر'
    user.short_description = 'کاربر'

    def profile_phone(self, obj):
        return obj.profile.phone_number if obj.profile else 'بدون پروفایل'
    profile_phone.short_description = 'شماره تلفن پروفایل'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)