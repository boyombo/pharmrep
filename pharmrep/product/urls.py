from django.conf.urls import url

from product import views


urlpatterns = [
    url(r'sale/$', views.sale, name='product_sale'),
    url(r'saleslist/$', views.sales_list, name='sales_list'),
    url(r'payment/$', views.payment, name='product_payment'),
    url(r'paymentlist/$', views.payment_list, name='payment_list'),
]
