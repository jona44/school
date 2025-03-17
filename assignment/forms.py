from django import forms
from customadmin.models import CustomUser
from .models import *
from django import forms




class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_date', 'description', ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'style': 'width:350px;',
                }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'style': 'width:350px;',
                }),
            'description':forms.Textarea(attrs={
                'class': 'form-control',
                'type': 'text',
                'rows': 3,
                }),
        }
        
   
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']
       