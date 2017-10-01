"""All Django views for myapp.
"""
from django.shortcuts import render


def login(request):
    """Example to handle request from clients."""
    return render(request, 'login/login.html', {})


def analyst(request):
    """Example to handle request from clients."""
    return render(request, 'analyst/base_site.html', {})


def operator(request):
    """Example to handle request from clients."""
    return render(request, 'operator/base_site.html', {})


def chief(request):
    """Example to handle request from clients."""
    return render(request, 'chief/base_site.html', {})
