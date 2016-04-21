from django.conf.urls import url

from product import views


urlpatterns = [
    url(r'sale/$', views.sale, name='product_sale'),
]
