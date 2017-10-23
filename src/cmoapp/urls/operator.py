from django.conf.urls import url
from cmoapp.views import OperatorManager, ApiManager

urlpatterns = [
    url(r'^$', OperatorManager.index, name="Operator_Index"),
    url(r'^(?P<pk>\d+)', OperatorManager.assignnewCrisis, name='Operator_AssignCrisis'),
    url(r'^create_crisis/$', OperatorManager.create_crisis, name="create_crisis"),
    url(r'^delete_crisis/$', OperatorManager.delete_crisis, name="delete_crisis"),

    #Puting here for testing becus of the operator.js call diff url
    url(r'^api/crisisreports/$', ApiManager.crisisreport_collection, name='Api_Crisisreport'),
    url(r'^api/crisisreports/(?P<pk>\d+)', ApiManager.crisisreport_element, name='Api_Crisisreport_element')

]