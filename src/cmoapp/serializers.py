from rest_framework import serializers
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Comment, Force, ForceDeployment, EFUpdate, ForceUtilization
from django.utils import timezone

class CrisisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crisis
        fields = ('id', 'analyst', 'status')

#This serializer is for retrieval
class CrisisReportSerializer(serializers.ModelSerializer):
    crisisType = serializers.SlugRelatedField(queryset=CrisisType.objects.all(), slug_field='name').allow_null

    class Meta:
        model = CrisisReport
        fields = ('id', 'description', 'datetime', 'latitude', 'longitude', 'radius', 'crisis', 'crisisType')

#This serializer is for serializing
class NineOneOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisReport
        fields = ('description', 'datetime', 'latitude', 'longitude', 'radius')


class ActionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionPlan
        fields = ('id', 'description', 'status', 'resolution_time', 'projected_casualties', 'type', 'crisis')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'timeCreated', 'actionPlan')



class AuthSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    approval = serializers.BooleanField(required=True)

    def validate(self, attrs):
        #validate id exists
        id = attrs.get('id')
        text = attrs.get('text')
        # ap = ActionPlan.objects.get(id=id)
        # if ap.status == 'Rejected' and text :

        if ActionPlan.objects.get(pk=id) == True:
            raise serializers.ValidationError('ID already exists')
        elif not text or text == '':
            raise serializers.ValidationError('Comment not exists')
        elif ActionPlan.objects.get(pk=id) == False:
            return attrs;

        return attrs;

    def save(self):
        #ap = ActionPlan.objects.get(pk = self.validated_data['id'])
        #ap = ActionPlan.objects.get(self.data['id'])
        #ap.id = self.validated_data['id']
        aid = self.validated_data['id']
        ap = ActionPlan.objects.get(id = aid)
        if self.validated_data['approval'] == True:
            ap.status = 'Approved'
        else:
            ap.status = 'Rejected'
        ap.save()
        if self.validated_data['text'] and self.validated_data['approval'] == False:
            #c =  Comment.objects.
            #c.text
            text = self.validated_data['text']
            author = 'PMO'
            timeCreated = timezone.now()
            actionPlan = aid
            Comment.objects.create(text=text,author=author,timeCreated=timeCreated,actionPlan=ap)

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


class PMOSerializer(serializers.ModelSerializer):

    class IReportSerializer(serializers.ModelSerializer):

        crisisType = serializers.SlugRelatedField(queryset=CrisisType.objects.all(), slug_field='name')
        class Meta:
            model = CrisisReport
            fields = ('id', 'description', 'datetime', 'latitude', 'longitude', 'radius', 'crisisType')

    class IEFUpdateSerializer(serializers.ModelSerializer):

        class Meta:
            model = EFUpdate
            fields = ('datetime', 'affectedRadius', 'totalInjured', 'totalDeaths', 'duration', 'description')

    class IActionPlanSerializer(serializers.ModelSerializer):

        class Meta:
            model = ActionPlan
            fields = ('id', 'plan_number', 'description', 'status', 'resolution_time', 'projected_casualties', 'type')

    crisisreport_set = IReportSerializer(many=True, read_only=True)
    actionplan_set = serializers.SerializerMethodField('get_filtered_plans')
    efupdate_set = IEFUpdateSerializer(many=True, read_only=True)

    #Filter out "Planning', or in 'CORequest'
    #Show 'Approved','Rejected' and 'PMORequest'
    def get_filtered_plans(self, obj):
        qs = ActionPlan.objects.filter(crisis=obj, status="PMOApproved");
        serializer = self.IActionPlanSerializer(qs,many=True,read_only=True)
        return serializer.data

    class Meta:
        model = Crisis
        fields = ('id', 'status','crisisreport_set','actionplan_set','efupdate_set')
        # = ("crisisreport")


class EFSerializer(serializers.ModelSerializer):

    class ForceSerializer(serializers.Serializer):

         class Meta:
                model = ForceUtilization
                fields = ('name', 'utilization', 'update')

    force = ForceSerializer(many=True)

    def create(self, validated_data):
        force_utilizations = validated_data.pop('tracks')
        ef_update = EFUpdate.objects.create(**validated_data)
        for utilization_data in force_utilizations:
            ForceUtilization.objects.create(ef_update, **utilization_data)
        return ef_update

    class Meta:
        model = EFUpdate
        fields = ('id', 'datetime', 'actionPlan', 'crisis', 'description', 'statistics')

