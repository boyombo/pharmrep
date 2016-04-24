from django.conf.urls import url

from call import views


urlpatterns = [
    url(r'call/$', views.call, name='new_call'),
    url(r'call_list/$', views.call_list, name='call_list'),
]
