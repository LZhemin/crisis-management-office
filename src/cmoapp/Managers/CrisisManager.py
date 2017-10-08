#!/usr/bin/python

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Analyst, Crisis, CrisisReport, CrisisType, 
Location, ActionPlan, Force, ForceDeployment, EFUpdate

class CrisisManager:
	'Common base class for all Crisis'
	crisisID = 0
	actionPlanID = 0
	data = []

	def __init__(self, crisisID, actionPlanID):
      self.crisisID = crisisID
      self.actionPlanID = actionPlanID
	  
	def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")
   
	def __str__(self):
      return 'Crisis View (%d, %d)' % (self.crisisID, self.actionPlanID)
	 
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
			