from django import template
from django.utils import timezone
from assignment.models  import AssignmentSubmission

register = template.Library()

@register.filter
def submission_status(assignment, user):
    if not user.is_authenticated:
        return {'text': 'N/A', 'color': 'secondary'}

    student_profile = getattr(user, 'studentprofile', None)
    if not student_profile:
        return {'text': 'N/A', 'color': 'secondary'}

    # Check if the student has submitted the assignment
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student_profile).exists()

    if submission:
        return {'text': 'Submitted', 'color': 'success'}
    
    # Check if assignment is overdue
    if assignment.due_date < timezone.now():
        return {'text': 'Overdue', 'color': 'danger'}
    
    return {'text': 'Pending', 'color': 'warning'}
