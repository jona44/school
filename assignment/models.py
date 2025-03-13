from django.db import models

from district.models import AcademicCalendar
from schoolconfig.models import SchoolSubject
from student.models import StudentProfile
from teacher.models import TeacherProfile

# Create your models here.
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

