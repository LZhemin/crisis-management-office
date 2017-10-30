from django.conf.urls import url
from cmoapp.views import LoginManager

urlpatterns = [
    url(r'^', LoginManager.index, name='Login_Index')
]