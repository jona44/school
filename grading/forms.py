from django import forms
from customadmin.models import CustomUser
from django import forms
from grading.models import Capture, CapturedClassroom, GetMark


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


