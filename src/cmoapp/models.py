"""All models for myapp Django application.
"""


from django.db import models

#all models have automatically add an auto-increment id unless another field is explicitly specified as primary key
#note, on_delete assigns a Function 'Callback'
#note, no fking clue in the django tutorial that says you can add a null option, only says field options are
#avaliable to all field types, but no explict example wtf

class Analyst(models.Model):
    name = models.CharField(max_length=100)

#has nothing but a bunch of foreign keys such keys much wow
class Crisis(models.Model):
    #analyst is FK to crisis. This enables analyst to be deleted once the crisis is resolved
    analyst = models.OneToOneField(Analyst,null=True, on_delete=models.SET_NULL)

class CrisisReport(models.Model):
    #attributes
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    description = models.TextField()
    datetime = models.DateTimeField()

    #Relations
    Crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)

class CrisisType(models.Model):
    #Attributes
    name = models.CharField(max_length=50)
    crisis = models.ManyToManyField(Crisis)

class Location(models.Model):
    #Relations
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius = models.IntegerField()
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)


#The response plan of the crsos
class ActionPlan(models.Model):
    #attributes
    description = models.TextField()
    COApproval = models.BooleanField()
    PMOApproval = models.BooleanField()

    #Relations
    crisis = models.ForeignKey(Crisis)


class Force(models.Model):
    name = models.TextField(primary_key=True)

class ForceDeployment(models.Model):
    name = models.ForeignKey(Force, on_delete= models.PROTECT)
    recommended = models.DecimalField(max_digits=5, decimal_places=2)
    max = models.DecimalField(max_digits=5, decimal_places=2)


class EFUpdate(models.Model):
    #Attributes
    datetime = models.DateTimeField()
    affectedRadius = models.DecimalField(max_digits=12,decimal_places=2)
    totalInjured = models.IntegerField()
    totalDeaths = models.IntegerField()
    duration =  models.DurationField()
    description = models.TextField()

    #Relations
    ActionPlan = models.ForeignKey(ActionPlan,null=True,on_delete = models.SET_NULL)
    #i leave this here in case the action plan can be deleted. we can thus still have a reference back to cris
    Crisis = models.ForeignKey(Crisis, on_delete =  models.CASCADE)
