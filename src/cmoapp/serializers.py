from rest_framework import serializers
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Comment, Force, ForceDeployment, EFUpdate
from django.utils import timezone

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
        fields = ('id', 'description', 'status', 'resolutionTime', 'projectedCasualties', 'type', 'crisis')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'timeCreated', 'actionPlan')


    # id = serializers.IntegerField(read_only=True)
    # text = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # author = serializers.CharField(required=True, allow_blank=True, max_length=20)
    # timeCreated = serializers.DateTimeField(default=timezone.now,editable=False)
    # #approval = serializers.BooleanField(required=False)
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Comment` instance, given the validated data.
    #     """
    #     return Comment.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Comment` instance, given the validated data.
    #     """
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.author = validated_data.get('author', instance.author)
    #     instance.timeCreated = validated_data.get('timeCreated', instance.timeCreated)
    #     instance.save()
    #     return instance


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'login', 'password', 'type')


