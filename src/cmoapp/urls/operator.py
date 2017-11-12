from django.conf.urls import url
from cmoapp.views import OperatorManager, ApiManager

urlpatterns = [
    url(r'^$', OperatorManager.index, name="Operator_Index"),
    url(r'^(?P<pk>\d+)', OperatorManager.assignnewCrisis, name='Operator_AssignCrisis'),
    url(r'^create_crisis/$', OperatorManager.create_crisis, name="create_crisis"),
    url(r'^assignexisting/$', OperatorManager.assignexisting, name="assignexisting"),
    url(r'^reload_notification/$', OperatorManager.reload_notification, name="Reload_Notification"),
    url(r'^delete_notification/$', OperatorManager.delete_notification, name="Delete_Notification"),
    url(r'^crisisdisplay/$', OperatorManager.getallassignedCrisisReport, name='getAssignedCrisis'),
    url(r'^load_analyst/$', OperatorManager.load_analyst, name="load_analyst"),
    url(r'^crisisreports/$', OperatorManager.get_crisisreport_collection, name='Operator_Crisisreport'),
]