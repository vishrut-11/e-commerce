from django.contrib import admin
from app.models import (Customer, Product, OrderPlaced, Cart)
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(OrderPlaced)
# admin.site.register(Cart)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","name","locality","city","zipcode","state"]

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('app/js/tinyinject.js',)

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["id","title","selling_price","discounted_price","description","brand","category","product_image"]

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ["id","user","product","quantity"]

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ["id","user", "customer_info", "product","quantity","ordered_date","status",]

# @admin.register(Product)
    def  customer_info(self,obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a herf="{}">{}</a>', link, obj.customer.name)
