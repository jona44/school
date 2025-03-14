# Inside assignment/templatetags/assignment_tags.py
from django import template
from assignment.models import AssignmentSubmission
from datetime import date

register = template.Library()

@register.simple_tag
def has_student_submitted(assignment, student_profile):
    """Checks if a student has submitted an assignment."""
    if not student_profile:
        return False
    return AssignmentSubmission.objects.filter(
        assignment=assignment, student=student_profile
    ).exists()

@register.simple_tag
def is_assignment_overdue(assignment, today):
    """Checks if an assignment is overdue."""
    return assignment.due_date.date() < today

