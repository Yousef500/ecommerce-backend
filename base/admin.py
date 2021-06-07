from django.contrib import admin

from .models import Product, ShippingAddress, OrderItem, Order, Review

admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)

# Register your models here.
