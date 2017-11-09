from django.conf.urls import url
from cmoapp.views import ApiManager

urlpatterns = [
    #Function Based View
    url(r'^crisisreports/$', ApiManager.crisisreport_collection, name='Api_Crisisreport'),
    url(r'^auth/$', ApiManager.auth_collection, name='Api_Auth'),
    url(r'^pmo/$', ApiManager.PMO_collection, name='Api_PMO'),
    url(r'^pmo/(?P<status>\w+)/$', ApiManager.PMO_collection, name='Api_PMO'),
    url(r'^ef/$', ApiManager.EF_collection, name='Api_EF')

    #url(r'^pmo/resolved$', ApiManager.PMO_Resolved_collection, name='Api_PMO_Resolved'),
    #url(r'^pmo/(?P<status>\w+')

]