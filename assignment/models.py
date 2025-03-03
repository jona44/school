from datetime import timezone
import os
from django.db import models
from customadmin.models import CustomUser
from district.models import AcademicCalendar
from student.models import ClassRoom, StudentProfile
from schoolconfig.models import SchoolSubject
from teacher.models import TeacherProfile
from django.utils.text import slugify


class Assignment(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField()
    subject     = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE)
    teacher     = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    classrooms  = models.ManyToManyField(ClassRoom)  # Change to ManyToManyField   
    due_date    = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True)
    academic_year = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def is_due(self):
        return self.due_date < timezone.now()

    @staticmethod
    def get_assignments_by_teacher(teacher_id):
        return Assignment.objects.filter(teacher__id=teacher_id)
    
    
from django.utils import timezone 


def dynamic_upload_path(instance, filename):
    now = timezone.now()  # Get the current time (timezone-aware)
    assignment_name = instance.assignment.title  # Or .id, etc.
    safe_assignment_name = slugify(assignment_name)
    return f"uploads/{now.year}/{now.month}/{filename}"

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
