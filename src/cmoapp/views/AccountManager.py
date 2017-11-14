from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import logout
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment, Notifications,ForceUtilization

def index(request):
    account = Account.objects.get(login=request.user.username)
    request.session['id'] = account.id
    if account.type == 'Analyst':
        return HttpResponseRedirect('/analyst/')
    if account.type == 'Operator':
        return HttpResponseRedirect('/operator/')
    if account.type == 'Chief':
        return HttpResponseRedirect('/chief/')

    raise Http404('<h1>Invalid accounts</h1>')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')