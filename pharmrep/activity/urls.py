from django.conf.urls import url

from activity import views


urlpatterns = [
    #url(r'call/$', views.call, name='new_call'),
    url(r'call/$', views.CallView.as_view(), name='new_call'),
    url(r'govt/$', views.GovtCallView.as_view(), name='govt_call'),
    url(r'private/$', views.PrivateCallView.as_view(), name='private_call'),
    url(r'trade/$', views.TradeCallView.as_view(), name='trade_call'),
    url(r'call_list/$', views.CallListView.as_view(), name='call_list'),
    url(r'call_detail/(?P<call_id>\d+)/$',
        views.call_detail, name='call_detail'),
    url(r'products/(?P<call_id>\d+)/$',
        views.product_detailed, name='product_detailed'),
    url(r'remove_order/(?P<detail_id>\d+)/$',
        views.remove_order, name='remove_order'),

    url(r'competition/$', views.CompetitionView.as_view(), name='competition'),
    url(r'competitionlist/$', views.CompetitionListView.as_view(),
        name='competition_list'),
    url(r'competition_detail/(?P<entry_id>\d+)/$',
        views.competition_detail, name='competition_detail'),

    url(r'contact/$', views.ContactView.as_view(), name='contact'),
    url(r'contactlist/$', views.ContactListView.as_view(),
        name='contact_list'),
    url(r'market/$', views.MarketView.as_view(), name='market'),
    url(r'marketlist/$', views.MarketListView.as_view(), name='market_list'),
    url(r'conclusion/$', views.ConclusionView.as_view(), name='conclusion'),
    url(r'conclusionlist/$', views.ConclusionListView.as_view(),
        name='conclusion_list'),
    #url(r'itinerary/$', views.ItineraryView.as_view(), name='itinerary'),
    url(r'itinerary/$', views.itinerary, name='itinerary'),
    url(r'itinerarylist/$', views.ItineraryListView.as_view(),
        name='itinerary_list'),
    url(r'edit_itinerary/(?P<item_id>\d+)/$', views.edit_itinerary,
        name='edit_itinerary'),
    url(r'summary/$', views.SummaryView.as_view(), name='summary'),
    url(r'summarylist/$', views.SummaryListView.as_view(),
        name='summary_list'),
    url(r'summarydetail/(?P<summary_id>\d+)/$', views.summary_detail,
        name='summary_detail'),
]
