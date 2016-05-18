from django.contrib import admin

from activity import models as activity


@admin.register(activity.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ['rep', 'customer', 'contact', 'position',
                    'call_type', 'call_date', 'next_meeting']
    list_filter = ['call_type']
    search_fields = ['rep__name']


@admin.register(activity.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['rep', 'product', 'competing_company',
                    'competing_product', 'recorded_date']
    search_fields = ['rep__name']


@admin.register(activity.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['rep', 'name', 'phone', 'address', 'added_date']
    search_fields = ['rep__name']


@admin.register(activity.MarketNeed, activity.Conclusion)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['rep', 'text', 'recorded_date']
    search_fields = ['rep__name']


@admin.register(activity.Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['rep', 'places', 'recorded_date']
    search_fields = ['rep__name']


@admin.register(activity.Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ['rep', 'start_date', 'end_date', 'outstanding', 'report']
    search_fields = ['rep__name']
