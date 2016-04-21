from django.contrib import admin

from product.models import Product, Rep, Customer, Sale, Payment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']


@admin.register(Rep, Customer)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'rep', 'customer', 'quantity',
                    'sales_date', 'recorded_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'rep', 'customer', 'receipt_no',
                    'payment_date', 'recorded_date', 'balance']
