from django import forms
from .models import Assignment, AssignmentSubmission


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_date', 'description', 'classrooms','file']  # Include classrooms and file
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
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'type': 'text',
                'rows': 3,
            }),
            'classrooms': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),  # Use CheckboxSelectMultiple
        }

    file = forms.FileField(
        required=False,  # Make the file upload optional
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Upload Assignment File (Optional)"
    )

    def __init__(self, *args, **kwargs):
        teacher_profile = kwargs.pop('teacher_profile', None)
        super().__init__(*args, **kwargs)

        if teacher_profile:
            self.fields['classrooms'].queryset = teacher_profile.classes_taught.all() #filter the classes
            
            
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']  # Only the file field is needed for submission
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'file': 'Upload Your Assignment File',
        }

