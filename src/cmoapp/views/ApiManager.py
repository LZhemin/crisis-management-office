from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status,generics
from rest_framework.response import Response

from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, ActionPlanSerializer

import json
#Kindly help to remove unwanted modules


### class based views ###
#Are we using generics???
#Crisis
# class CrisisCollection(generics.ListCreateAPIView):
#     queryset = Crisis.objects.all()
#     serializer_class = CrisisSerializer
#
# class CrisisMember(generics.RetrieveDestroyAPIView):
#     queryset = Crisis.objects.all()
#     serializer_class = CrisisSerializer
#
# #CrisisReport
# class CrisisReportCollection(generics.ListCreateAPIView):
#     queryset = CrisisReport.objects.all()
#     serializer_class = CrisisReportSerializer
#
# class CrisisReportMember(generics.RetrieveDestroyAPIView):
#     queryset = CrisisReport.objects.all()
#     serializer_class = CrisisReportSerializer
#
# #ActionPlan
# class ActionPlanCollection(generics.ListCreateAPIView):
#     queryset = ActionPlan.objects.all()
#     serializer_class = ActionPlanSerializer
#
# class ActionPlanMember(generics.RetrieveDestroyAPIView):
#     queryset = ActionPlan.objects.all()
#     serializer_class = ActionPlanSerializer


###Else the function based view###

##Crisis########################################
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def crisis_collection(request):
    if request.method == 'GET':
        crisiss = Crisis.objects.all()
        serializer = CrisisSerializer(crisiss, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        #need to change the data.get according
        data = {'getcrisis': request.DATA.get('getcrisis'),
                'getanalyst': request.DATA.get('getanalyst'),
                'getstatus': request.DATA.get('getstatus')
                }
        serializer = CrisisSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def crisis_element(request, pk):
    crisis = get_object_or_404(Crisis, id=pk)
    # try:
    #     crisis = Crisis.objects.get(pk=pk)
    # except Crisis.DoesNotExist:
    #     return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CrisisReportSerializer(crisis)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        crisis.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


##CrisisReport########################################
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def crisisreport_collection(request):
    if request.method == 'GET':
        crisisreports = CrisisReport.objects.all()
        serializer = CrisisReportSerializer(crisisreports, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        #need to change the data.get according
        data = {'getcrisisreport': request.DATA.get('getcrisisreport'),
                'getdescription': request.DATA.get('getdescription'),
                'getdatetime': request.DATA.get('getdatetime'),
                'getlatitude': request.DATA.get('getlatitude'),
                'getlongitude': request.DATA.get('getlongitude'),
                'getradius': request.DATA.get('getradius'),
                'getcrisis': request.DATA.get('getcrisis'),
                'getcrisisType': request.DATA.get('getcrisisType')
                }

        serializer = CrisisReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def crisisreport_element(request, pk):
    crisisreport = get_object_or_404(CrisisReport, id=pk)
    # try:
    #     crisisreport = CrisisReport.objects.get(pk=pk)
    # except CrisisReport.DoesNotExist:
    #     return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CrisisReportSerializer(crisisreport)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        crisisreport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


##ActionPlan########################################

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def actionplan_collection(request):
    if request.method == 'GET':
        actionplans = ActionPlan.objects.all()
        serializer = ActionPlanSerializer(actionplans, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        #need to change the data.get according
        data = {'getactionplan': request.DATA.get('getactionplan'),
                'getdescription': request.DATA.get('getdescription'),
                'getstatus': request.DATA.get('getstatus'),
                'getCOComments': request.DATA.get('getCOComments'),
                'getPMOComments': request.DATA.get('getPMOComments'),
                'getresolutionTime': request.DATA.get('getresolutionTime'),
                'getprojectedCasualties': request.DATA.get('getprojectedCasualties'),
                'gettype': request.DATA.get('gettype'),
                'getcrisis': request.DATA.get('getcrisis')
                }

        serializer = ActionPlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def actionplan_element(request, pk):
    actionplan = get_object_or_404(ActionPlan, id=pk)
    # try:
    #     actionplan = ActionPlan.objects.get(pk=pk)
    # except ActionPlan.DoesNotExist:
    #     return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CrisisReportSerializer(actionplan)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        actionplan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


