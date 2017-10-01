"""All Django views for myapp.
"""
from django.shortcuts import render


def index(request):
    """Example to handle request from clients."""
    return render(request, 'main/base_site.html', {})
