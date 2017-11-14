from django.conf.urls import url
from cmoapp.views import AccountManager

urlpatterns = [
    url(r'^profile/$', AccountManager.index, name='AccountManager_Index'),
    url(r'^logout/$', AccountManager.logout_view, name='AccountManager_Logout'),
]
