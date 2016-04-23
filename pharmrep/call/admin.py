from django.contrib import admin

from call.models import Call


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['rep', 'customer', 'contact', 'products_detailed',
                    'order_value', 'call_type', 'call_date']
