from django.conf.urls import url
from cmoapp.views import AnalystManager

urlpatterns = [
    url(r'^$', AnalystManager.index, name="Analyst_Index"),
    url(r'^action_plans/$',AnalystManager.ActionPlanList.as_view(), name='Analyst_Action_Plan_List'),
    url(r'^action_plans/(?P<pk>\d+)/$', AnalystManager.ActionPlanDetail.as_view(), name='Analyst_Action_Plan_Detail')
]