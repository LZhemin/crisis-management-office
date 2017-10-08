"""All Django views for myapp.
"""
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Analyst, Crisis, CrisisReport, CrisisType, 
Location, ActionPlan, Force, ForceDeployment, EFUpdate

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

	
#Reference
# def 
	# latest_crisis_list = CrisisReport.objects.order_by('-datetime')[:5]
	# output = ', '.join([c.Crisis for c in latest_crisis_list])
    # return HttpResponse(output)
	
	# #to be write inside HTML
	# # {% if latest_question_list %}
    # # <ul>
    # # {% for question in latest_question_list %}
        # # <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    # # {% endfor %}
    # # </ul>
	# # {% else %}
		# # <p>No polls are available.</p>
	# # {% endif %}
	
	
	# template = loader.get_template('cmoapp/index.html')
    # context = {
        # 'latest_crisis_list': latest_crisis_list,
    # }
    # return HttpResponse(template.render(context, request))
	
	
	# try:
        # crisis = Crisis.objects.get(pk=crisis_id)
    # except Crisis.DoesNotExist:
        # raise Http404("Crisis does not exist")
    # return render(request, 'polls/detail.html', {'crisis': crisis})
	
	# crisis = get_object_or_404(Crisis, pk=crisis_id)
    # return render(request, 'polls/detail.html', {'crisis': crisis})

	
		
	
#AnalystManager----------------------------------------------------------------
def addCrisisMarker(request, crisis_id)
	latest_location_list = Location.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_location_list])
	context = {'latest_location_list': latest_location_list}
	try:
		forLocation = request.POST['location']
	except(KeyError, location.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a location.",
        })
		
	try:
		forCrisis = request.POST['crisis']
	except(KeyError, crisis.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            'crisis': crisis,
            'error_message': "You didn't select a crisis.",
        })
	
	else:
		crisisMarker = CrisisReport(latitude=forLocation, longitude=forLocation, Crisis=forCrisis)
		crisisMarker.save()
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def deleteCrisisMarker(request, crisis_id)
	latest_location_list = Location.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_location_list])
	context = {'latest_location_list': latest_location_list}
	try:
		forLocation = request.POST['location']
	except(KeyError, location.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a location.",
        })
		
	try:
		forCrisis = request.POST['crisis']
	except(KeyError, crisis.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            'crisis': crisis,
            'error_message': "You didn't select a crisis.",
        })
	
	else:
		crisisMarker = CrisisReport(latitude=forLocation, longitude=forLocation, Crisis=forCrisis)
		crisisMarker.delete()
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

def getCrisisMarker(request, crisis_id)
	latest_location_list = Location.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_location_list])
	context = {'latest_location_list': latest_location_list}
	try:
		crisisMarker = request.POST['crisisMarker']		
		selectedCrisisMarker = crisis.crisis_set.get(crisisMarker)
	except(KeyError, selectedCrisisMarker.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            'crisisMarker': crisisMarker,
            'error_message': "You didn't select a crisisMarker.",
        })
	
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

def submitActionPlan(request, crisis_id)
	latest_actionplan_list = Location.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_location_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	try:
		actionPlanDescription = request.POST['description']
	except(KeyError, description.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a description.",
        })
		
	try:
		forCrisis = request.POST['crisis']
	except(KeyError, crisis.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a crisis.",
        })
	
	else:
		actionPlan = ActionPlan(desciption=actionPlanDescription, crisis_id=forCrisis)
		actionPlan.save() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

def getCrisis(request, analyst_id)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	#output = ', '.join([l.Location for l in latest_crisis_list])
	context = {'latest_crisis_list': latest_crisis_list}
	try:
		forCrisis = request.POST['crisis']
		selectedCrisisMarker = crisis.crisis_set.get(forCrisis)
	except(KeyError, selectedCrisisMarker.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a crisisMarker.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

def editActionPlan(Request,crisis_id)
	latest_actionplan_list = Location.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_actionplan_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forActionPlan = request.POST['ActionPlan']
		selectedActionPlan = ActionPlan.ActionPlan.get(forActionPlan)
	except(KeyError, selectedActionPlan.DoesNotExist):
		 # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            'error_message': "You didn't select a ActionPlan.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

#OperatorManager----------------------------------------------------------------
def getCrisisAllocationList(request)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	#output = ', '.join([l.Location for l in latest_crisis_list])
	context = {'latest_crisis_list': latest_crisis_list}
	
	 return render(request, 'operator/base_site.html', {
            context,
        })


def allocateToExistingCrisis(request, crisis_id)
	latest_crisis_list = CrisisReport.objects.order_by('-datetime')[:5]
	#output = ', '.join([l.Location for l in latest_crisis_list])
	context = {'latest_crisis_list': latest_crisis_list}
	
	try:
		forCrisis = request.POST['CrisisReport']
		selectedCrisis = Crisis.Crisis.get(forCrisis)
	except(KeyError, selectedCrisis.DoesNotExist):
		 # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            'error_message': "You didn't select a Crisis.",
        })

	else:
		crisisList = CrisisReport( crisis_id=forCrisis)
		crisisList.save() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))


