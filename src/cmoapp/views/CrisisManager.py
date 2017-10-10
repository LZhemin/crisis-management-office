from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Analyst, Crisis, CrisisReport, CrisisType, Location, ActionPlan, Force, ForceDeployment, EFUpdate

#Kindly help to remove unwanted modules

def getHistoricalData(request):
    latest_crisis_list = Crisis.objects.order_by('-datetime')
    context = {'latest_crisis_list': latest_crisis_list}

    return render(request, 'chief/base_site.html', {
        context,
    })


def getCrisis(request, analyst_id):
    latest_crisis_list = Crisis.objects.order_by('-crisis')[:5]
    context = {'latest_crisis_list': latest_crisis_list}

    return render(request, 'chief/base_site.html', {
        context,
    })


def sendActionPlan(request, Crisis_ID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        forActionPlan = request.POST['ActionPlan']
    except(KeyError, ActionPlan.DoesNotExist):
        return render(request, 'chief/base_site.html', {context,{'error_message': "You didn't select a ActionPlan.",}})
    else:
        sdActionPlan = ActionPlan(ActionPlan=forActionPlan)
        sdActionPlan.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_ID)))


def updateActionPlan(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        forActionPlan = request.POST['ActionPlan']
    except(KeyError, ActionPlan.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {context,{'error_message': "You didn't select a ActionPlan."}})
    else:
        udActionPlan = ActionPlan(crisis=CrisisID)
        udActionPlan.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(CrisisID)))


def getLocationCoordinates(request, CrisisID):
    latest_location_list = Location.objects.order_by('-crisis')[:5]
    context = {'latest_location_list': latest_location_list}

    try:
        forLocation = request.POST['Location']
        selectedLocation = Crisis.location_set.get(forLocation)
    except(KeyError, Location.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a Location."}
    })

def getCrisis(request, crisis_id):
    latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    context = {'latest_crisis_list': latest_crisis_list}
    try:
        forCrisis = request.POST['crisis']
        selectedCrisis = Crisis.objects.get(forCrisis)
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
        context,
        {'error_message': "You didn't select a crisis."}})
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis_id,)))


def getCrisisList(request, crisis_id):
    latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    context = {'latest_crisis_list': latest_crisis_list}
    try:
        forCrisis = request.POST['crisis']
        selectedCrisis = Crisis.objects.get(forCrisis)
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
        context,
        {'error_message': "You didn't select a crisis."}})
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis_id,)))


def getSuggestion(request, crisis_id):
    latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    context = {'latest_crisis_list': latest_crisis_list}
    try:
        forCrisis = request.POST['crisis']
        selectedCrisis = Crisis.objects.get(forCrisis)
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
        context,
        {'error_message': "You didn't select a crisis."}})
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis_id,)))