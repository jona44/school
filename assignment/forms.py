from django import forms
from customadmin.models import CustomUser
from .models import *
from django import forms




from django import forms
from .models import Assignment, SchoolSubject, ClassRoom

from django import forms
from django.forms import ModelMultipleChoiceField # Import ModelMultipleChoiceField
from customadmin.models import CustomUser
from .models import *

from django import forms
from .models import Assignment, SchoolSubject, ClassRoom

class AssignmentCreateForm(forms.ModelForm):
    classrooms = ModelMultipleChoiceField(
        queryset=ClassRoom.objects.none(),  # Start with an empty queryset
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True
    )
    # We removed subject from the form here.

    class Meta:
        model = Assignment
        fields = ['title', 'due_date', 'description', 'classrooms']  # Removed 'subject' from fields
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'style': 'width:350px;',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            self.fields['classrooms'].queryset = teacher.classes_taught.all()


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']

   
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']
       