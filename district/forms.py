from django import forms
from django.contrib.auth.forms import UserCreationForm
from customadmin.models import CustomUser
from schoolconfig.models import SchoolAdminProfile
from teacher.models import TeacherProfile
from . models import AcademicCalendar, District,District_School_Registration, DistrictAdminProfile, Holiday, SchoolHeadProfile, SubjectsManager




class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model  = District_School_Registration
        fields = [ 'school', 'address', 'phone_number', 'email','district']

        widgets = {
                'school': forms.TextInput(attrs={
                'class': 'form-control',
                  
                }),
                
                'address': forms.Textarea(attrs={
                'class': 'form-control',
                 
                  'rows':  3
                }),
                'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                 
                }),

                'email': forms.EmailInput(attrs={
                'class': 'form-control',
                 
                  
                }),
                }
        

class    SchoolHeadRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password1','password2' )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
            else:
                field.widget.attrs = {'class': 'form-control'}       
        
        
        widgets = {
           'email': forms.TextInput(attrs={
                'class': 'form-control',
               
                }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                
                }),
            
           'password1': forms.PasswordInput(attrs={
                'class': 'form-control',  
                }),
       
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
               
                }),
         }
        
class    DistrictAdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password1','password2' )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
            else:
                field.widget.attrs = {'class': 'form-control'}    
                
                
                
class    SchoolAdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password1','password2' )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
            else:
                field.widget.attrs = {'class': 'form-control'}    
        
        
        # widgets = {
        #    'email': forms.TextInput(attrs={
        #         'class': 'form-control',
               
        #         }),
        #     'first_name': forms.TextInput(attrs={
        #         'class': 'form-control',
                
        #         }),
        #     'last_name': forms.TextInput(attrs={
        #         'class': 'form-control',
                
        #         }),
           
        #     'position': forms.Select(attrs={
        #         'class': 'form-control',
                
        #         }),
        #     'password1': forms.PasswordInput(attrs={
        #         'class': 'form-control',  
        #         }),
       
        #     'password2': forms.PasswordInput(attrs={
        #         'class': 'form-control',
               
        #         }),
        #  }
        
        
        
class SchoolHeadProfileForm(forms.ModelForm):
    class Meta:
        model = SchoolHeadProfile
        fields = [
            'contact_number',
            'email',
            'school',
            'address',
            'date_of_birth',
            'profile_picture',
            'is_complete',
        ]
        widgets = {
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model  = SubjectsManager
        fields = ['subjects']


class DistrictAdminProfileForm(forms.ModelForm):
    class Meta:
        model   = DistrictAdminProfile
        fields  = ['contact_number','district_name']
        widgets = {
            'district_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
           
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
            
        }        
        
class AcademicCalendarForm(forms.ModelForm):
    class Meta:
        model = AcademicCalendar
        fields = [
            
            'academic_year',
            'term_1_start_date',
            'term_1_end_date',
            'term_2_start_date',
            'term_2_end_date',
            'term_3_start_date',
            'term_3_end_date',
            'term_4_start_date',
            'term_4_end_date',
        ]
        widgets = {
            'academic_year': forms.DateInput(attrs={
                'class': 'form-control',
               
                
                }),
            'term_1_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px','class':'form-control',}),
            'term_1_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_2_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_2_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_3_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_3_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_4_start_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
            'term_4_end_date': forms.DateInput(attrs={'type': 'date','style':'width:300px;','class':'form-control',}),
        }
        
        
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('name', 'date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': ' box-shadow: 0 0 0 0.2rem rgba(0, 255, 0, 0.25);',
                }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'width: 350px; box-shadow: 0 0 0 0.2rem rgba(0, 255, 0, 0.25);',
                }),
        }        
        
        
class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district']
        
        
class AssignSchoolAdminForm(forms.ModelForm):
    class Meta:
        model = SchoolAdminProfile 
        fields = ['school']
        widgets = {
            'school': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
            'admin': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width:350px;',
                }),
        }        
class AssignSchoolHeadForm(forms.ModelForm):
    class Meta:
        model = SchoolHeadProfile 
        fields = ['school','school_head']
        widgets = {
            'school': forms.Select(attrs={
                'class': 'form-control',
                
                }),
            'school_head': forms.Select(attrs={
                'class': 'form-control',
               
                }),
        }    
        
 # Create a form for group creation
class GroupForm(forms.Form):
    name = forms.CharField(max_length=150, required=True, label="Group Name")           