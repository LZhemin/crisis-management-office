from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, Location, ActionPlan, Force, ForceDeployment, EFUpdate

#Kindly help to remove unwanted modules

def loadMap(request, Location):
    latest_location_list = Location.objects.order_by('-crisis')[:5]
    context = {'latest_location_list': latest_location_list}

    try:
        forLocation = request.POST['Location']
    except(KeyError, Location.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
        context,
            {'error_message': "You didn't select a Location."}
        })
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))