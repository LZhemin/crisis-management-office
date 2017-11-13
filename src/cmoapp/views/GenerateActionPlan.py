from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate
from django.db.models import Case, Value, When
import datetime
from datetime import timedelta

def index(Request):

    getCrisis = CrisisReport.objects.all()

    findCrisis = Crisis.objects.filter(pk=1)
    findCrisisReport = CrisisReport.objects.filter(crisis=findCrisis)
    context = {'getCrisis': getCrisis,
               'findCrisis': findCrisis,
               'findCrisisReport': findCrisisReport
               }
    generateActionPlan(Request, findCrisis);
    return render(Request, 'ActionPlan/index.html',
                  context,
                {'error_message': "You didn't select a Crisis."}
                )

def generateActionPlan(Request, recCrisis):

    dt = datetime.timedelta(days=0, hours=0)
    option = 0
    findCrisisReport = CrisisReport.objects.filter(crisis=recCrisis)

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

    actionplanDescription = ""
    for report in findCrisisReport.all():
        if (report.radius > 199):
            rule7 = False
            rule8 = False
            rule9 = False
            rule10 = False
            rule11 = False
        if (report.crisisType.name == 'Terrorist Attack'):
            rule3 = False
            rule4 = False
            rule5 = False
            rule6 = False
            rule8 = False
            rule9 = False
            rule10 = False
            rule11 = False
        if (report.crisisType.name == 'Large Fires'):
            rule4 = False
            rule5 = False
            rule6 = False
            rule9 = False
            rule10 = False
            rule11 = False
        if (report.crisisType.name == 'Natural Disasters'):
            rule6 = False
        if (report.crisisType.name == 'Pandemics'):
            rule5 = False
            rule10 = False
            rule11 = False
        if (report.crisisType.name == 'Riots/Mass Looting'):
            rule2 = False
            rule3 = False
            rule4 = False
            rule5 = False
            rule6 = False
            rule11 = False
        if(report.radius > 199) and (report.crisisType.name == 'Riots/Mass Looting'):
            rule1 = True

    if (rule5 or rule10 or rule11) == False:
        actionplanDescription= actionplanDescription + "Cordon\n"
    if rule1:
        actionplanDescription= actionplanDescription + "Curfew\n"
        actionplanDescription= actionplanDescription + "Public Advisory\n"
        actionplanDescription= actionplanDescription + "SCDF Deployment\n"
        scdf = True
    if (rule7 or rule8 or rule9 or rule10 or rule11)== False:
        actionplanDescription= actionplanDescription + "SAF Deployment\n"
        saf = True
    if (rule11) == False:
        actionplanDescription= actionplanDescription + "SPF Deployment\n"
        spf = True
    #findActionPlan = ActionPlan(description=actionplanDescription,
    #                            status="Planning",
    #                            type="Combat",
    #                            resolutionTime=dt,
    #                            projectedCasualties=0.0,
    #                            crisis_id=1)
    #findActionPlan.save()
