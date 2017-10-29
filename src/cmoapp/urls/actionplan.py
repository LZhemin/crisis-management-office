from django.conf.urls import url
from cmoapp.views import GenerateActionPlan

urlpatterns = [
    url(r'^', GenerateActionPlan.index, name="GenerateActionPlan_Index"),
    url(r'^generateactionplan/$', GenerateActionPlan.generateActionPlan, name='generateActionPlan'),
]