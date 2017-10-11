from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, Location, ActionPlan, Force, ForceDeployment, EFUpdate

#Kindly help to remove unwanted modules

def index(Request):

    getallcrisis = CrisisReport.objects.all();
    return render(Request, 'operator/base_site.html',{'getallcrisis':getallcrisis})

def getCrisisAllocationList(Request):
    #latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    # output = ', '.join([l.Location for l in latest_crisis_list])
    #context = {'latest_crisis_list': latest_crisis_list}

    return render(Request, 'operator/base_site.html', {})


def allocateToExistingCrisis(request, crisis_id):
    crisis_list = CrisisReport.objects.order_by('-datetime')
    # output = ', '.join([l.Location for l in latest_crisis_list])
    context = {'latest_crisis_list': crisis_list}

    try:
        forCrisis = request.POST['CrisisReport']
        selectedCrisis = Crisis.Crisis.get(forCrisis)
    except(KeyError, selectedCrisis.DoesNotExist):
    # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            {'error_message': "You didn't select a Crisis."}
        })

    else:
        crisisList = CrisisReport(crisis_id=forCrisis)
        crisisList.save()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis_id)))


def allocateCrisis(request, analyst_id):
    latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    # output = ', '.join([l.Location for l in latest_crisis_list])
    context = {'latest_crisis_list': latest_crisis_list}

    try:
        forCrisis = request.POST['Crisis']
        selectedCrisis = Crisis.Crisis.get(forCrisis)
    except(KeyError, selectedCrisis.DoesNotExist):
    # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            {'error_message': "You didn't select a Crisis."}
        })

    else:
        crisisList = Crisis(crisis_id=forCrisis)
        crisisList.save()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(analyst_id)))


def newCrisisReport(request,Crisis_ID):
    latest_crisis_list = CrisisReport.objects.order_by('-datetime')[:5]
    # output = ', '.join([l.Location for l in latest_crisis_list])
    context = {'latest_crisis_list': latest_crisis_list}

    try:
        forCrisis = request.POST['Crisis']
        selectedCrisis = Crisis.Crisis.get(forCrisis)
    except(KeyError, selectedCrisis.DoesNotExist):
    # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            {'error_message': "You didn't select a Crisis."}
        })

    else:
        crisisList = CrisisReport(crisis_id=forCrisis)
        crisisList.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_ID)))