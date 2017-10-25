from rest_framework import serializers
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Force, ForceDeployment, EFUpdate


class CrisisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crisis
        fields = ('id', 'analyst', 'status')


class CrisisReportSerializer(serializers.ModelSerializer):
    # crisisType = serializers.SlugRelatedField(
    #     queryset=CrisisType.objects.all(), slug_field='selectCrisisType'
    # )

    class Meta:
        model = CrisisReport
        fields = ('id', 'description', 'datetime', 'latitude', 'longitude', 'radius', 'crisis', 'crisisType')


class ActionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionPlan
        fields = ('id', 'description', 'status', 'COComments', 'PMOComments', 'resolutionTime', 'projectedCasualties', 'type', 'crisis')

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'login', 'password', 'type')
