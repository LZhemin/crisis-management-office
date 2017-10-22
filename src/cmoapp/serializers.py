from rest_framework import serializers
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate


class CrisisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crisis
        fields = ('id', 'analyst', 'status')


class CrisisReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrisisReport
        fields = ('id', 'description', 'datetime', 'latitude', 'longitude', 'radius', 'crisis', 'crisisType')


class ActionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionPlan
        fields = ('id', 'description', 'status', 'COComments', 'PMOComments', 'resolutionTime', 'projectedCasualties', 'type', 'crisis')
