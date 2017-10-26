from django.forms import ModelForm
from cmoapp.models import ActionPlan,ForceDeployment

class AnalystActionPlanForm(ModelForm):
    class Meta:
        model = ActionPlan
        fields = ['description, resolutionTime, projectedCasulaties']

class AnalystForceForm(ModelForm):
    model = ForceDeployment
    fields = ['Name','Recommended','Max']
