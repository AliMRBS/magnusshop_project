from django.contrib import admin
from django.contrib.admin import register
from magnusplus.models import Package, PackageAttribute


class PackageAttributeInline(admin.TabularInline):
    model = PackageAttribute

@register(Package)
class PackageModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = (PackageAttributeInline,)


