from django.conf.urls import url
from cmoapp.views import AnalystManager

urlpatterns = [
    url(r'^$', AnalystManager.index, name="Analyst_Index"),
    url(r'^action_plans/$',AnalystManager.ActionPlanList.as_view(), name='Analyst_Action_Plan_List'),
    url(r'^action_plans/(?P<pk>\d+)/$', AnalystManager.ActionPlanDetail.as_view(), name='Analyst_Action_Plan_Detail'),
    url(r'^get_efupdate_count/$', AnalystManager.get_efupdates_count, name="Get_EfUpdate_Count"),
    url(r'^get_efupdates/$', AnalystManager.get_efupdates, name="Get_EFUpdates"),
    url(r'^get_comment_count/$', AnalystManager.get_comment_count, name="Get_Comment_Count"),
    url(r'^get_comments/$', AnalystManager.get_comments, name="Get_Comments"),
    url(r'^get_crisis_report_count/$', AnalystManager.get_crisis_report_count, name="Get_Crisis_Report_Count"),
    url(r'^get_crisis_reports/$', AnalystManager.get_crisis_reports, name="Get_Crisis_Report"),
]