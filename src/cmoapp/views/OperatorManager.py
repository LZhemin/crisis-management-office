from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate
from django.forms.models import model_to_dict
from django.core import serializers
from cmoapp.serializers import CrisisReportSerializer

import json
#Kindly help to remove unwanted modules


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

    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getCrisisReportList': getCrisisReportList,
               'getUnassignedCrisisReport': getUnassignedCrisisReport,
               'getAccountList': getAccountList,
               'getNotResolvedCrisisList': getNotResolvedCrisisList,
               'getAssignedCrisisReport':getAssignedCrisisReport,
               'all_crisis': Crisis.objects.reverse(),
               'all_crisisreport': CrisisReport.objects.reverse(),
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
        entered_title = Request.POST.get("crisistitle")
        created_crisis = Crisis(crisis_title = entered_title,analyst_id=pk, status='Ongoing')
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
        entered_title = request.POST.get('crisistitlename')

        created_crisis = Crisis(crisis_title = entered_title, analyst_id=selected_analyst, status='Ongoing')
        created_crisis.save()
        CrisisReport.objects.filter(pk=selected_reportID).update(crisis=created_crisis.pk, crisisType=selected_crisis)

        #created_crisis = Crisis(pk = selected_crisis, analyst_id=selected_analyst, status = 'Ongoing')#status=selected_status
        #created_crisis.save()
        response_data = {}
        response_data['result'] = 'Create post successful!'
        response_data['crisispk'] = created_crisis.pk
        response_data['analyst'] = created_crisis.analyst_id
        response_data['crisisreportid'] = selected_reportID

        return JsonResponse(response_data)
    else:
        return JsonResponse(model_to_dict(0))


def assignexisting(request):
    if request.method == 'POST':

        selected_crisis = request.POST.get('getExisting')
        selected_reportID = request.POST.get('existingreportid')
        selected_crisistype = request.POST.get('getcrisistype2')


        #selected_type = CrisisReport.objects.filter(crisis_id = selected_crisis).values_list('crisisType_id', flat=True)
        #getassignexisting = CrisisReport.objects.filter(pk=selected_reportID).update(crisis=selected_crisis, crisisType=selected_type[0])
        CrisisReport.objects.filter(pk=selected_reportID).update(crisis=selected_crisis, crisisType=selected_crisistype)
        response_data = {}
        response_data['result'] = 'Create post successful!'
        response_data['existingreportid'] = selected_reportID
        return JsonResponse(response_data)
    else:
        #return HttpResponse(
         #   json.dumps({"nothing to see": "this isn't happening"}),
          #  content_type="application/json"
        #)
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

