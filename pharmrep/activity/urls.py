from django.conf.urls import url

from activity import views


urlpatterns = [
    #url(r'call/$', views.call, name='new_call'),
    url(r'call/$', views.CallView.as_view(), name='new_call'),
    url(r'govt/$', views.GovtCallView.as_view(), name='govt_call'),
    url(r'private/$', views.PrivateCallView.as_view(), name='private_call'),
    url(r'trade/$', views.TradeCallView.as_view(), name='trade_call'),
    url(r'call_list/$', views.call_list, name='call_list'),
    url(r'competition/$', views.CompetitionView.as_view(), name='competition'),
    url(r'competitionlist/$', views.competition_list, name='competition_list'),
    url(r'contact/$', views.ContactView.as_view(), name='contact'),
    url(r'contactlist/$', views.contact_list, name='contact_list'),
    url(r'market/$', views.MarketView.as_view(), name='market'),
    url(r'marketlist/$', views.market_list, name='market_list'),
    url(r'conclusion/$', views.ConclusionView.as_view(), name='conclusion'),
    url(r'conclusionlist/$', views.conclusion_list, name='conclusion_list'),
    url(r'itinerary/$', views.ItineraryView.as_view(), name='itinerary'),
    url(r'itinerarylist/$', views.ItineraryListView.as_view(),
        name='itinerary_list'),
    url(r'summary/$', views.SummaryView.as_view(), name='summary'),
    url(r'summarylist/$', views.SummaryListView.as_view(),
        name='summary_list'),
    url(r'summarydetail/(?P<summary_id>\d+)/$', views.summary_detail,
        name='summary_detail'),
]
