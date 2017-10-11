from django.conf.urls import url
from cmoapp.views import OperatorManager

urlpatterns = [
    url(r'^', OperatorManager.index, name="Operator_Index")
]