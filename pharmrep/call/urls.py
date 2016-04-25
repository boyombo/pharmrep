from django.conf.urls import url

from call import views


urlpatterns = [
    #url(r'call/$', views.call, name='new_call'),
    url(r'call/$', views.CallView.as_view(), name='new_call'),
    url(r'govt/$', views.GovtCallView.as_view(), name='govt_call'),
    url(r'private/$', views.PrivateCallView.as_view(), name='private_call'),
    url(r'trade/$', views.TradeCallView.as_view(), name='trade_call'),
    url(r'call_list/$', views.call_list, name='call_list'),
]
