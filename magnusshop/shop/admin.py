from django.contrib import admin
from shop.models import *


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                try:
                    product = Product.objects.get(pk=obj_id)
                    kwargs["queryset"] = ProductAttribute.objects.filter(product_type=product.product_type)
                except Product.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'upc', 'product_type', 'title', 
        'is_active', 'category', 'brand',
        'modify_time'
    )
    list_display_links = ('title',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('upc', 'title', 'category__name', 'brand__name')
    actions = ('active_all',)
    inlines = (ProductAttributeValueInline, ProductImageInline)
    
    def active_all(self, request, queryset):
        pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','parent')


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [ProductAttributeInline]


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')


admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
