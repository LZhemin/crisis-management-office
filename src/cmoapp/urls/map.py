from django.conf.urls import url
from cmoapp.views import PublicMap

urlpatterns = [
    url(r'^', PublicMap.index, name='PublicMap_Index'),
]