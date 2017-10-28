from django.conf.urls import url
from cmoapp.views import ChiefOfficerManager

urlpatterns = [
    url(r'^', ChiefOfficerManager.index, name="Chief_Index"),
    url(r'^action_plans/(?P<pk>\d+)/$', ChiefOfficerManager.ActionPlanDetail.as_view(), name='Analyst_Action_Plan_Detail')
]