from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate
from cmoapp.forms import CrisisForm
from django.forms.models import model_to_dict
from django.core import serializers

import json
#Kindly help to remove unwanted modules


def sharedindex():
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getCrisisReportList = CrisisReport.objects.all
    getUnassignedCrisisReport = CrisisReport.objects.filter(crisis__isnull=True).order_by('datetime')

    getResolvedCrisis = Crisis.objects.exclude(status='Resolved').values_list('pk', flat=True)
    getAssignedCrisisReport = CrisisReport.objects.exclude(crisis__isnull=True).filter(crisis__in = getResolvedCrisis)

    #getanalystacc = Crisis.objects.filter(analyst__isnull=False)
    #getAccountList = Account.objects.exclude(pk__in=getanalystacc).filter(type="Analyst")

    getcrisisacc = CrisisReport.objects.filter(crisis__isnull=False)
    getUnassignedCrisis = Crisis.objects.all().exclude(pk__in=getcrisisacc)

    getanalystacc = Crisis.objects.exclude(analyst__isnull=True).values_list('analyst_id', flat=True)
    getAccountList = Account.objects.exclude(pk__in=getanalystacc).filter(type="Analyst")



    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getCrisisReportList': getCrisisReportList,
               'getUnassignedCrisisReport': getUnassignedCrisisReport,
               'getAccountList': getAccountList,
               'getUnassignedCrisis': getUnassignedCrisis,
                'getAssignedCrisisReport':getAssignedCrisisReport,
               'all_crisis': Crisis.objects.reverse(),
               'all_crisisreport': CrisisReport.objects.reverse(),
               'form': CrisisForm()
               }
    return context

def index(Request):

    context = sharedindex();
    return render(Request, 'operator/index.html',
                context,
                {'error_message': "You didn't select a Crisis."}
                )



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

    getallcrisis = CrisisReport.objects.filter(pk=pk)
    getanalystacc = Crisis.objects.exclude(analyst__isnull=True).values_list('analyst_id', flat=True)
    getallanalyst = Account.objects.exclude(pk__in = getanalystacc).filter(type = "Analyst")


    getallcrisistype = CrisisType.objects.all()

    return render(Request, 'operator/assigncrisis.html',
                  {'getallcrisis': getallcrisis, 'getallcrisistype': getallcrisistype,
                   })


def create_crisis(request):
    if request.method == 'POST':

        selected_crisis = request.POST.get('getcrisis')
        selected_analyst = request.POST.get('getanalyst')
        #selected_status = request.POST.get('getstatus')
        #selected_crisistype = request.POST["getcrisistype"]
        #selected_filtercrisistype = CrisisType.objects.filter(name='selected_crisistype')
        response_data = {}

        created_crisis = Crisis(pk = selected_crisis, analyst_id=selected_analyst, status = 'Ongoing')#status=selected_status
        created_crisis.save()

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

        response = serializers.serialize("json", getAccountList)
        return HttpResponse(response, content_type='application/json')
    else:
      return JsonResponse(model_to_dict(0))


