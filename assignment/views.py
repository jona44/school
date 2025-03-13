from assignment.forms import AssignmentCreateForm, AssignmentSubmissionForm

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from assignment.models import Assignment
from core.utils import get_teacher_profile
from schoolconfig.models import SchoolSubject
from student.models import StudentProfile

# Create your views here.
@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    profile = get_object_or_404(StudentProfile, student=request.user)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = profile
            submission.assignment = assignment
            submission.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('student_dashboard')
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'student/submit_assignment.html', {'form': form, 'assignment': assignment})



@login_required
def assignments_list(request, subject_id):
    
    subject = get_object_or_404(SchoolSubject, id=subject_id)
    assignments = Assignment.objects.filter(subject=subject)  # Fetch only assignments for this subject
    
    context = {
        'assignments': assignments,
        'subject': subject,
    }
    return render(request, 'grading/assignments_list.html', context)


@login_required
def create_assignment(request, subject_id):
    subject = get_object_or_404(SchoolSubject, pk=subject_id)
    teacher_profile = get_teacher_profile(request.user)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher_profile
            assignment.subject = subject
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentCreateForm()

    assignments = Assignment.objects.filter(teacher=teacher_profile, subject=subject).order_by('-due_date')

    context = {
        'form': form,
        'assignments': assignments
    }
    return render(request, 'grading/create_assignment.html', context)


@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('create_assignment', assignment.id)
    else:
            form = AssignmentCreateForm(instance=assignment)

    context = {
       'form': form,
       'assignment': assignment
     }
    return render(request, 'grading/update_assignment.html', context)


@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    subject_id = assignment.subject.id

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('create_assignment', subject_id)

    context = {
        'assignment': assignment
    }
    return render(request, 'grading/delete_assignment.html', context)   

