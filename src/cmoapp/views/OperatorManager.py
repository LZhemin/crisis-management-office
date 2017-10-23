from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate
from cmoapp.forms import CrisisForm
from django.forms.models import model_to_dict

import json
#Kindly help to remove unwanted modules


def sharedindex():
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getCrisisReportList = CrisisReport.objects.all
    getUnassignedCrisisReport = CrisisReport.objects.filter(crisis__isnull=True).order_by('datetime')

    #getanalystacc = Crisis.objects.filter(analyst__isnull=False)
    #getAccountList = Account.objects.exclude(pk__in=getanalystacc).filter(type="Analyst")

    getcrisisacc = CrisisReport.objects.filter(crisis__isnull=False)
    getUnassignedCrisis = Crisis.objects.all().exclude(pk__in=getcrisisacc)

    getanalystacc = Crisis.objects.all().values_list('analyst_id', flat=True)
    getAccountList = Account.objects.exclude(pk__in=getanalystacc).filter(type="Analyst")

    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getCrisisReportList': getCrisisReportList,
               'getUnassignedCrisisReport': getUnassignedCrisisReport,
               'getAccountList': getAccountList,
               'getUnassignedCrisis': getUnassignedCrisis,

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
        selected_analyst = Request.POST.get("analystselection")
        # hiddenid = Request.POST.get("hiddenid")
        # selected_crisistype = Request.POST.getlist("crisistypeT")
        selected_crisistype = Request.POST.get("crisistypeT")
        created_crisis = Crisis(analyst_id=selected_analyst, status='Ongoing')
        created_crisis.save()

        CrisisReport.objects.filter(pk=pk).update(crisis=created_crisis.pk, crisisType=selected_crisistype)
        context = sharedindex();
        return HttpResponseRedirect(reverse('Operator_Index'))

    getallcrisis = CrisisReport.objects.filter(pk=pk)
    getanalystacc = Crisis.objects.all().values_list('analyst_id', flat=True)
    getallanalyst = Account.objects.exclude(pk__in = getanalystacc).filter(type = "Analyst")

    getallcrisistype = CrisisType.objects.all()

    return render(Request, 'operator/assigncrisis.html',
                  {'getallcrisis': getallcrisis, 'getallanalyst': getallanalyst, 'getallcrisistype': getallcrisistype,
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







# def getCrisisAllocationList(Request):
#
#     getAllocationList = Crisis.objects.all
#     context = {'getAllocationList': getAllocationList}
#     return render(Request, 'operator/allolist.html',
#                   context,
#                   {'error_message': "You didn't select a Crisis."}
#                   )
#
#
#
# def allocateToExistingCrisis(request):
#     getCrisisList = Crisis.objects.all
#     getCrisisTypeList = CrisisType.objects.all
#     getAccountList = Account.objects.all
#     context = {'getCrisisList': getCrisisList,
#                'getCrisisTypeList': getCrisisTypeList,
#                'getAccountList': getAccountList}
#     # getCrisisList = get_object_or_404(Crisis, pk=crisis_id)
#
#     try:
#         # selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
#         # selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
#         selected_analyst = request.POST['getanalyst']
#         selected_crisistype = request.POST['getcrisistype']
#
#
#     except(KeyError, Crisis.DoesNotExist):
#         context = {'getCrisisList': getCrisisList,
#                    'getCrisisTypeList': getCrisisTypeList,
#                    'getAccountList': getAccountList}
#
#         return render(request, 'operator/allocrisis.html',
#                       context,
#                       {'error_message': "You didn't select a Crisis."}
#                       )
#
#     else:
#         created_crisis = Crisis(analyst=selected_analyst, crisistypes=selected_crisistype)
#         created_crisis.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('Operator_allocateToExistingCrisis'))
#
#
# def allocateCrisis(request):
#     getCrisisList = Crisis.objects.all
#     getCrisisTypeList = CrisisType.objects.all
#     getAccountList = Account.objects.filter(type = 'Analyst')
#     context = {'getCrisisList': getCrisisList,
#                'getCrisisTypeList': getCrisisTypeList,
#                'getAccountList': getAccountList}
#     #getCrisisList = get_object_or_404(Crisis, pk=crisis_id)
#
#     try:
#         #selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
#         #selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
#         selected_analyst = request.POST["getanalyst"]
#         selected_crisistype = request.POST["getcrisistype"]
#         #get all crisis types types
#         selected_filtercrisistype = CrisisType.objects.filter(name = selected_crisistype)
#
#     except(KeyError, Crisis.DoesNotExist):
#         context = {'getCrisisList': getCrisisList,
#                    'getCrisisTypeList': getCrisisTypeList,
#                    'getAccountList': getAccountList}
#
#         return render(request, 'operator/allocrisis.html',
#                       context,
#                       {'error_message': "You didn't select a Crisis."}
#                       )
#
#     else:
#         created_crisis = Crisis(analyst_id=selected_analyst)
#         created_crisis.save()
#         created_crisis.crisistypes.add(selected_crisistype)
#
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('Operator_AllocateCrisis'))
#
#
# def newCrisisReport(request):
#     getCrisisReportList = CrisisReport.objects.all
#     getCrisisTypeList = CrisisType.objects.all
#     getAccountList = Account.objects.all
#     context = {'getCrisisReportList': getCrisisReportList,
#                'getCrisisTypeList': getCrisisTypeList,
#                'getAccountList': getAccountList}
#     # getCrisisList = get_object_or_404(Crisis, pk=crisis_id)
#
#     try:
#         # selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
#         # selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
#         selected_crisisname = request.POST['getcrisisname']
#         selected_crisisdes = request.POST['getcrisisdes']
#         selected_crisislong = request.POST['getcrisislong']
#         selected_crisislat = request.POST['getcrisislat']
#         selected_crisisdatetime = request.POST['getcrisisdatetime']
#
#     except(KeyError, Crisis.DoesNotExist):
#         context = {'getCrisisReportList': getCrisisReportList,
#                    'getCrisisTypeList': getCrisisTypeList,
#                    'getAccountList': getAccountList}
#
#         return render(request, 'operator/newcrisisrpt.html',
#                       context,
#                       {'error_message': "You didn't select a Crisis."}
#                       )
#
#     else:
#         created_crisisrpt = CrisisReport(latitude=selected_crisislat, longitude=selected_crisislong
#                                       ,description=selected_crisisdes, datetime=selected_crisisdatetime)
#         created_crisisrpt.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('Operator_NewCrisisReport'))