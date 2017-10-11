"""All models for myapp Django application.
"""
from django.db import models

#all models have automatically add an auto-increment id unless another field is explicitly specified as primary key
#note, on_delete assigns a Function 'Callback'
#note, no fking clue in the django tutorial that says you can add a null option, only says field options are
#avaliable to all field types, but no explict example wtf

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
class Crisis(models.Model):
    #analyst is FK to crisis. This enables analyst to be deleted once the crisis is resolved
    analyst = models.OneToOneField(Account,null=True,limit_choices_to={'type':'Analyst'}, on_delete=models.SET_NULL)
    crisistypes = models.ManyToManyField(CrisisType)


class CrisisReport(models.Model):
    #attributes
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    description = models.TextField()
    datetime = models.DateTimeField()

    #Relations, can have no crisis assigned for the sake of testi
    Crisis = models.ForeignKey(Crisis,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.pk,self.description);

class Location(models.Model):
    #Relations
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius = models.IntegerField()
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)

    def __str__(self):
        return 'ID: {}'.format(self.pk);

#The response plan of the crsos
class ActionPlan(models.Model):
    #attributes
    description = models.TextField()
    COApproval = models.BooleanField()
    PMOApproval = models.BooleanField()
    ResolutionTime = models.DurationField()
    ProjectedCasualties = models.DecimalField(max_digits=5, decimal_places=2)
    #Relations
    crisis = models.ForeignKey(Crisis, on_delete= models.CASCADE)

    def __str__(self):
        return 'ID: {}'.format(self.pk);

class Force(models.Model):
    name = models.TextField(primary_key=True)
    def __str__(self):
        return '{}'.format(self.name);

class ForceDeployment(models.Model):
    #a force can only be deleted after all force deployments are deleted
    name = models.ForeignKey(Force, on_delete= models.PROTECT)
    recommended = models.DecimalField(max_digits=5, decimal_places=2)
    ActionPlan =  models.ForeignKey(ActionPlan, on_delete= models.CASCADE)
    def __str__(self):
        return 'ID: {} Name: {}'.format(self.pk,self.name);

class EFUpdate(models.Model):
    #Attributes
    datetime = models.DateTimeField()
    affectedRadius = models.DecimalField(max_digits=12,decimal_places=2)
    totalInjured = models.IntegerField()
    totalDeaths = models.IntegerField()
    duration =  models.DurationField()
    ActionPlan = models.ForeignKey(ActionPlan,null=True,on_delete = models.SET_NULL)
    #i leave this here in case the action plan can be deleted. we can thus still have a reference back to cris
    Crisis = models.ForeignKey(Crisis, on_delete =  models.CASCADE)

    def __str__(self):
        return 'ID: {}'.format(self.pk);

class ForceUtilization(models.Model):
    name = models.ForeignKey(Force,on_delete= models.CASCADE)
    utilization = models.DecimalField(max_digits=5, decimal_places=2)
    update = models.ForeignKey(EFUpdate, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name);