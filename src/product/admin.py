from django.contrib import admin
from .models import Product, Variant, ProductImage, ProductVariantPrice, ProductVariant
# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)