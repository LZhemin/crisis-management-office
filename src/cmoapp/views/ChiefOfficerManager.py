from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate

#Kindly help to remove unwanted modules
sessionId = 2

def index(Request):
    # UNTIL WE IMPLEMENT SESSIONS WE WILL WORKAROUND WITH SESSION ID = 1
    try:
        assigned_crisis = Crisis.objects.get(analyst__id=sessionId)
        #crisis_reports = CrisisReport.objects.filter(crisis_id=assigned_crisis.id).select_related('crisisType')
        crisis_reports = CrisisReport.objects.filter().select_related('crisisType')
    except(KeyError, Crisis.DoesNotExist):
        context = {'assigned_crisis': False}
    else:
        context = {
            'assigned_crisis': assigned_crisis,
            'crisis_reports': crisis_reports
        }

    return render(Request, 'chief/index.html', context)

def sendDeployment(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_actionplan_list])
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        Name = request.POST['name']
    except(KeyError, name.DoesNotExist):
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


def setApprovalStatus(request, CrisisID):
    latest_actionplan_list = ActionPlan.objects.order_by('-crisis')[:5]
    # output = ', '.join([l.Location for l in latest_actionplan_list])
    context = {'latest_actionplan_list': latest_actionplan_list}

    try:
        COApproval = request.POST['COApproval']
    except(KeyError, COApproval.DoesNotExist):
    # Redisplay
        return render(request, 'chief/base_site.html', {
            context,
            {'error_message': "You didn't select a COApproval."}
        })

    else:
        setActionPlan = ActionPlan(COApproval=COApproval)
        setActionPlan.add()  # save to database
        return HttpResponseRedirect(reverse('cmoapp:base_site', args=(CrisisID)))


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