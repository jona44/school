from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from customadmin.models import  CustomUser
from customsettings.models import *
from student.models import ClassRoom
from district.models import District_School_Registration

class TeacherProfile(models.Model):
    assigned_school     = models.ForeignKey(District_School_Registration, on_delete=models.CASCADE, blank=True, null=True, related_name='teacher_profiles')
    teacher         = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    base_subject    = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE, null=True, blank=True,related_name='base_subject_teacher_profiles')
    assigned_class  = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='base_class')
    classes_taught  = models.ManyToManyField(ClassRoom,  related_name='teacher')
    subjects_taught = models.ManyToManyField(SchoolSubject, related_name='teacher_subjects')
    contact_number  = models.CharField(max_length=20)
    date            = models.DateField(auto_now_add=True, null=True, blank=True)
    academic_year   = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.teacher.first_name} {self.teacher.last_name}'
    
    def get_absolute_url(self):
            return reverse('view_teacher_profile', kwargs={'teacher_id': self.id})

    def get_all_classes_taught(self):
        return self.classes_taught.all()

    def get_all_subjects_taught(self):
        return self.subjects_taught.all()
    
    def get_base_subject(self):
        return self.base_subject
    
    def get_base_class(self):
        return self.base_class

  



