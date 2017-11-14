"""cmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from cmoapp.views import *

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CrisisReportSerializer
#
# # Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [ # pylint: disable=invalid-name
    url(r'^admin/', admin.site.urls),
    url(r'^analyst/', include('cmoapp.urls.analyst')),
    url(r'^operator/', include('cmoapp.urls.operator')),
    url(r'^chief/', include('cmoapp.urls.chief')),
    url(r'^ActionPlan/', include('cmoapp.urls.actionplan')),
    url(r'^publicmap', include('cmoapp.urls.map')),
    url(r'^accounts/', include('cmoapp.urls.account')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/',include('cmoapp.urls.account')),
	#url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # url(r'^$', login, name='login'),
    url(r'^api/', include('cmoapp.urls.api'))
]
