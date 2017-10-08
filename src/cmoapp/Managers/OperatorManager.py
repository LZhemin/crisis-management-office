#!/usr/bin/python

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Analyst, Crisis, CrisisReport, CrisisType, 
Location, ActionPlan, Force, ForceDeployment, EFUpdate

class OperatorManager:
	'Common base class for all Crisis'
	operatorID = 0
	crisisID = 0
	data = []

	def __init__(self, operatorID, crisisID):
      self.operatorID = operatorID
      self.crisisID = crisisID
	  
	def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")
   
	def __str__(self):
      return 'Crisis View (%d, %d)' % (self.operatorID, self.crisisID)
	 
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

		


