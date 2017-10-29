from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment
from django.views.generic import ListView,DetailView
from django.core import serializers


#Kindly help to remove unwanted modules

def index(Request):
    # UNTIL WE IMPLEMENT SESSIONS WE WILL WORKAROUND WITH SESSION ID = 1
    try:
        crisis = Crisis.objects.all().exclude(status='Resolved')
        forces = Force.objects.all();
    except(KeyError, Crisis.DoesNotExist):
        context = {'all_crisis': False}
    else:
        context = {
            'all_crisis': crisis,
            'all_force':forces,
            'json_crisis': serializers.serialize('json', crisis)
        }

    return render(Request, 'chief/index.html', context)


def sendDeployment(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_actionplan_list])
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        Name = request.POST['name']
    except(KeyError, Name.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a name.",
        }})

    try:
        Recommended = request.POST['recommended']
    except(KeyError, Recommended.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a recommended."},
        })

    try:
        Max = request.POST['max']
    except(KeyError, max.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a max."}
        })
    else:
        deployment = ForceDeployment(name=Name, recommanded=Recommended, max=Max)
        deployment.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(CrisisID)))


def rejectActionPlan(request, CrisisID):
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
    return JsonResponse({"success": True, "message": "Action Plan Approved Successfully!"})


def RejectActionPlan(request):
    try:
        actionPlanId = request.POST['id']
        comment = request.POST['comment']
    except(KeyError):
        return JsonResponse({"success":False,"error":"Error Occurred Problems check key names!"})
    else:
        actionPlan = ActionPlan.objects.get(id=actionPlanId)
        actionPlan.status = 'Rejected'
        commentObj = Comment(text=comment,author='CO',actionPlan_id=actionPlanId)
        commentObj.save()
        return JsonResponse({"success":True,"message":"Action Plan Rejected Successfully!"})


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



def ReloadData(request):

    if request.method == 'GET':

        unresolvedCrisis = Crisis.objects.all().exclude(status='Resolved')

        response = serializers.serialize("json", unresolvedCrisis)
        return HttpResponse(response, content_type='application/json')
    else:
        return JsonResponse(0)