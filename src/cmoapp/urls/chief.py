from django.conf.urls import url
from cmoapp.views import ChiefOfficerManager

urlpatterns = [
    url(r'^', ChiefOfficerManager.index, name="Chief_Index")
]