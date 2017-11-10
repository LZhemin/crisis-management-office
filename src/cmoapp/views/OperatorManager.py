from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Notifications
from django.forms.models import model_to_dict
from django.core import serializers
from cmoapp.serializers import CrisisReportSerializer, NotificationSerializer

import json
#Kindly help to remove unwanted modules

sessionId = 3


def sharedindex():
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getCrisisReportList = CrisisReport.objects.all
    getUnassignedCrisisReport = CrisisReport.objects.filter(crisis__isnull=True).order_by('datetime')
    getResolvedCrisis = Crisis.objects.exclude(status='Resolved').values_list('pk', flat=True)
    getAssignedCrisisReport = CrisisReport.objects.exclude(crisis__isnull=True).filter(crisis__in = getResolvedCrisis)
    getNotResolvedCrisisList = Crisis.objects.filter(analyst__isnull=False).exclude(status='Resolved')
    getanalystacc = Crisis.objects.exclude(analyst__isnull = True).values_list('analyst_id', flat=True)
    getAccountList = Account.objects.filter(type="Analyst").exclude(pk__in=getanalystacc)
    notifications = Notifications.objects.filter(_for=sessionId).exclude(new=0)
    notification_count = notifications.count()

    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getCrisisReportList': getCrisisReportList,
               'getUnassignedCrisisReport': getUnassignedCrisisReport,
               'getAccountList': getAccountList,
               'getNotResolvedCrisisList': getNotResolvedCrisisList,
               'getAssignedCrisisReport':getAssignedCrisisReport,
               'all_crisis': Crisis.objects.reverse(),
               'all_crisisreport': CrisisReport.objects.reverse(),
               'notifications': notifications,
               'notification_count': notification_count
               }
    return context

def index(Request):

    context = sharedindex();
    return render(Request, 'operator/index.html',
                context,
                {'error_message': "You didn't select a Crisis."}
                )

def getallassignedCrisisReport(Request):
    if Request.method == 'GET':

        getResolvedCrisis = Crisis.objects.exclude(status='Resolved')
        getAssignedCrisisReport = CrisisReport.objects.exclude(crisis__isnull=True).filter(crisis__in=getResolvedCrisis)
        #getCrisisReportList = CrisisReport.objects.all()
        #crisisType = serializers.SlugRelatedField(queryset=CrisisType.objects.all(), slug_field='name')
        #response = serializers.serialize("json", getAssignedCrisisReport)
        #return HttpResponse(response, content_type='application/json')
        serializer = CrisisReportSerializer(getAssignedCrisisReport, many=True)
        return JsonResponse(serializer.data, safe=False)
        #serializer = CrisisReportSerializer(getAssignedCrisisReport, many=True)
        #return Response(serializer.data)
    else:
      return JsonResponse(model_to_dict(0))


def assignnewCrisis(Request, pk):
    if Request.method == 'POST':
        #selected_analyst = Request.POST.get("analystselection")
        selected_crisistype = Request.POST.get("crisistypeT")
        created_crisis = Crisis(analyst_id=pk, status='Ongoing')
        created_crisis.save()

        selectedCrisis= Request.POST.getlist('crisisSelector')

        for sc in selectedCrisis:
            CrisisReport.objects.filter(pk=sc).update(crisis=created_crisis.pk, crisisType=selected_crisistype)

        context = sharedindex();
        return HttpResponseRedirect(reverse('Operator_Index'))

    getallcrisis = CrisisReport.objects.filter(crisis__isnull = True)
    #getallanalyst = Account.objects.filter(pk=pk)
    #getanalystacc = Crisis.objects.exclude(analyst__isnull = True).values_list('analyst_id', flat=True)
    #getallanalyst = Account.objects.exclude(pk__in = getanalystacc).filter(type = "Analyst")

    getallcrisistype = CrisisType.objects.all()

    return render(Request, 'operator/assigncrisis.html',
                  {'getallcrisis': getallcrisis, 'getallcrisistype': getallcrisistype,
                   })


def create_crisis(request):
    if request.method == 'POST':

        selected_crisis = request.POST.get('getcrisistype')
        selected_analyst = request.POST.get('getanalyst')
        selected_reportID = request.POST.get('crisisreportid')
        #selected_status = request.POST.get('getstatus')
        #selected_crisistype = request.POST["getcrisistype"]
        #selected_filtercrisistype = CrisisType.objects.filter(name='selected_crisistype')
        response_data = {}

        created_crisis = Crisis(analyst_id=selected_analyst, status='Ongoing')
        created_crisis.save()
        CrisisReport.objects.filter(pk=selected_reportID).update(crisis=created_crisis.pk, crisisType=selected_crisis)

        #created_crisis = Crisis(pk = selected_crisis, analyst_id=selected_analyst, status = 'Ongoing')#status=selected_status
        #created_crisis.save()

        response_data['result'] = 'Create post successful!'
        response_data['crisispk'] = created_crisis.pk
        response_data['analyst'] = created_crisis.analyst_id
        #response_data['status'] = created_crisis.status

        #return HttpResponse(
         #   json.dumps(response_data),
         #   content_type="application/json"
        #)
        #obj = Place.objects.get(id=object_id)
        return JsonResponse(response_data)
    else:
        #return HttpResponse(
         #   json.dumps({"nothing to see": "this isn't happening"}),
          #  content_type="application/json"
        #)
        return JsonResponse(model_to_dict(0))




def assignexisting(request):
    if request.method == 'POST':

        selected_crisis = request.POST.get('getExisting')
        selected_reportID = request.POST.get('existingreportid')
        response_data = {}

        selected_type = CrisisReport.objects.filter(crisis_id = selected_crisis).values_list('crisisType_id', flat=True)
        CrisisReport.objects.filter(pk=selected_reportID).update(crisis=selected_crisis, crisisType=selected_type[0])

        response_data['result'] = 'Create post successful!'
        return JsonResponse(response_data)
    else:
        #return HttpResponse(
         #   json.dumps({"nothing to see": "this isn't happening"}),
          #  content_type="application/json"
        #)
        return JsonResponse(model_to_dict(0))


def delete_crisis(request):

    if request.method == 'DELETE':

        selected_crisis = Crisis.objects.get(pk=int(QueryDict(request.body).get('crisispk')))

        selected_crisis.delete()

        response_data = {}
        response_data['msg'] = 'Crisis was deleted.'

        return JsonResponse(response_data)
    else:
        return JsonResponse(model_to_dict(0))


def load_crisis(request):
    if request.method == 'GET':

        getcrisisacc = CrisisReport.objects.filter(crisis__isnull=False)
        getUnassignedCrisis = Crisis.objects.all().exclude(pk__in=getcrisisacc)

        response = serializers.serialize("json", getUnassignedCrisis)
        return HttpResponse(response, content_type='application/json')
    else:
       return JsonResponse(model_to_dict(0))

def load_analyst(request):

    if request.method == 'GET':

        getanalystacc = Crisis.objects.exclude(analyst__isnull=True).values_list('analyst_id', flat=True)
        getAccountList = Account.objects.exclude(pk__in=getanalystacc).filter(type="Analyst")
        #getAccountList = Account.objects.all()
        response = serializers.serialize("json", getAccountList)
        return HttpResponse(response, content_type='application/json')
    else:
      return JsonResponse(model_to_dict(0))

def get_crisisreport_collection(request):
    # crisisreports = CrisisReport.objects.all()
    crisisreports = CrisisReport.objects.filter(crisis__isnull=True).order_by('datetime')
    serializer = CrisisReportSerializer(crisisreports, many=True)
    return JsonResponse(serializer.data,safe=False)


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
