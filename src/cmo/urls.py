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

urlpatterns = [ # pylint: disable=invalid-name
    url(r'^admin/', admin.site.urls),
    url(r'^analyst/', include('cmoapp.urls.analyst')),
    url(r'^operator/', include('cmoapp.urls.operator')),
    url(r'^chief/', include('cmoapp.urls.chief')),
    url(r'^ActionPlan/', include('cmoapp.urls.actionplan')),
    url(r'^login/', include('cmoapp.urls.login'))
    #url(r'^$', login, name='login'),
]
