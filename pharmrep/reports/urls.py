from django.conf.urls import url
from django.views.generic import TemplateView

from reports import views


urlpatterns = [
    url(r'balance/$', views.balance, name='report_balance'),
    url(r'performance/$', views.performance, name='report_performance'),
    #url(r'collection/$', views.collection, name='report_collection'),
    url(r'collection/$', views.CollectionListView.as_view(),
        name='report_collection'),
    url(r'saleschart/$', TemplateView.as_view(
        template_name='reports/sales_chart.html'), name='chart_sales'),
    url(r'paymentchart/$', TemplateView.as_view(
        template_name='reports/payment_chart.html'), name='chart_payment'),
    url(r'callchart/$', TemplateView.as_view(
        template_name='reports/calls_chart.html'), name='chart_call'),
]
