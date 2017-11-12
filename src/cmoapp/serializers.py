from rest_framework import serializers
from cmoapp.models import Account, Crisis, CrisisReport, CrisisType, ActionPlan, Comment, Force, ForceDeployment, EFUpdate, ForceUtilization, Notifications
from django.utils import timezone

class CrisisSerializer(serializers.ModelSerializer):

    totalInjured = serializers.IntegerField(source="injuries")
    totalDeaths = serializers.IntegerField(source="deaths")

    class Meta:
        model = Crisis
        fields = ('id', 'analyst', 'status', 'totalInjured', 'totalDeaths')

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


    class InternalSerializer(serializers.ModelSerializer):

        class Meta:
            model = ActionPlan
            fields = ('plan_number','id')

    actionPlan = InternalSerializer(many=False)

    class Meta:
        model = Comment
        #planNumber = serializers.IntegerField(source=Comment.actionPlan.plan_number)
        fields = ('id', 'text', 'author', 'timeCreated', 'actionPlan')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ('title', 'text', '_for', 'new', 'time_added')

class AuthSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=100)
    approval = serializers.BooleanField(required=True)

    def validate(self, data):
        id = data.get('id')
        text = data.get('text',None)
        approval = data.get('approval')
        ap = ActionPlan.objects.get(id=id)

        if ap.status != 'PMORequest':
            raise serializers.ValidationError('ActionPlan already validated')
        elif approval == False and text == None:
            raise serializers.ValidationError('Comment should exists')
        elif ap.status == 'PMORequest':
            return data;

        return data;

    def save(self):
        aid = self.validated_data['id']
        ap = ActionPlan.objects.get(id = aid)
        if self.validated_data['approval'] == True:
            ap.status = 'PMOApproved'
        else:
            ap.status = 'Rejected'

        ap.save()

        if self.validated_data['approval'] == False:
            author = 'PMO'
            text = self.validated_data['text']
            timeCreated = timezone.now()
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

        class IForceUtilizationSerializer(serializers.ModelSerializer):

            class Meta:
                model = ForceUtilization
                fields = ('name','utilization')

        forceutilization_set = IForceUtilizationSerializer(read_only=True,many=True)

        class Meta:
            model = EFUpdate
            fields = ('id','datetime', 'affectedRadius', 'totalInjured', 'totalDeaths', 'duration', 'description','forceutilization_set')

    class IActionPlanSerializer(serializers.ModelSerializer):

        class IForceDeploymentSerializer(serializers.ModelSerializer):

            class Meta:
                model = ForceDeployment
                fields = ('name','recommended','max')


        class ICommentSerializer(serializers.ModelSerializer):

            class Meta:
                model = Comment
                fields = ('id','text','author','timeCreated')


        forcedeployment_set = IForceDeploymentSerializer(many=True, read_only=True)

        comment = ICommentSerializer(read_only=True)

        class Meta:
            model = ActionPlan
            fields = ('id', 'plan_number', 'description', 'status', 'resolution_time', 'projected_casualties','outgoing_time', 'type', 'forcedeployment_set', 'comment')

    crisisreport_set = IReportSerializer(many=True, read_only=True)
    actionplan_set = serializers.SerializerMethodField('get_filtered_plans')
    efupdate_set = IEFUpdateSerializer(many=True, read_only=True)

    #Filter out "Planning', or in 'CORequest'
    #Show 'Approved','Rejected' and 'PMORequest'
    def get_filtered_plans(self, obj):
        qs =  ActionPlan.objects.exclude(status='Planning',).exclude(status='CORequest')
        serializer = self.IActionPlanSerializer(qs,many=True,read_only=True)
        return serializer.data

    totalInjured = serializers.IntegerField(source="injuries")
    totalDeaths = serializers.IntegerField(source="deaths")

    class Meta:
        model = Crisis
        fields = ('id', 'status','crisis_title','totalInjured', 'totalDeaths', 'crisisreport_set','actionplan_set','efupdate_set')
        # = ("crisisreport")



    #actionPlan = serializers.PrimaryKeyRelatedField(queryset=ActionPlan.objects.all())
    #crisis = serializers.PrimaryKeyRelatedField(queryset=Crisis.objects.all())

class EFSerializer(serializers.ModelSerializer):

    class StatisticsSerializer(serializers.Serializer):
        class ForceSerializer(serializers.ModelSerializer):
            # utilization = serializers.DecimalField(source="Utilisation",required=False,max_digits=5, decimal_places=2)
            # name = serializers.PrimaryKeyRelatedField(read_only=True)
            # utilization = serializers.DecimalField(max_digits=5, decimal_places=2)
            # FUCKING DRF CAN'T DO NESTED SERIALIZATION ON MODELS
            class Meta:
                fields = ('name', 'utilization')
                model = ForceUtilization

        force = serializers.ListField(child=ForceSerializer(), required=False)
        # Wtf DATA IS PASSED AS TotalDuration but is referenced by the field name designated as source
        #NOT THE OTHER WAY ROUND WTF ISN'T SOURCE AS IN SOURCE DATA?
        TotalDuration = serializers.DurationField(source='duration', required=False)
        AffectedRadius = serializers.IntegerField(source="affectedRadius", min_value=0)
        TotalInjured = serializers.IntegerField(source='totalInjured', min_value=0)
        TotalDeaths = serializers.IntegerField(source='totalDeaths', min_value=0)

    statistics = StatisticsSerializer(source='*')

    class Meta:
        model = EFUpdate
        fields = ('crisis','actionPlan', 'datetime','type', 'description', 'statistics')

    def create(self, validated_data):
        force_data = validated_data.pop('force')
        efupdate = EFUpdate.objects.create(**validated_data)
        for data in force_data:
            #Create Force Utilization
            FU = ForceUtilization.objects.create(update=efupdate,**data)
            #Update each force's utilization
            force = FU.name
            force.currentUtilisation = FU.utilization
            force.save()
        return efupdate
