from django import forms
from cmoapp.models import Crisis

class CrisisForm(forms.ModelForm):
    class Meta:
        model = Crisis
        # exclude = ['author', 'updated', 'created', ]
        fields = ['analyst']
        widgets = {
            'analyst': forms.TextInput(
                attrs={'id': 'crisis-analyst', 'required': True, 'placeholder': 'Say something...'}
            ),
        }
