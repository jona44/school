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
        fields = ['grd_level', 'classname']

    def __init__(self, *args, schoolprofile=None, academic_year=None, **kwargs):
        super().__init__(*args, **kwargs)

        if schoolprofile and academic_year:
            used_classnames = ClassName.objects.filter(
                schoolprofile=schoolprofile, academic_year=academic_year
            ).values_list('classname', flat=True)

            # Exclude used class names from the choices
            self.fields['classname'].choices = [
                (code, label) for code, label in ClassName.CLASS_CHOICES if code not in used_classnames
            ]



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
        fields = ['contact_number', 'school', 'admin','address', 'date_of_birth', 'profile_picture',]
        
        widgets = {
            
           
           'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 250px; background-color: #474955; color:white',
                }),
           'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'width: 150px; background-color: #474955; color:white',
                }),
            
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                  'rows':  3
                }),
          
        }   


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
   


class ClassProfileForm(forms.ModelForm):
    class Meta:
        model = ClassProfile
        fields = ['name', 'subjects', 'is_default']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
        }
        