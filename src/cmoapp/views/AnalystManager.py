from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment, Notifications,ForceUtilization
from cmoapp.forms.analyst import ActionPlanForm, ForceForm
from django.views.generic import ListView,DetailView
from rest_framework import serializers
from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, ActionPlanSerializer, CommentSerializer, NotificationSerializer
import datetime

#Future use in session-based views
from django.contrib.auth.mixins import LoginRequiredMixin

#Kindly help to remove unwanted modules

sessionId = 1


def getHistorical_data(request):
    try:
        getallcrisis = Crisis.objects.filter(status='Resolved')
        getallcrisisreport = CrisisReport.objects.all()
        getallForceDeployment = ForceDeployment.objects.all()
        getallForceUtilization = ForceUtilization.objects.all()
        getallActionPlan = ActionPlan.objects.all()
        getallEFUpdate = EFUpdate.objects.all()

    except(KeyError, getallcrisis.DoesNotExist):
        context = {'getallcrisis': False}
    else:
        context = {'getallcrisis': getallcrisis, 'getallcrisisreport': getallcrisisreport,
                   'getallForceDeployment': getallForceDeployment, 'getallForceUtilization': getallForceUtilization,
                   'getallActionPlan': getallActionPlan,
                   'getallEFUpdate': getallEFUpdate}

        return render(request, 'analyst/historical.html', context)

