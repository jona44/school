from django.db import models
from customadmin.models import CustomUser
from district.models import District_School_Registration,GradeLevel,AcademicCalendar,SubjectsManager
from django.utils.translation import gettext_lazy as _

class SchoolProfile(models.Model):
    school            = models.OneToOneField(District_School_Registration, on_delete=models.CASCADE, blank=True, null=True)
    school_logo       = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    is_setup_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.school}'
    
class SchoolAdminProfile(models.Model):
    school_admin   = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    email          = models.EmailField(blank=True, null=True)
    school         = models.ForeignKey(District_School_Registration, on_delete=models.CASCADE, blank=True, null=True)
    admin          = models.CharField(max_length=10, choices=[('admin1', 'admin1'), ('admin2', 'admin2'), ('admin3', 'admin3')], null=True, blank=True)
    address        = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth  = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True)
    last_updated   = models.DateTimeField(auto_now=True)
    is_complete    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.school_admin}'

   
    
class ClassName(models.Model):
    CLASS_CHOICES = [
        ('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),('E', 'E'),('F', 'F'),('G', 'G'),('H', 'H'),('I', 'I'),('J', 'J'),
    ]
    schoolprofile  = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE,blank=True, null=True)   
    grd_level      = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, null=True, blank=True)
    classname      = models.CharField(max_length= 1, choices=CLASS_CHOICES)
    academic_year  = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)
    date           = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.grd_level} {self.classname}-({self.academic_year}){self.schoolprofile }"    
    

class SchoolSubject(models.Model):
    subjects   = models.ManyToManyField(SubjectsManager)
    school     = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE,blank=True, null=True) 

    def __str__(self):
        return ', '.join(str(subject) for subject in self.subjects.all())
    
 
class ClassProfile(models.Model):
    name       = models.CharField(max_length=255, unique=True)  # e.g., "Science Stream", "Arts Stream"
    subjects   = models.ManyToManyField(SchoolSubject, related_name='class_profiles')
    is_default = models.BooleanField(default=False)  # One default profile

    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure only one default profile exists
            ClassProfile.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  