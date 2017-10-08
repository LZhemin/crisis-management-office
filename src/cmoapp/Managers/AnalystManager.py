#!/usr/bin/python

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Analyst, Crisis, CrisisReport, CrisisType, 
Location, ActionPlan, Force, ForceDeployment, EFUpdate

class AnalystManager:
	'Common base class for all Analyst'
	analystID = 0
	crisisID = 0
	data = []

	def __init__(self, crisisID, analystID):
      self.crisisID = crisisID
      self.analystID = analystID
      AnalystManager.analystID += 1
	  
	def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")
   
	def __str__(self):
      return 'Analyst View (%d, %d)' % (self.analystID, self.crisisID)
	 
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
				



