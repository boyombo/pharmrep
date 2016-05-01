from django.conf.urls import url

from product import views


urlpatterns = [
    url(r'sale/(?P<invoice_id>\d+)/$', views.sale, name='product_sale'),
    url(r'invoicelist/$', views.invoice_list, name='invoice_list'),
    url(r'invoice/$', views.invoice, name='product_invoice'),
    url(r'invoicedetail/(?P<invoice_id>\d+)/$',
        views.invoice_detail, name='product_invoice_detail'),
    url(r'payment/$', views.payment, name='product_payment'),
    url(r'paymentlist/$', views.payment_list, name='payment_list'),
    url(r'paymentdetail/(?P<payment_id>\d+)/$',
        views.payment_detail, name='payment_detail'),
]
