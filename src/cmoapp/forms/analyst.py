from django.forms import ModelForm
from cmoapp.models import ActionPlan,ForceDeployment

class ActionPlanForm(ModelForm):

    class Meta:
        model = ActionPlan
        fields = ['description', 'resolution_time', 'projected_casualties', 'type']


class ForceForm(ModelForm):

    class Meta:
        model = ForceDeployment
        fields = ['name','recommended','max']
