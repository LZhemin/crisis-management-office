from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict, JsonResponse
from django.urls import reverse
from django.utils import timezone
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Comment, Force, ForceDeployment, EFUpdate

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status,generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from cmoapp.serializers import CrisisSerializer, CrisisReportSerializer, NineOneOneSerializer, EFSerializer, ActionPlanSerializer, CommentSerializer, AuthSerializer, PMOSerializer
from cmoapp.views import ChiefOfficerManager

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


##CrisisReport########################################
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def crisisreport_collection(request):
    if request.method == 'POST':
        serializer = NineOneOneSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    response_data = {}
    response_data['Status'] = 'Failed!' #+ serializer.errors
    response_data['Message'] = 'CrisisReport Not Captured!'

    return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##Comment########################################

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def auth_collection(request):
    if request.method == 'POST':
        #need to change the data.get according
        # getStatus = request.data.query_params('status',None)
        # if getStatus == True:
        #     data = {'id': request.get('getPlanID'),
        #             #'description': request.data.get('getDesp'),
        #             'status': 'Approved',
        #             #'resolutionTime': request.data.get('getResTime'),
        #             #'projectedCasualties': request.data.get('getProCas'),
        #             #'type': request.data.get('getType'),
        #             #'crisis': request.data.get('getCrisisID'),
        #             }
        #    # fields = ('id', 'description', 'status', 'resolutionTime', 'projectedCasualties', 'type', 'crisis')
        #
        # elif getStatus == False:
        #     data = {'id': request.data.get('getPlanID'),
        #             #'description': request.data.get('getDesp'),
        #             'status': 'Rejected',
        #             ##'resolutionTime': request.data.get('getResTime'),
        #             #'projectedCasualties': request.data.get('getProCas'),
        #             #'type': request.data.get('getType'),
        #             #'crisis': request.data.get('getCrisisID'),
        #             }
        #     data2 = {'text': request.data.get('getPMOComments'),
        #             'author' : 'PMO',
        #             'timeCreated': timezone.now,
        #             'actionPlan': data.id,
        #             }
            #fields = ('id', 'text', 'author', 'timeCreated', 'actionPlan')

        #serializer = ActionPlanSerializer(data=request.data)#data=request.data
        #serializer2 = CommentSerializer(data=request.data,many=True)
        serializer = AuthSerializer(data=request.data)
        response_data = {}

        if serializer.is_valid(): #and serializer2.is_valid():
            #serializer.validated_data
            #datatest = JSONRenderer().render(serializer.validated_data)
            #datatryout = json.loads(datatest)
            serializer.save()
            if(serializer.data['approval'] == True):
                ChiefOfficerManager.sendDeploymentPlan(serializer.data['id'])
            response_data['Status'] = 'Success!'
            response_data['Message'] = 'Approval Captured!'
            return Response(response_data, status=status.HTTP_200_OK)

        response_data['Status'] = 'Failed!'
        response_data['Message'] = 'Approval Not Captured!'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


##PMO########################################

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def PMO_collection(request,status=None):
    print(status)
    if request.method == 'GET':
        if(status):
            crisis_list = Crisis.objects.filter(status=status)
        else:
            crisis_list = Crisis.objects.all()
        serializer = PMOSerializer(crisis_list, many=True)
        return Response(serializer.data)

    #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##EF########################################

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def EF_collection(request):

    serializer = EFSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)