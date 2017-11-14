from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth import logout


def index(request):
    print("FUCK")
    if request.user.username.endswith('@operator'):
        return HttpResponseRedirect('/operator/')
    if request.user.username.endswith('@analyst'):
        return HttpResponseRedirect('/analyst/')
    if request.user.username.endswith('@chief'):
        print("I cna come here!")
        return HttpResponseRedirect('/chief/')

    raise Http404('<h1>Invalid accounts</h1>')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')