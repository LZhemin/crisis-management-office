from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse


def index(request):
    if request.user.username.endswith('@operator'):
        return render(request, 'operator/index.html')
    if request.user.username.endswith('@analyst'):
        return render(request, 'analyst/index.html')

    raise Http404('<h1>Invalid accounts</h1>')
