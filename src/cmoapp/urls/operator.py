from django.conf.urls import url
from cmoapp.views import OperatorManager

urlpatterns = [
    url(r'^', OperatorManager.index, name="Operator_Index"),
    url(r'^post/(?P<pk>\d+)/$', OperatorManager.index, name='post_detail')
]