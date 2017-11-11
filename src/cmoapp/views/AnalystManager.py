from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment, Notifications
from cmoapp.forms.analyst import ActionPlanForm, ForceForm
from django.views.generic import ListView,DetailView
from rest_framework import serializers
from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, ActionPlanSerializer, CommentSerializer
import datetime
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
        notifications = Notifications.objects.all().exclude(new=0)
        notification_count = notifications.count()
    except(KeyError, Crisis.DoesNotExist):
        context = {'assigned_crisis': False}
    else:
        context = {
            'assigned_crisis': assigned_crisis,
            'crisis_reports': crisis_reports,
            'ActionPlanList': actionPlanList,
            'all_force': all_forces,
            'json_force': AnalystForceSerializer(Force.objects.all(), many=True).data,
            'notification_count': notification_count
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

    data = AnalystEFUpdateSerializer(efUpdates, many=True).data

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

    data = []
    for comment in comments:
        data.append({
            'author': comment.author,
            'text': comment.text,
            'plan_number': comment.actionPlan.plan_number,
            'timeCreated': comment.timefrom()
        })
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


def reload_notification(request):
    try:
        notifications = Notifications.objects.all().exclude(new=0)
        notification_count = notifications.count()
    except KeyError:
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    else:
        context = {
            'all_notifications': notifications,
            'notification_count': notification_count
        }
        return render(request, 'chief/ui_components/top_navigation.html', context)


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

class AnalystEFUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EFUpdate
        fields = ['id','datetime','affectedRadius','totalInjured','totalDeaths','duration','description','actionPlan_id','crisis_id']


class ActionPlanGenerator:
    def generateCombatPlan(crisis_id):

        dt = datetime.timedelta(days=0, hours=0)
        option = 0
        findCrisisReport = CrisisReport.objects.filter(crisis=crisis_id)

        rule1 = False
        rule2 = True
        rule3 = True
        rule4 = True
        rule5 = True
        rule6 = True
        rule7 = True
        rule8 = True
        rule9 = True
        rule10 = True
        rule11 = True
        fire = False
        largescalecrisis = False
        terroristattack = False
        riotormasslooting = False
        actionplanDescription = ""
        for report in findCrisisReport.all():
            if (report.crisisType.name == 'Bombing') or (report.crisisType.name == 'Hijacking & Skyjacking') or (report.crisisType.name == 'Cyber Terrorism') or (report.crisisType.name == 'Nuclear/Radiological') or (report.crisisType.name == 'Biological-Chemical') or (report.crisisType.name == 'Kidnapping') or (report.crisisType.name == 'Arson') or (report.crisisType.name == 'Massacre'):
                terroristattack = True
            if (report.radius > 199):
                rule7 = False
                rule8 = False
                rule9 = False
                rule10 = False
                rule11 = False
                largescalecrisis = True
            if (terroristattack):
                rule3 = False
                rule4 = False
                rule5 = False
                rule6 = False
                rule8 = False
                rule9 = False
                rule10 = False
                rule11 = False
            if (report.crisisType.name == 'Large Fire') or (report.crisisType.name == 'Fire'):
                rule4 = False
                rule5 = False
                rule6 = False
                rule9 = False
                rule10 = False
                rule11 = False
                fire = True
            if (report.crisisType.name == 'Natural Disaster'):
                rule6 = False
            if (report.crisisType.name == 'Pandemic'):
                rule5 = False
                rule10 = False
                rule11 = False
            if (report.crisisType.name == 'Riot') or (report.crisisType.name == 'Mass Looting'):
                rule2 = False
                rule3 = False
                rule4 = False
                rule5 = False
                rule6 = False
                rule11 = False
                riotormasslooting = True
            if (largescalecrisis) and (riotormasslooting):
                rule1 = True

        if (rule5 or rule10 or rule11) == False:
            actionplanDescription = actionplanDescription + "Cordon off affected area.\n"
        if rule1:
            actionplanDescription = actionplanDescription + "Curfew will be set and implemented.\n"
        actionplanDescription = actionplanDescription + "Public Advisory will be carried out on all medias.\n"
        if (fire) == True:
            actionplanDescription = actionplanDescription + "Deploy SCDF to extinguish any fire on scene\n"
        actionplanDescription = actionplanDescription + "Deploy SCDF to decontaminate affected area and carry out search & rescue.\n"
        if (rule7 or rule8 or rule9 or rule10 or rule11) == False:
            if riotormasslooting == True:
                actionplanDescription = actionplanDescription + "Deploy SAF to contain the riot and crowd control. Traffic redirection to ensure no one enters the affected area.\n"
            else:
                if terroristattack == True:
                    actionplanDescription = actionplanDescription + "Deploy SAF to carry out lethal response to terrorist causing damage. Explosives expert to be sent if there's a bomb.\n"
                else:
                    actionplanDescription = actionplanDescription + "Deploy SAF to redirect the traffic to ensure no one enters the affected area. \n"
        if (rule11) == False:
            actionplanDescription = actionplanDescription + "SPF Deployment to help out focusing on the safety of the citizens. \n"
        ap = ActionPlan(description=actionplanDescription,
                        status="Planning",
                        type="Combat",
                        resolution_time=dt,
                        projected_casualties=0.0,
                        crisis_id=crisis_id)
        return ap

    def generateCleanup(crisis_id):
        dt = datetime.timedelta(days=0, hours=0)
        option = 0
        findCrisisReport = CrisisReport.objects.filter(crisis=crisis_id)

        rule1 = False
        rule2 = True
        rule3 = True
        rule4 = True
        rule5 = True
        rule6 = True
        rule7 = True
        rule8 = True
        rule9 = True
        rule10 = True
        rule11 = True
        fire = False
        largescalecrisis = False
        terroristattack = False
        riotormasslooting = False
        actionplanDescription = ""
        for report in findCrisisReport.all():
            if (report.crisisType.name == 'Bombing') or (report.crisisType.name == 'Hijacking & Skyjacking') or (report.crisisType.name == 'Cyber Terrorism') or (report.crisisType.name == 'Nuclear/Radiological') or (report.crisisType.name == 'Biological-Chemical') or (report.crisisType.name == 'Kidnapping') or (report.crisisType.name == 'Arson') or (report.crisisType.name == 'Massacre'):
                terroristattack = True
            if (report.radius > 199):
                rule7 = False
                rule8 = False
                rule9 = False
                rule10 = False
                rule11 = False
                largescalecrisis = True
            if (terroristattack):
                rule3 = False
                rule4 = False
                rule5 = False
                rule6 = False
                rule8 = False
                rule9 = False
                rule10 = False
                rule11 = False
            if (report.crisisType.name == 'Large Fire') or (report.crisisType.name == 'Fire'):
                rule4 = False
                rule5 = False
                rule6 = False
                rule9 = False
                rule10 = False
                rule11 = False
                fire = True
            if (report.crisisType.name == 'Natural Disaster'):
                rule6 = False
            if (report.crisisType.name == 'Pandemic'):
                rule5 = False
                rule10 = False
                rule11 = False
            if (report.crisisType.name == 'Riot') or (report.crisisType.name == 'Mass Looting'):
                rule2 = False
                rule3 = False
                rule4 = False
                rule5 = False
                rule6 = False
                rule11 = False
                riotormasslooting = True
            if (largescalecrisis) and (riotormasslooting):
                rule1 = True

        if (rule5 or rule10 or rule11) == False:
            actionplanDescription = actionplanDescription + "Cordon off affected area.\n"
        if rule1:
            actionplanDescription = actionplanDescription + "Curfew will be set and implemented.\n"
        actionplanDescription = actionplanDescription + "Public Advisory will be carried out on all medias.\n"
        if (fire) == True:
            actionplanDescription = actionplanDescription + "Deploy SCDF to extinguish any fire on scene\n"
        actionplanDescription = actionplanDescription + "Deploy SCDF to decontaminate affected area and carry out search & rescue.\n"
        if (rule7 or rule8 or rule9 or rule10 or rule11) == False:
            if riotormasslooting == True:
                actionplanDescription = actionplanDescription + "Deploy SAF to contain the riot and crowd control. Traffic redirection to ensure no one enters the affected area.\n"
            else:
                if terroristattack == True:
                    actionplanDescription = actionplanDescription + "Deploy SAF to carry out lethal response to terrorist causing damage. Explosives expert to be sent if there's a bomb.\n"
                else:
                    actionplanDescription = actionplanDescription + "Deploy SAF to redirect the traffic to ensure no one enters the affected area. \n"
        if (rule11) == False:
            actionplanDescription = actionplanDescription + "SPF Deployment to help out focusing on the safety of the citizens. \n"
        ap = ActionPlan(description=actionplanDescription,
                        status="Planning",
                        type="Clean Up",
                        resolution_time=dt,
                        projected_casualties=0.0,
                        crisis_id=crisis_id)
        return ap
