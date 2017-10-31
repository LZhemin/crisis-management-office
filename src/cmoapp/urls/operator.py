from django.conf.urls import url
from cmoapp.views import OperatorManager, ApiManager

urlpatterns = [
    url(r'^$', OperatorManager.index, name="Operator_Index"),
    url(r'^(?P<pk>\d+)', OperatorManager.assignnewCrisis, name='Operator_AssignCrisis'),
    url(r'^create_crisis/$', OperatorManager.create_crisis, name="create_crisis"),
    url(r'^delete_crisis/$', OperatorManager.delete_crisis, name="delete_crisis"),
    url(r'^load_crisis/$', OperatorManager.load_crisis, name="load_crisis"),
    url(r'^assignexisting/$', OperatorManager.assignexisting, name="assignexisting"),

    url(r'^crisisdisplay/$', OperatorManager.getallassignedCrisisReport, name='getAssignedCrisis'),

    url(r'^load_analyst/$', OperatorManager.load_analyst, name="load_analyst"),

    #Puting here for testing becus of the operator.js call diff url
    url(r'^api/crisisreports/$', ApiManager.crisisreport_collection, name='Api_Crisisreport'),
    url(r'^api/crisisreports/(?P<pk>\d+)', ApiManager.crisisreport_element, name='Api_Crisisreport_element'),

    url(r'^api/crisis/$', ApiManager.crisis_collection, name='Api_Crisis'),
    url(r'^api/crisis/(?P<pk>\d+)', ApiManager.crisis_element, name='Api_Crisis_element')

]