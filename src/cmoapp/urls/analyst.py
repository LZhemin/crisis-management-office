from django.conf.urls import url
from cmoapp.views import AnalystManager

urlpatterns = [
    url(r'^$', AnalystManager.index, name="Analyst_Index"),
    url(r'^historicaldata', AnalystManager.historicalData, name="Analyst_Historical_Data")
]