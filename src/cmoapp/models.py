"""All models for myapp Django application.
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator,MinValueValidator

#all models have automatically add an auto-increment id unless another field is explicitly specified as primary key
#note, on_delete assigns a Function 'Callback'
#note, no fking clue in the django tutorial that says you can add a null option, only says field options are
#avaliable to all field types, but no explict example wtf
#note, if you want a FK that is null, you have to set blank=true so that validation will not be triggered

class Account(models.Model):
    TYPES = (
        ('Analyst','Analyst'),
        ('Operator', 'Operator'),
        ('Chief', 'Chief')
    )
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return '{}'.format(self.login)

class CrisisType(models.Model):
    #Attributes
    name = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.name)

#has nothing but a bunch of foreign keys such keys much wow
#Crisis ID
class Crisis(models.Model):
    #analyst is FK to crisis. This enables analyst to be deleted once the crisis is resolved
    analyst = models.OneToOneField(Account,blank=True,null=True,limit_choices_to={'type':'Analyst'}, on_delete=models.SET_NULL)
    STATUS = (
        ('Clean-up','Clean up'),
        ('Ongoing','Ongoing'),
        ('Resolved', 'Resolved')
    )
    status = models.CharField(max_length=20, choices=STATUS)

    #class Meta:
     #   ordering = ['analyst']

    def injuries(self):
        return self.efupdate_set.latest('datetime').totalDeaths

    def deaths(self):
        return self.efupdate_set.latest('datetime').totalInjured

    def __str__(self):
        return 'ID: {} - assigned to: {}'.format(self.pk, self.analyst)

class CrisisReport(models.Model):
    #attributes
    description = models.TextField()
    datetime = models.DateTimeField()
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius = models.IntegerField(verbose_name="Radius(Metres)", validators=[MinValueValidator(0)])
    #Relations, can have no crisis assigned for the sake of testi

    crisis = models.ForeignKey(Crisis,null=True,blank=True,on_delete=models.CASCADE)
    crisisType = models.ForeignKey(CrisisType,null=True,blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'ID: {} - {}'.format(self.pk,self.description)

#The response plan of the crsis.
#The deployment id is the action plan id
class ActionPlan(models.Model):
    #attributes

    #plan Number supports the CMO-PMO API as their endpoint is expecting "<<CrisisID>><<planNumber>> where "
    #where planNumber is the running number of the plan related to its crisis
    def _planNumber(self):
        return self.crisis.actionplan_set.all().count()


    planNumber = models.IntegerField(validators=[MinValueValidator(1)], editable=False,null=True, default=_planNumber());
    description = models.TextField(null=True,blank=True)
    STATUS= (
        ('Planning','Planning'),
        ('CORequest','Awaiting CO Approval'),
        ('PMORequest','Awaiting PMO Approval'),
        ('Rejected','Rejected'),
        ('PMOApproved','Approved')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    resolutionTime = models.DurationField()
    projectedCasualties = models.IntegerField(validators=[MinValueValidator(0)])
    #Relations
    TYPES = (
        ('Clean-up','Clean up'),
        ('Combat','Combat'),
        ('Resolved','Resolved')
    )
    type = models.CharField(max_length=20, choices=TYPES)
    crisis = models.ForeignKey(Crisis, on_delete= models.CASCADE)

    def abridged_description(self):
        return self.description[:140] + "..."

    def __str__(self):
        return 'ID: {}'.format(self.pk);


class Comment(models.Model):
    text = models.TextField()
    authors = (
        ('PMO','Prime Minister\'s Office'),
        ('CO','Chief Officer')
    )
    author = models.CharField(max_length=20, choices=authors)
    #timeCreated = models.DateTimeField(auto_now=True/auto_now_add=True) not used cause it causes the field to not be seen
    #on the DB/ admin site, it can still be referenced (hard to debug/ check)
    timeCreated = models.DateTimeField(default=timezone.now,editable=False)
    #If the CO comments, then it is rejected by CO. If PMO comments, then PMO has rejected.
    actionPlan = models.OneToOneField(ActionPlan, on_delete= models.CASCADE)

    def abridged(self):
        return self.description[:140] + "..."

    def __str__(self):
        return 'ID: {} - Author: {} - Comment: {}'.format(self.id, self.author,self.text)

class Force(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    #Current Utilisation can be NULL, in the event that EF cannot provide, then the field is set to NULL and Blank
    currentUtilisation = models.DecimalField(null=True,blank=True, max_digits=5, decimal_places=2)
    def __str__(self):
        return '{}'.format(self.name);

#Force deployment tracks how much force to deploy for an action plan
class ForceDeployment(models.Model):
    #a force can only be deleted after all force deployments are deleted
    name = models.ForeignKey(Force, on_delete= models.PROTECT)
    recommended = models.DecimalField(max_digits=5, decimal_places=2)
    max = models.DecimalField(max_digits=5, decimal_places=2)
    actionPlan =  models.ForeignKey(ActionPlan, on_delete= models.CASCADE)
    def __str__(self):
        return 'ID: {} Name: {}'.format(self.pk,self.name)

class EFUpdate(models.Model):
    #Attributes
    datetime = models.DateTimeField()
    affectedRadius = models.DecimalField(max_digits=12,decimal_places=2, verbose_name="Affected Radius")
    totalInjured = models.IntegerField(verbose_name="Total Injured")
    totalDeaths = models.IntegerField(verbose_name="Total Deaths")
    duration =  models.DurationField()
    actionPlan = models.ForeignKey(ActionPlan,null=True,on_delete = models.SET_NULL)
    #i leave this here in case the action plan can be deleted. we can thus still have a reference back to cris
    crisis = models.ForeignKey(Crisis, on_delete =  models.CASCADE)
    description = models.TextField()
    #We are removing types and adding a request
    TYPES = (
        ('Request','Request'),
        ('Notifications','Notifications')
    )
    def __str__(self):
        return 'ID: {}'.format(self.pk)

#Force Utilization tracks how much each force is being used for the current action plan
class ForceUtilization(models.Model):
    name = models.ForeignKey(Force,on_delete= models.CASCADE)
    utilization = models.DecimalField(max_digits=5, decimal_places=2)
    update = models.ForeignKey(EFUpdate, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name);