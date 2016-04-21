from django.conf.urls import url

from product import views


urlpatterns = [
    url(r'sale/$', views.sale, name='product_sale'),
    url(r'payment/$', views.payment, name='product_payment'),
]
