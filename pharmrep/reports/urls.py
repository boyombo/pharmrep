from django.conf.urls import url

from reports import views


urlpatterns = [
    url(r'balance/$', views.balance, name='report_balance'),
    url(r'performance/$', views.performance, name='report_performance'),
    url(r'collection/$', views.collection, name='report_collection'),
]
