from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment
from django.views.generic import ListView,DetailView
from django.core import serializers
import requests


#Kindly help to remove unwanted modules

def index(Request):
    # UNTIL WE IMPLEMENT SESSIONS WE WILL WORKAROUND WITH SESSION ID = 1
    try:
        crisis = Crisis.objects.all().exclude(status='Resolved')
        forces = Force.objects.all()
        efUpdatesCount = EFUpdate.objects.count()
        forceWidth = int(12/Force.objects.count())
        sideWidth =  int((12-forceWidth*Force.objects.count())/2)

    except(KeyError, Crisis.DoesNotExist):

        context = {'all_crisis': False}
    else:
        context = {
            'all_crisis': crisis,
            'all_force':forces,
            'efUpdateCount': efUpdatesCount,
            'forceWidth':forceWidth,
            'sideWidth':sideWidth
        }
        return render(Request, 'chief/index.html', context)

# Changing the status from here need to add post resolved methods here
def change_status(request):
    try:
        crisis_id = request.POST['id']
        new_status = request.POST['status']
        crisis = Crisis.objects.get(id=crisis_id)
    except(KeyError, crisis.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Error in retrieving efupdates!'})

    crisis.status = new_status;
    crisis.save();

    return JsonResponse({'success': True, 'message': 'Crisis '+crisis_id+'Status Changed to '+new_status})




def get_efupdates_count(request):
    efCount = EFUpdate.objects.count()
    return JsonResponse({'count':efCount}, safe=False)

def get_efupdates(request):
    try:
        startNum = int(request.POST['startNum'])
        efUpdates = EFUpdate.objects.all()[startNum:]
    except(KeyError):
        return JsonResponse({'success':False,'error':'Error in retrieving efupdates!'})
    data = serializers.serialize('json',efUpdates)

    return JsonResponse(data, safe=False)

def forwardActionPlan(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_actionplan_list])
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        COApproval = request.POST['COApproval']
    except(KeyError, COApproval.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a COApproval."},
        })

    else:
        fwActionPlan = ActionPlan(COApproval=COApproval)
        fwActionPlan.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(CrisisID)))


#change to forwarding of ActionPlan Soon
def ApproveActionPlan(request):
    try:
        actionPlanId = request.POST['id']
    except(KeyError):
        return JsonResponse('Error Found in keys!')
    actionPlan = ActionPlan.objects.get(id=actionPlanId)
    actionPlan.status = 'PMORequest'
    actionPlan.save()
    return JsonResponse({"success": True, "message": "Action Plan"+actionPlanId+" Approved Successfully!"})


def RejectActionPlan(request):
    try:
        actionPlanId = request.POST['id']
        comment = request.POST['comment']
        actionPlan = ActionPlan.objects.get(id=actionPlanId)
    except(KeyError, comment.DoesNotExist, actionPlanId.DoesNotExist):
        return JsonResponse({"success":False,"error":"Error Occurred Problems check key names!"})
    else:
        actionPlan.status = 'Rejected'
        commentObj = Comment(text=comment,author='CO',actionPlan_id=actionPlanId)
        commentObj.save()
        actionPlan.save()
        return JsonResponse({"success":True,"message":"Action Plan "+actionPlanId+" Rejected Successfully!"})


def getCrisisList(request):
    latest_crisis_list = Crisis.objects.order_by('-crisis')[:5]
    context = {'latest_crisis_list': latest_crisis_list}

    return render(request, 'chief/base_site.html', {
        context,
    })


def addEFUpdate(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        forActionPlan = request.POST['ActionPlan']
    except(KeyError, ActionPlan.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a ActionPlan."}
        })

    else:
        aEFUpdate = EFUpdate(ActionPlan=forActionPlan)
        EFUpdate.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(CrisisID)))


#Add the LoginRequiredMixin as the leftmost inheritance
class ActionPlanDetail(DetailView):
    context_object_name = "Action_Plan"
    template_name='analyst/actionplan_detail.html'
    model = ActionPlan



def select_crisischat(request):
    #select_id = CrisisID;
    CrisisID= 0;
    selectCrisis = Crisis.objects.filter(pk=CrisisID)

    context = {
        'json_crisis': serializers.serialize('json', selectCrisis)
    }

    return JsonResponse(serializers.serialize('json', selectCrisis), safe=False)



def ReloadTable(request):
    try:
        crisis = Crisis.objects.all().exclude(status='Resolved')
    except(KeyError, crisis.DoesNotExist):
        context = {'all_crisis': False}
    else:
        context = {
            'all_crisis': crisis
        }
        return render(request, 'chief/ui_components/action_plan_table.html', context)

def ReloadCrisis(request):
    try:
        crisis = Crisis.objects.all().exclude(status='Resolved')
    except(KeyError, crisis.DoesNotExist):
        context = {'all_crisis': False}
    else:
        context = {
            'all_crisis': crisis
        }
        return render(request, 'chief/ui_components/all_crisis.html', context)


def sendDeploymentPlan(request,id):
    try:
        ap_id = id
        actionPlan = ActionPlan.objects.get(id=ap_id)
        crisis = actionPlan.crisis
        crisis_reports = CrisisReport.objects.filter(crisis_id=crisis.id)
        forces = actionPlan.forcedeployment_set.all()
    except(KeyError):
        return JsonResponse({"success": False, "error": "Error Occurred Problems check key names!"})
    else:
        location =[]
        category =[]
        deployment =[]
        description = ""
        for report in crisis_reports:
            location.append({"LocationId":report.id, "Lat" : report.latitude,"long": report.longitude,"AOE":report.radius, "category": report.crisisType.name})
            description+=report.description

        for force in forces:
            deployment.append({"ForceType":force.name,"recommended":force.recommended,"maxUtilisation": force.max})

        order_data = {
            "CrisisID":crisis.id,
            "Datetime":timezone.now(),
            "ActionPlanID": actionPlan.id,
            "Location":location,
            "Crisis Description":description,
            "Action Plan Description":actionPlan.description,
            "Deployment":deployment
        }
        #return HttpResponse(timezone.now().strftime("%b. %d, %Y, %I:%M"))
        r = requests.post('url', params=order_data)
        if r.status_code == 200:
            print('Posted Successfully!')
        print('Failure Code:'+r.status_code)