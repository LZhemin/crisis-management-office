from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment
from django.views.generic import ListView,DetailView
#Future use in session-based views
from django.contrib.auth.mixins import LoginRequiredMixin

#Kindly help to remove unwanted modules

sessionId = 2

def index(Request):
    #UNTIL WE IMPLEMENT SESSIONS WE WILL WORKAROUND WITH SESSION ID = 1
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
        crisis_reports = CrisisReport.objects.filter(crisis_id=assigned_crisis.id).select_related('crisisType')
        actionPlanList = ActionPlan.objects.filter(crisis_id=assigned_crisis.id).exclude(status='Planning')
        comments = Comment.objects.all().order_by('timeCreated')
    except(KeyError, Crisis.DoesNotExist):
        context = { 'assigned_crisis': False }
    else:
        context = {
            'assigned_crisis': assigned_crisis,
            'crisis_reports': crisis_reports,
            'ActionPlanList': actionPlanList,
            'comments': comments
        }
    return render(Request, 'analyst/index.html',context)

def historicalData(Request):
    return HttpResponse("HISTORICAL DATA")

'''
#need to slowly take out cause we remove the location need some time to see what to modify
def addCrisisMarker(request, Crisis_id):
    latest_location_list = Location.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_location_list])
    context = {'latest_location_list': latest_location_list}
    try:
        forLocation = request.POST['location']
    except(KeyError, Location.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a Location."}
        })

    try:
        Crisis = request.POST['crisis']
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            {'crisis': Crisis,
            'error_message': "You didn't select a Crisis."}
        })

    else:
        crisisMarker = CrisisReport(latitude=forLocation, longitude=forLocation, Crisis=Crisis)
        crisisMarker.save()
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_id,)))


def deleteCrisisMarker(request, Crisis_id):
    latest_location_list = Location.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_location_list])
    context = {'latest_location_list': latest_location_list}
    try:
        forLocation = request.POST['location']
    except(KeyError, Location.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a location.",}
        })

    try:
        forCrisis = request.POST['crisis']
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            'crisis': Crisis,
            'error_message': "You didn't select a crisis.",
        })

    else:
        crisisMarker = CrisisReport(latitude=forLocation, longitude=forLocation, Crisis=forCrisis)
        crisisMarker.delete()
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis.id,)))


def getCrisisMarker(request, Crisis_id):
    latest_location_list = Location.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_location_list])
    context = {'latest_location_list': latest_location_list}
    try:
        crisisMarker = request.POST['crisisMarker']
        selectedCrisisMarker = Crisis.crisis_set.get(crisisMarker)
    except(KeyError, selectedCrisisMarker.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            {'crisisMarker': crisisMarker,
            'error_message': "You didn't select a crisisMarker."}
        })

    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_id,)))
'''

def submitActionPlan(request, Crisis_id):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_location_list])
    context = {'latest_actionplan_list': latest_actionplan_list}
    try:
        actionPlanDescription = request.POST['description']
    except(KeyError, ActionPlan.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a description.",}
        })

    try:
        forCrisis = request.POST['crisis']
    except(KeyError, Crisis.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a crisis.",}
        })

    else:
        actionPlan = ActionPlan(desciption=actionPlanDescription, crisis_id=forCrisis)
        actionPlan.save()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_id,)))


def getCrisis(request, analyst_id):
    latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    # output = ', '.join([l.Location for l in latest_crisis_list])
    context = {'latest_crisis_list': latest_crisis_list}
    try:
        forCrisis = request.POST['crisis']
        selectedCrisisMarker = Crisis.crisis_set.get(forCrisis)
    except(KeyError, selectedCrisisMarker.DoesNotExist):
    # Redisplay
        return render(request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a Crisis."}
        })
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(analyst_id)))


def editActionPlan(Request, Crisis_id):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_actionplan_list])
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        actionPlan = Request.POST['ActionPlan']
        selectedActionPlan = ActionPlan.ActionPlan.get(ActionPlan)
    except(KeyError, selectedActionPlan.DoesNotExist):
    # Redisplay
        return render(Request, 'analyst/base_site.html', {
            context,
            {'error_message': "You didn't select a Actionplan."}
        })
    else:
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(Crisis_id,)))


#Add the LoginRequiredMixin as the leftmost inheritance
class ActionPlanList(ListView):
    context_object_name = "ActionPlanList"
    template_name = 'analyst/actionplan_list.html'
    #need to get session
    def get_queryset(self):
        return ActionPlan.objects.filter(crisis__analyst = sessionId).prefetch_related('forcedeployment_set')

class ActionPlanDetail(DetailView):
    context_object_name = "Action_Plan"
    template_name='analyst/actionplan_detail.html'
    model = ActionPlan