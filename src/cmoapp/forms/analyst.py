from django.forms import ModelForm,ChoiceField,IntegerField
from cmoapp.models import ActionPlan,ForceDeployment
from datetime import timedelta

class ActionPlanForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActionPlanForm, self).__init__(*args, **kwargs)
        self.fields['description'].blank = False
        self.fields['description'].required = True

    duration_types = (
        ("week","Weeks"),
        ("days","Days"),
        ("hours","Hours")
    )
    duration_type = ChoiceField(choices=duration_types)
    duration_count = IntegerField(min_value=1, label="Projected Duration")

    class Meta:
        model = ActionPlan
        fields = ['description', 'projected_casualties', 'type']

    def update_or_create(self,crisis=None, plan_status="Planning"):

        if crisis:
            try:
                ap = ActionPlan.objects.get(crisis=crisis,status="Planning")
                for key, value in self.cleaned_data.items():
                    setattr(ap, key, value)
            except ActionPlan.DoesNotExist:
                ap = super(ActionPlanForm, self).save(commit=False)

            ap.status=plan_status
            ap.crisis=crisis

            if self.cleaned_data['duration_type'] == 'week':
               td = {'days': self.cleaned_data['duration_count']*7}
            else:
               td = {self.cleaned_data['duration_type']: self.cleaned_data['duration_count']}
            ap.resolution_time= timedelta(**td)
            #Causes a double call to Model.Clean() because ModelForm.is_valid calls Model.clean also
            #A small performance price to pay at this point in time until we change the ModelForm back to the normal Form
            ap.clean()
            ap.save()
        else:
            raise ValueError("Crisis ID of Action Plan Object needs to be set before saving")

class ForceForm(ModelForm):

    class Meta:
        model = ForceDeployment
        fields = ['name','recommended','max']

    # def update_or_create(self,action_plan=None):
    #     if(action_plan):
    #         try:
    #
    #         except ForceDeployment.DoesNotExist
    #
    #
    #     else:
    #         raise ValueError("Action Plan of Force Deployment Object needs to be set before saving")
    #     pass