def allocateCrisis(request, analyst_id)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	#output = ', '.join([l.Location for l in latest_crisis_list])
	context = {'latest_crisis_list': latest_crisis_list}
	
	try:
		forCrisis = request.POST['Crisis']
		selectedCrisis = Crisis.Crisis.get(forCrisis)
	except(KeyError, selectedCrisis.DoesNotExist):
		 # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            'error_message': "You didn't select a Crisis.",
        })

	else:
		crisisList = Crisis( crisis_id=forCrisis)
		crisisList.save() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))


def newCrisisReport(request)
	latest_crisis_list = CrisisReport.objects.order_by('-datetime')[:5]
	#output = ', '.join([l.Location for l in latest_crisis_list])
	context = {'latest_crisis_list': latest_crisis_list}
	
	try:
		forCrisis = request.POST['Crisis']
		selectedCrisis = Crisis.Crisis.get(forCrisis)
	except(KeyError, selectedCrisis.DoesNotExist):
		 # Redisplay
        return render(request, 'operator/base_site.html', {
            context,
            'error_message': "You didn't select a Crisis.",
        })

	else:
		crisisList = CrisisReport( crisis_id=forCrisis)
		crisisList.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))


#ChiefOfficerManager----------------------------------------------------------------
def sendDeployment(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_actionplan_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forName = request.POST['name']
	except(KeyError, name.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a name.",
        })

	try:
		forRecommended = request.POST['recommended']
	except(KeyError, recommended.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a recommended.",
        })
		
	try:
		forMax = request.POST['max']
	except(KeyError, max.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a max.",
        })
	
	else:	
		deployment = ForceDeployment( name=forName, recommanded=forRecommended, max=forMax)
		deployment.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))


def rejectActionPlan(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_actionplan_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forCOApproval = request.POST['COApproval']
	except(KeyError, COApproval.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a COApproval.",
        })

	else:
		rejActionPlan = ActionPlan( COApproval=forCOApproval)
		rejActionPlan.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def forwardActionPlan(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_actionplan_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forCOApproval = request.POST['COApproval']
	except(KeyError, COApproval.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a COApproval.",
        })
	
	else:
		fwActionPlan = ActionPlan( COApproval=forCOApproval)
		fwActionPlan.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def setApprovalStatus(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	#output = ', '.join([l.Location for l in latest_actionplan_list])
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forCOApproval = request.POST['COApproval']
	except(KeyError, COApproval.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a COApproval.",
        })

	else:
		setActionPlan = ActionPlan( COApproval=forCOApproval)
		setActionPlan.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def getCrisisList(request)
	latest_crisis_list = Crisis.objects.order_by('-crisis')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	
	return render(request, 'chief/base_site.html', {
            context,
        })
		
def addEFUpdate(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forActionPlan = request.POST['ActionPlan']
	except(KeyError, ActionPlan.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a ActionPlan.",
        })

	else:
		aEFUpdate = EFUpdate( ActionPlan=forActionPlan)
		EFUpdate.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
#CrisisManager----------------------------------------------------------------
def getHistoricalData(request)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	
	return render(request, 'chief/base_site.html', {
            context,
        })
		
def getCrisis(request, analyst_id)
	latest_crisis_list = Crisis.objects.order_by('-crisis')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	
	return render(request, 'chief/base_site.html', {
            context,
        })
		
def sendActionPlan(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forActionPlan = request.POST['ActionPlan']
	except(KeyError, ActionPlan.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a ActionPlan.",
        })

	else:
		sdActionPlan = ActionPlan( ActionPlan=forActionPlan)
		sdActionPlan.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def updateActionPlan(request,ActionPlan)
	latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
	context = {'latest_actionplan_list': latest_actionplan_list}
	
	try:
		forActionPlan = request.POST['ActionPlan']
	except(KeyError, ActionPlan.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a ActionPlan.",
        })

	else:
		udActionPlan = ActionPlan( ActionPlan=forActionPlan)
		udActionPlan.add() #save to database
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
	
def getLocationCoordinates(request,Location)
	latest_location_list = Location.objects.order_by('-crisis')[:5]
	context = {'latest_location_list': latest_location_list}
	
	try:
		forLocation = request.POST['Location']
		selectedLocation = crisis.location_set.get(forLocation)
	except(KeyError, Location.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a Location.",
        })

def getCrisis(request, crisis_id)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	try:
		forCrisis = request.POST['crisis']
		selectedCrisis = crisis.crisis_set.get(forCrisis)
	except(KeyError, selectedCrisisMarker.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a crisis.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

def getCrisisList(request, crisis_id)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	try:
		forCrisis = request.POST['crisis']
		selectedCrisis = crisis.crisis_set.get(forCrisis)
	except(KeyError, selectedCrisisMarker.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a crisis.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
		
def getSuggestion(request, crisis_id)
	latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
	context = {'latest_crisis_list': latest_crisis_list}
	try:
		forCrisis = request.POST['crisis']
		selectedCrisis = crisis.crisis_set.get(forCrisis)
	except(KeyError, selectedCrisisMarker.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a crisis.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
		
#MapManager----------------------------------------------------------------
def loadMap(request,Location)
	latest_location_list = Location.objects.order_by('-crisis')[:5]
	context = {'latest_location_list': latest_location_list}
	
	try:
		forLocation = request.POST['Location']
	except(KeyError, Location.DoesNotExist):
		 # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            'error_message': "You didn't select a Location.",
        })
	else:
		return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))
