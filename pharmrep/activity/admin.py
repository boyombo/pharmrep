from django.contrib import admin

from activity import models as activity


@admin.register(activity.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['rep', 'customer', 'contact', 'products_detailed',
                    'order_value', 'call_type', 'call_date']


@admin.register(activity.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['rep', 'activity', 'recorded_date']
