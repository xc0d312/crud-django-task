from django import forms
from .models import Tasks
class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title','description','important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':'4'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto '})
        }