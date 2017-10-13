from django.conf.urls import url
from cmoapp.views import OperatorManager

urlpatterns = [
   url(r'^(?P<pk>\d+)', OperatorManager.viewCrisis, name='Operator_View'),
   #url(r'^(?P<pk>[0-9]+)/', OperatorManager.viewCrisis, name = "View_Crisis"),
    url(r'^$', OperatorManager.index, name="Operator_Index")
]