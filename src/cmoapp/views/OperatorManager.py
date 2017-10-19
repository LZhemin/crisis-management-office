from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate
from cmoapp.forms import CrisisForm
from django.forms.models import model_to_dict

import json
#Kindly help to remove unwanted modules

def index(Request):

    #getallcrisis = CrisisReport.objects.order_by('-datetime')[:5]
    #context = {'getallcrisis': getallcrisis}
    # if Request.method == 'GET':
    #
    #     context = {
    #                'all_crisis': Crisis.objects.reverse(),
    #
    #                }
    #     return render(Request, 'operator/index.html',
    #                   context,
    #                   {'error_message': "You didn't select a Crisis."}
    #                   )
    # else:

    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getTypeList = Crisis.objects.all
    getAccountList = Account.objects.filter(type='Analyst')
    getallcrisis = CrisisReport.objects.all()
    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getTypeList': getTypeList,
               'getAccountList': getAccountList,
               'getallcrisis': getallcrisis,

               'all_crisis': Crisis.objects.reverse(),
               'form': CrisisForm()

               }
    return render(Request, 'operator/index.html',
                context,
                {'error_message': "You didn't select a Crisis."}
                )


def create_crisis(request):
    if request.method == 'POST':

        selected_analyst = request.POST.get('getanalyst')
        selected_crisistype = request.POST.get('getcrisistype')
        selected_type = request.POST.get('gettype')
        #selected_crisistype = request.POST["getcrisistype"]
        #selected_filtercrisistype = CrisisType.objects.filter(name='selected_crisistype')
        response_data = {}

        created_crisis = Crisis(analyst_id=selected_analyst, type=selected_type)
        created_crisis.save()
        created_crisis.crisistypes.add(selected_crisistype)

        response_data['result'] = 'Create post successful!'
        response_data['crisispk'] = created_crisis.pk
        response_data['analyst'] = created_crisis.analyst_id
        response_data['crisistypes'] = created_crisis.crisistypes.name
        response_data['type'] = created_crisis.type

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

def getCrisisAllocationList(Request):

    getAllocationList = Crisis.objects.all
    context = {'getAllocationList': getAllocationList}
    return render(Request, 'operator/allolist.html',
                  context,
                  {'error_message': "You didn't select a Crisis."}
                  )

def viewCrisis(Request, pk):

    if Request.method == 'POST':
        selected_analyst = Request.POST.get("analystselection")

        selected_crisistype = Request.POST.get("crisistypeSelection")
        created_crisis = Crisis(analyst_id=selected_analyst, type = 'Ongoing')
        created_crisis.save()
        created_crisis.crisistypes.add(selected_crisistype)
        #crisistypes = models.ManyToManyField(CrisisType)
        #type = models.CharField(max_length=20, choices=TYPES)
        #('Clean-up', 'Clean up'),
        #('Ongoing', 'Ongoing'),
        #('Resolved', 'Resolved')
        #temp = CrisisReport.objects.filter(pk=pky)
        #temp.Crisis = created_crisis.pk
        CrisisReport.objects.filter(pk=pk).update(Crisis = created_crisis.pk)


    getallcrisis = CrisisReport.objects.filter(pk=pk)
    getlocation = Location.objects.first();
    getallanalyst = Account.objects.filter(type='Analyst')
    getallcrisistype = CrisisType.objects.all()
    getallcrisiss = Crisis.objects.all()
    return render(Request, 'operator/assigncrisis.html',
                  {'getallcrisis': getallcrisis, 'getallanalyst': getallanalyst, 'getallcrisistype': getallcrisistype,
                   'getallcrisiss': getallcrisiss, 'getlocation': getlocation})


def allocateToExistingCrisis(request):
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getAccountList = Account.objects.all
    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getAccountList': getAccountList}
    # getCrisisList = get_object_or_404(Crisis, pk=crisis_id)

    try:
        # selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
        # selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
        selected_analyst = request.POST['getanalyst']
        selected_crisistype = request.POST['getcrisistype']


    except(KeyError, Crisis.DoesNotExist):
        context = {'getCrisisList': getCrisisList,
                   'getCrisisTypeList': getCrisisTypeList,
                   'getAccountList': getAccountList}

        return render(request, 'operator/allocrisis.html',
                      context,
                      {'error_message': "You didn't select a Crisis."}
                      )

    else:
        created_crisis = Crisis(analyst=selected_analyst, crisistypes=selected_crisistype)
        created_crisis.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Operator_allocateToExistingCrisis'))


def allocateCrisis(request):
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getAccountList = Account.objects.filter(type = 'Analyst')
    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getAccountList': getAccountList}
    #getCrisisList = get_object_or_404(Crisis, pk=crisis_id)

    try:
        #selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
        #selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
        selected_analyst = request.POST["getanalyst"]
        selected_crisistype = request.POST["getcrisistype"]
        #get all crisis types types
        selected_filtercrisistype = CrisisType.objects.filter(name = selected_crisistype)

    except(KeyError, Crisis.DoesNotExist):
        context = {'getCrisisList': getCrisisList,
                   'getCrisisTypeList': getCrisisTypeList,
                   'getAccountList': getAccountList}

        return render(request, 'operator/allocrisis.html',
                      context,
                      {'error_message': "You didn't select a Crisis."}
                      )

    else:
        created_crisis = Crisis(analyst_id=selected_analyst)
        created_crisis.save()
        created_crisis.crisistypes.add(selected_crisistype)

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Operator_AllocateCrisis'))


def newCrisisReport(request):
    getCrisisReportList = CrisisReport.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getAccountList = Account.objects.all
    context = {'getCrisisReportList': getCrisisReportList,
               'getCrisisTypeList': getCrisisTypeList,
               'getAccountList': getAccountList}
    # getCrisisList = get_object_or_404(Crisis, pk=crisis_id)

    try:
        # selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
        # selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
        selected_crisisname = request.POST['getcrisisname']
        selected_crisisdes = request.POST['getcrisisdes']
        selected_crisislong = request.POST['getcrisislong']
        selected_crisislat = request.POST['getcrisislat']
        selected_crisisdatetime = request.POST['getcrisisdatetime']

    except(KeyError, Crisis.DoesNotExist):
        context = {'getCrisisReportList': getCrisisReportList,
                   'getCrisisTypeList': getCrisisTypeList,
                   'getAccountList': getAccountList}

        return render(request, 'operator/newcrisisrpt.html',
                      context,
                      {'error_message': "You didn't select a Crisis."}
                      )

    else:
        created_crisisrpt = CrisisReport(latitude=selected_crisislat, longitude=selected_crisislong
                                      ,description=selected_crisisdes, datetime=selected_crisisdatetime)
        created_crisisrpt.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('Operator_NewCrisisReport'))