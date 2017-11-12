from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate, Comment
from django.views.generic import ListView,DetailView
from django.core import serializers
from rest_framework import serializers
from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, ActionPlanSerializer, CommentSerializer
#import requests

def index(Request):
    try:

        crisisrep = CrisisReport.objects.all()
        totaldeathCount = 0
        totalinjuryCount = 0
        crisis_list = Crisis.objects.all().exclude(status='Resolved')
        print(crisis_list)
        json_crisis = CrisisSerializer(crisis_list)
        for crisis in crisis_list:
            try:
                totalinjuryCount = totalinjuryCount + crisis.injuries()
                totaldeathCount = totaldeathCount + crisis.deaths()
            except:
                None


    except(KeyError, Crisis.DoesNotExist):

        context = {'all_crisis': False}
    else:
        context = {
            'all_crisis': crisis_list,
            'all_crisisrep': crisisrep,
            'totalinjury': totalinjuryCount,
            'totaldeath': totaldeathCount,
            'json_crisis': CrisisSerializer(Crisis.objects.all(), many=True).data,
        }
        return render(Request, 'map/index.html', context)

