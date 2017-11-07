from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment
from cmoapp.forms.analyst import ActionPlanForm, ForceForm
from django.views.generic import ListView,DetailView
from rest_framework import serializers
from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, ActionPlanSerializer, CommentSerializer
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
        all_forces = Force.objects.all()
    except(KeyError, Crisis.DoesNotExist):
        context = {'assigned_crisis': False}
    else:
        context = {
            'assigned_crisis': assigned_crisis,
            'crisis_reports': crisis_reports,
            'ActionPlanList': actionPlanList,
            'all_force': all_forces,
            'json_force': AnalystForceSerializer(Force.objects.all(), many=True).data
        }
        if(Request.method == "GET"):
            #WHY DJANGO WHY DONT YOU HAVE AN INBUILT GET OBJECT_OR_NONE
            try:
                planned_action_plan = assigned_crisis.actionplan_set.get(status="Planning")
                context['ActionPlanForm'] = ActionPlanForm(instance=planned_action_plan)
            except ActionPlan.DoesNotExist:
                context['ActionPlanForm'] = ActionPlanForm()
        else:
            print(Request.POST)
            #Validate Action Plan
            submitted_action_plan_form = ActionPlanForm(Request.POST)
            context['ActionPlanForm'] = submitted_action_plan_form
            #SAVE ME https://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/



            if submitted_action_plan_form.is_valid():
                if(Request.POST['submitType'] == "Save"):
                    submitted_action_plan_form.update_or_create(assigned_crisis,"Planning")
                else:
                    #Create
                    submitted_action_plan_form.update_or_create(assigned_crisis,"Awaiting CO Approval")
                    context['ActionPlanForm'] = ActionPlanForm()
    return render(Request, 'analyst/index.html',context)

def crisis_statistics(Request):

    pass

def historicalData(Request):
    return HttpResponse("HISTORICAL DATA")


#Methods used for updating of Page components
def get_efupdates_count(request):
    assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
    efCount = EFUpdate.objects.filter(crisis_id=assigned_crisis.id).count()
    return JsonResponse({'count':efCount}, safe=False)

def get_efupdates(request):
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
        startNum = int(request.POST['startNum'])
        efUpdates = EFUpdate.objects.filter(crisis_id=assigned_crisis.id)[startNum:]
    except(KeyError):
        return JsonResponse({'success':False,'error':'Error in retrieving efupdates!'})

    data = EFUpdateSerializer(efUpdates, many=True).data

    return JsonResponse(data,safe=False)

def get_comment_count(request):
    assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
    commentCount = Comment.objects.filter(actionPlan__crisis__id =assigned_crisis.id).count()
    return JsonResponse({'count':commentCount}, safe=False)

def get_comments(request):
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
        startNum = int(request.POST['startNum'])
        comments = Comment.objects.filter(actionPlan__crisis__id =assigned_crisis.id)[startNum:]
    except(KeyError):
        return JsonResponse({'success':False,'error':'Error in retrieving Comments!'})

    data = CommentSerializer(comments, many=True).data
    return JsonResponse(data, safe=False)

def get_crisis_report_count(request):
    assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
    crCount = CrisisReport.objects.filter(crisis_id=assigned_crisis.id).count()
    return JsonResponse({'count':crCount}, safe=False)

def get_crisis_reports(request):
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
        startNum = int(request.POST['startNum'])
        crisis_reports = CrisisReport.objects.filter(crisis_id=assigned_crisis.id)[startNum:]
    except(KeyError):
        return JsonResponse({'success':False,'error':'Error in retrieving crisis reports!'})

    data = CrisisReportSerializer(crisis_reports, many=True).data
    return JsonResponse(data, safe=False)

def reload_current_stat(request):
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)

    except(KeyError):
        return JsonResponse({'success':False,'error':'Error in retrieving crisis!'})

    data = CrisisSerializer(assigned_crisis).data
    return JsonResponse(data, safe=False)



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

#Internal use only
class AnalystCrisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = ('id', 'text', 'author', 'timeCreated', 'actionPlan')

class AnalystForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Force
        fields = ['name','currentUtilisation']


class EFUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EFUpdate
        fields = ['id','datetime','affectedRadius','totalInjured','totalDeaths','duration','description','actionPlan_id','crisis_id']
        