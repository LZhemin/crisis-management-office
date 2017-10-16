from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, Location, ActionPlan, Force, ForceDeployment, EFUpdate

#Kindly help to remove unwanted modules

def index(Request):

    getallcrisis = CrisisReport.objects.order_by('-datetime')[:5]
    context = {'getallcrisis': getallcrisis}
    return render(Request, 'operator/index.html',
                context,
                {'error_message': "You didn't select a Crisis."}
                )

def getCrisisAllocationList(Request):

    getAllocationList = Crisis.objects.all
    context = {'getAllocationList': getAllocationList}
    return render(Request, 'operator/allolist.html',
                  context,
                  {'error_message': "You didn't select a Crisis."}
                  )

def viewCrisis(Request, pk):
    #change = CrisisReport.objects.get(id=pk)
    getallcrisis = CrisisReport.objects.all()
    return render(Request, 'operator/assigncrisis.html', {'getallcrisis':getallcrisis})


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
        return HttpResponseRedirect(reverse('operator/allolist.html'))


def allocateCrisis(request):
    getCrisisList = Crisis.objects.all
    getCrisisTypeList = CrisisType.objects.all
    getAccountList = Account.objects.all
    context = {'getCrisisList': getCrisisList,
               'getCrisisTypeList': getCrisisTypeList,
               'getAccountList': getAccountList}
    #getCrisisList = get_object_or_404(Crisis, pk=crisis_id)

    try:
        #selected_crisis = getCrisisList.objects.all.analyst.get(request.POST['getanalyst'])
        #selected_crisis = getCrisisList.objects.all.crisistypes.get(request.POST['getcrisistype'])
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
        return HttpResponseRedirect(reverse('operator/allolist.html'))





    # latest_crisis_list = Crisis.objects.order_by('-datetime')[:5]
    # # output = ', '.join([l.Location for l in latest_crisis_list])
    # context = {'latest_crisis_list': latest_crisis_list}
    #
    # try:
    #     forCrisis = request.POST['Crisis']
    #     selectedCrisis = Crisis.Crisis.get(forCrisis)
    # except(KeyError, selectedCrisis.DoesNotExist):
    # # Redisplay
    #     return render(request, 'operator/base_site.html', {
    #         context,
    #         {'error_message': "You didn't select a Crisis."}
    #     })
    #
    # else:
    #     crisisList = Crisis(crisis_id=forCrisis)
    #     crisisList.save()  # save to database
    #     return HttpResponseRedirect(reverse('cmoapp:base_site', args=(analyst_id)))


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
        selected_analyst = request.POST['getanalyst']
        selected_crisistype = request.POST['getcrisistype']


    except(KeyError, Crisis.DoesNotExist):
        context = {'getCrisisReportList': getCrisisReportList,
                   'getCrisisTypeList': getCrisisTypeList,
                   'getAccountList': getAccountList}

        return render(request, 'operator/newcrisisrpt.html',
                      context,
                      {'error_message': "You didn't select a Crisis."}
                      )

    else:
        created_crisis = Crisis(analyst=selected_analyst, crisistypes=selected_crisistype)
        created_crisis.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('operator/allolist.html'))