def index(Request,pk):
    #UNTIL WE IMPLEMENT SESSIONS WE WILL WORKAROUND WITH SESSION ID = 1
    try:
        id =pk
        assigned_crisis = Crisis.objects.get(analyst__id=id)
        crisis_reports = CrisisReport.objects.filter(crisis_id=assigned_crisis.id).select_related('crisisType')
        actionPlanList = ActionPlan.objects.filter(crisis_id=assigned_crisis.id).exclude(status='Planning')
        all_forces = Force.objects.all()
        forceWidth = int(12 / Force.objects.count())
        sideWidth = int(12 - (forceWidth * Force.objects.count()))/2
        notifications = Notifications.objects.filter(_for=sessionId).exclude(new=0)
        notification_count = notifications.count()

    except(KeyError, Crisis.DoesNotExist):
        context = {'assigned_crisis': False}
    else:
        context = {
            'id':id,
            'assigned_crisis': assigned_crisis,
            'crisis_reports': crisis_reports,
            'ActionPlanList': actionPlanList,
            'all_force': all_forces,
            'forceWidth':forceWidth,
            'sideWidth':sideWidth,
            'json_force': AnalystForceSerializer(Force.objects.all(), many=True).data,
            'notifications': notifications,
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

            forces_indexes = Request.POST['force_indexes']
            force_forms = []
            for index in forces_indexes:
                force_forms.append(Request.POST,ForceForm(prefix=index))

            if submitted_action_plan_form.is_valid() and all([form.is_valid for form in force_forms]):
                if(Request.POST['submitType'] == "Save"):
                    ap = submitted_action_plan_form.update_or_create(assigned_crisis,"Planning")
                else:
                    #Create
                    submitted_action_plan_form.update_or_create(assigned_crisis,"Awaiting CO Approval")
                    context['ActionPlanForm'] = ActionPlanForm()

    return render(Request, 'analyst/index.html', context)


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
        notifications = Notifications.objects.filter(_for=sessionId).exclude(new=0)
        data = NotificationSerializer(notifications, many=True).data
    except KeyError:
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    return JsonResponse(data, safe=False)


def delete_notification(request):
    try:
        notifications = Notifications.objects.filter(_for=sessionId).exclude(new=0)
    except KeyError:
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    for notification in notifications:
        notification.new = 0
        notification.save()
    return JsonResponse('OK', safe=False)


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

def generateCombatPlan(request):
        crisis_id = request.POST.get("crisisid");
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
        spf = False
        scdf = False
        saf = False
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

        actionplanDescription = actionplanDescription + "List of actions to be carried out: \n"
        if (rule5 or rule10 or rule11) == False:
            actionplanDescription = actionplanDescription + "Cordon off affected area to prevent access to or from the area. \nEntry to area will require special identification.\n"
        if rule1:
            actionplanDescription = actionplanDescription + "Curfew will be set and implementation will be carried out on immediate effect.\n"
            actionplanDescription = actionplanDescription + "Public Advisory will be carried out on all medias. \nPublic are advised to adhere to the news and proceed to carry out the necessary actions.\n"
        if (fire) == True:
            actionplanDescription = actionplanDescription + "Deploy SCDF to extinguish any fire on scene and tend to casualty\n"
            actionplanDescription = actionplanDescription + "Deploy SCDF to decontaminate affected area and carry out search & rescue.\n"
            scdf=True
        if (rule7 or rule8 or rule9 or rule10 or rule11) == False:
            if riotormasslooting == True:
                actionplanDescription = actionplanDescription + "Deploy SAF to contain the riot and crowd control. \nTraffic redirection to ensure no one enters the affected area.\n"
                saf=True
            else:
                if terroristattack == True:
                    actionplanDescription = actionplanDescription + "Deploy SAF to carry out lethal response to terrorist causing damage.\n Explosives expert to be sent if there's a bomb.\n"
                    saf=True
                else:
                    actionplanDescription = actionplanDescription + "Deploy SAF to redirect the traffic to ensure no one without approved identification are allowed to enter the affected area.\n"
                    saf=True
        if (rule11) == False:
            actionplanDescription = actionplanDescription + "SPF Deployment to help out in the overall crisis combat but focus more on the safety of the citizens. \n"
            spf=True
      #  ap = ActionPlan(description=actionplanDescription,
      #                  status="Planning",
      #                  type="Combat",
      #                  resolution_time=dt,
      #                  projected_casualties=0.0,
      #                  crisis_id=crisis_id)
      #  return JsonResponse(ap, safe=False)

        response_data = {}
        response_data['result'] = 'Create post successful!'
        response_data['description'] = actionplanDescription
        response_data['status'] = "Planning"
        response_data['type'] = "Combat"
        response_data['resolution_time'] = dt
        response_data['projected_casualties'] = 0
        response_data['crisis_id'] = crisis_id
        response_data['spf'] = spf
        response_data['scdf'] = scdf
        response_data['saf'] = saf

        return JsonResponse(response_data)






def generateCleanup(request):
        crisis_id = request.POST.get("crisisid");
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
        spf = False
        scdf = False
        saf = False
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

        actionplanDescription = actionplanDescription + "List of actions to be carried out: \n"
        if (rule5 or rule10 or rule11) == False:
            actionplanDescription = actionplanDescription + "Cordon off affected area to prevent access to or from the area. \nEntry to area will require special identification until clean up is done.\n"
        if rule1:
            actionplanDescription = actionplanDescription + "Curfew will be lifted after clean up is done. \nInformation to be included in broadcast.\n"
            actionplanDescription = actionplanDescription + "Closure of crisis will be broadcast on all medias. \nAny necessary precautions that the public should be taken should also be highlighted.\n"
        if (fire) == True:
            actionplanDescription = actionplanDescription + "SCDF to inspect the scene for any casualty and tend to found casualties.\n"
            actionplanDescription = actionplanDescription + "SCDF to continue decontaminating affected area and tend to found casualties.\n"
            scdf = True
        if (rule7 or rule8 or rule9 or rule10 or rule11) == False:
            if riotormasslooting == True:
                actionplanDescription = actionplanDescription + "SAF to contain crowd until dispersion. Traffic redirection to ensure no one enters the affected area until clean up is done.\n"
                saf=True;
            else:
                if terroristattack == True:
                    actionplanDescription = actionplanDescription + "SAF to assess damage on scene and ensure no one enters the affected area until clean up is done.\n"
                    saf=True;
                else:
                    actionplanDescription = actionplanDescription + "SAF to redirect the traffic to ensure no one enters the affected area until clean up is done.\n"
                    saf=True;
        if (rule11) == False:
            actionplanDescription = actionplanDescription + "SPF to help out in what ever is needed but focus more on safety of citizens and any necessary actions until clean up is done. \n"
            spf=True
        #ap = ActionPlan(description=actionplanDescription,
        #                status="Planning",
        #                type="Clean Up",
        #                resolution_time=dt,
        #                projected_casualties=0.0,
        #                crisis_id=crisis_id)

        response_data = {}
        response_data['result'] = 'Create post successful!'
        response_data['description'] = actionplanDescription
        response_data['status'] = "Planning"
        response_data['type'] = "Clean-up"
        response_data['resolution_time'] = dt
        response_data['projected_casualties'] = 0
        response_data['crisis_id'] = crisis_id
        response_data['spf'] = spf
        response_data['scdf'] = scdf
        response_data['saf'] = saf

        return JsonResponse(response_data)