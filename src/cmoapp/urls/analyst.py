from django.conf.urls import url
from cmoapp.views import AnalystManager

urlpatterns = [
    url(r'^$', AnalystManager.index, name="Analyst_Index"),
    url(r'^action_plans/$',AnalystManager.ActionPlanList.as_view(), name='Analyst_Action_Plan_List'),
    url(r'^action_plans/(?P<pk>\d+)/$', AnalystManager.ActionPlanDetail.as_view(), name='Analyst_Action_Plan_Detail'),
    url(r'^get_efupdate_count/$', AnalystManager.get_efupdates_count, name="Get_EfUpdate_Count"),
    url(r'^get_efupdates/$', AnalystManager.get_efupdates, name="Get_EFUpdates"),
    url(r'^reload_notification/$', AnalystManager.reload_notification, name="Reload_Notification"),
    url(r'^delete_notification/$', AnalystManager.delete_notification, name="Delete_Notification"),
    url(r'^get_comment_count/$', AnalystManager.get_comment_count, name="Get_Comment_Count"),
    url(r'^get_comments/$', AnalystManager.get_comments, name="Get_Comments"),
    url(r'^get_crisis_report_count/$', AnalystManager.get_crisis_report_count, name="Get_Crisis_Report_Count"),
    url(r'^get_crisis_reports/$', AnalystManager.get_crisis_reports, name="Get_Crisis_Report"),
    url(r'^reload_current_stat/$', AnalystManager.reload_current_stat, name="Reload_Current_Stat"),
    url(r'^historical_data/$', AnalystManager.getHistorical_data, name="display_historical_data_analyst"),
    url(r'^generateCombatAP/$', AnalystManager.ActionPlanGenerator.generateCombatPlan, name='generate_combat_action_plan'),
    url(r'^generateCleanAP/$', AnalystManager.ActionPlanGenerator.generateCleanup, name='generate_cleanup_action_plan'),
]