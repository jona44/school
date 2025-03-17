# Inside assignment/templatetags/assignment_tags.py
from django import template
from assignment.models import AssignmentSubmission
from datetime import date, datetime

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
    # If today is empty or None, use the current date
    if not today:
        today = date.today()
    elif isinstance(today, str):
        try:
            today = datetime.strptime(today, "%Y-%m-%d").date()
        except ValueError:
            today = date.today()  # Fallback to current date if parsing fails
    
    return assignment.due_date.date() < today



