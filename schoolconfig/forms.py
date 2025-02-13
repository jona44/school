from django import forms
from .models import *

class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolProfile
        fields = ['school_logo']

    def save(self, commit=True):
        instance = super(SchoolProfileForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # Save the many-to-many relationships
        return instance
    

class SchoolSubjectForm(forms.ModelForm):
    school_subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = SchoolSubject
        fields = ['school_subjects']


class ClassNameForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['grd_level','classname']


class GradeLevelForm(forms.ModelForm):
    class Meta:
        model = GradeLevel
        fields = ['grade_level'] 
        
        
        
class AssignSchoolAdminForm(forms.ModelForm):
    class Meta:
        model = SchoolAdminProfile
        fields = [
            
            'school',
            'admin',
            
        ]       
         

class SchoolAdminProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolAdminProfile
        fields = [
            'contact_number',
            'email',
            'school',
            'admin',
            'address',
            'date_of_birth',
            'profile_picture',
            
        ]


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'user_type', 'is_active']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }   
       
        
class CustomUserSearchForm(forms.Form):
    query = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search for user...'}))        
        