from datetime import datetime
from django.db import models
from django.urls import reverse
from customadmin.models import  CustomUser
from schoolconfig.models import *
from student.models import ClassRoom, StudentProfile
from django.conf import settings
import os
from django.utils.timezone import now

class TeacherProfile(models.Model):
    school          = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, blank=True, null=True, related_name='teacher_profiles')
    teacher         = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    base_subject    = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE, null=True, blank=True, related_name='base_subject_teacher_profiles')
    assigned_class  = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='base_class')
    classes_taught  = models.ManyToManyField(ClassRoom,  related_name='teacher')
    subjects_taught = models.ManyToManyField(SchoolSubject, related_name='teacher_subjects')
    contact_number  = models.CharField(max_length=20)
    date            = models.DateField(auto_now_add=True, null=True, blank=True)
    academic_year   = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)
    on_medical_leave    = models.BooleanField(default=False, null=True, blank=True)
    on_vocational_leave = models.BooleanField(default=False, null=True, blank=True)
    position            = models.CharField(max_length=10, null=True, blank=True, choices=[('Permanent', 'Permanent'), ('Substitute', 'Substitute')])
    
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

    @staticmethod
    def get_teacher_profile(teacher_id):
        try:
            return TeacherProfile.objects.get(teacher__id=teacher_id)
        except TeacherProfile.DoesNotExist:
            return None

  

class Subject(models.Model):
    name      = models.CharField(max_length=255)
    teacher   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})

    def __str__(self):
        return self.name

    @staticmethod
    def get_subject_by_teacher(teacher_id):
        return Subject.objects.filter(teacher__id=teacher_id)


class Assignment(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()
    subject     = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    teacher     = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    due_date    = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True)
    academic_year   = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def is_due(self):
        return self.due_date < timezone.now()

    @staticmethod
    def get_assignments_by_teacher(teacher_id):
        return Assignment.objects.filter(teacher__id=teacher_id)


import os
from django.utils.text import slugify
from django.utils import timezone  # Use timezone-aware datetimes

def dynamic_upload_path(instance, filename):
    now = timezone.now()  # Get the current time (timezone-aware)
    assignment_name = instance.assignment.title  # Or .id, etc.
    safe_assignment_name = slugify(assignment_name)
    return os.path.join('uploads', safe_assignment_name, str(now.year), filename)

class AssignmentSubmission(models.Model):
    assignment   = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student      = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    file         = models.FileField(upload_to=dynamic_upload_path)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.assignment}'

    @staticmethod
    def get_submissions_by_assignment(assignment_id):
        return AssignmentSubmission.objects.filter(assignment__id=assignment_id)

