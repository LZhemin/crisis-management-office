from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(Request):
    return render(Request, 'map/index.html')
