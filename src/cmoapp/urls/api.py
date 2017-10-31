from django.conf.urls import url
from cmoapp.views import ApiManager

urlpatterns = [
    #Function Based View
    url(r'^crisis/$', ApiManager.crisis_collection, name='Api_Crisis'),
    url(r'^crisis/(?P<pk>\d+)', ApiManager.crisis_element, name='Api_Crisis_element'),

    url(r'^crisisreports/$', ApiManager.crisisreport_collection, name='Api_Crisisreport'),
    url(r'^crisisreports/(?P<pk>\d+)', ApiManager.crisisreport_element, name='Api_Crisisreport_element'),

    url(r'^actionplans/$', ApiManager.actionplan_collection, name='Api_Actionplan'),
    url(r'^actionplans/(?P<pk>\d+)', ApiManager.actionplan_element, name='Api_Actionplan_element'),

    url(r'^auth/$', ApiManager.auth_collection, name='Api_Auth'),

    #Generic Based View
    #url(r'^crisiss/$', ApiManager.CrisisCollection.as_view(), name='Api_Crisisreport'),
    #url(r'^crisiss/(?P<pk>\d+)', ApiManager.CrisisMember.as_view(), name='Api_Crisisreport_element'),

    #url(r'^crisisreports/$', ApiManager.CrisisReportCollection.as_view(), name='Api_Crisisreport'),
    #url(r'^crisisreports/(?P<pk>\d+)', ApiManager.CrisisReportMember.as_view(), name='Api_Crisisreport_element'),

    #url(r'^actionplans/$', ApiManager.ActionPlanCollection.as_view(), name='Api_Crisisreport'),
    #url(r'^actionplans/(?P<pk>\d+)', ApiManager.ActionPlanMember.as_view(), name='Api_Crisisreport_element')


]