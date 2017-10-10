from django.conf.urls import url
from cmoapp.views import AnalystManager

urlpatterns = [
    url(r'^', AnalystManager.index, name="Chief_Index")
]