#!/usr/bin/python

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Analyst, Crisis, CrisisReport, CrisisType, 
Location, ActionPlan, Force, ForceDeployment, EFUpdate

class ChiefOfficerManager:
	'Common base class for ChiefOfficer'
	chiefID = 0
	actionPlanID = 0
	data = []

	def __init__(self, actionPlanID, chiefID):
      self.actionPlanID = actionPlanID
      self.chiefID = chiefID
	  
	def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")
   
	def __str__(self):
      return 'ChiefOfficer View (%d, %d)' % (self.ChiefOfficer, self.actionPlanID)
	 

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