from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from product.models import Product, Rep, Customer, Sale, Payment, Invoice,\
    BatchSize, PriceTemplate, ProductPriceTemplate


class ProductPriceTemplateAdmin(admin.TabularInline):
    model = ProductPriceTemplate


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate']
    inlines = [
        ProductPriceTemplateAdmin
    ]


@admin.register(BatchSize)
class BatchSizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']


@admin.register(Rep, Customer, PriceTemplate)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['rep', 'customer', 'invoice_no',
                    'invoice_date', 'sales_type', 'recorded_date']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['product', 'batch_size', 'quantity',
                    'invoice', 'recorded_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'rep', 'customer', 'receipt_no',
                    'payment_date', 'receipt_date', 'recorded_date', 'balance']


class RepInline(admin.StackedInline):
    model = Rep
    can_delete = False
    verbose_name_plural = 'Representative'


class UserAdmin(BaseUserAdmin):
    inlines = [RepInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
