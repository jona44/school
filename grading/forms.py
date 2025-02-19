from django import forms
from customadmin.models import CustomUser
from teacher.models import Assignment
from .models import *
from django import forms


class CaptureForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields = ['test_type', 'topic', 'total_mark']
       


class CapturedClassroomForm(forms.ModelForm):
    class Meta:
        model = CapturedClassroom
        fields = ['classroom']



class GetMarkForm(forms.ModelForm):
    class Meta:
        model  = GetMark
        fields = [ 'mark'] 
        

class EditMarkForm(forms.ModelForm):
    class Meta:
        model  = GetMark
        fields = [ 'mark'] 


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
        
   
