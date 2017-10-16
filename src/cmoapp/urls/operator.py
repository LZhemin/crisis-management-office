from django.conf.urls import url
from cmoapp.views import OperatorManager

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', OperatorManager.viewCrisis, name='Operator_View'),

    url(r'^allolist/$', OperatorManager.getCrisisAllocationList, name='Operator_ViewAllocationList'),
    url(r'^alloexcrisis/$', OperatorManager.allocateToExistingCrisis, name='Operator_allocateToExistingCrisis'),
    url(r'^allocrisis/$', OperatorManager.allocateCrisis, name='Operator_AllocateCrisis'),
    url(r'^newcrisisrpt/$', OperatorManager.newCrisisReport, name='Operator_NewCrisisReport'),

   #url(r'^(?P<pk>[0-9]+)/', OperatorManager.viewCrisis, name = "View_Crisis"),
    url(r'^$', OperatorManager.index, name="Operator_Index")


]