from assignment.forms import AssignmentCreateForm, AssignmentSubmissionForm

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from assignment.models import Assignment, AssignmentSubmission
from core.utils import get_teacher_profile
from schoolconfig.models import SchoolSubject
from student.models import ClassRoom, StudentProfile

# Create your views here.


@login_required
def assignments_list(request, subject_id):
    
    subject = get_object_or_404(SchoolSubject, id=subject_id)
    assignments = Assignment.objects.filter(subject=subject)  # Fetch only assignments for this subject
    
    context = {
        'assignments': assignments,
        'subject': subject,
    }
    return render(request, 'assignment/assignments_list.html', context)



@login_required
def create_assignment(request, subject_id):
    subject = get_object_or_404(SchoolSubject, pk=subject_id)
    teacher_profile = get_teacher_profile(request.user)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, teacher=teacher_profile)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher_profile
            assignment.subject = subject  # Set the subject here
            assignment.save()
            form.cleaned_data['classrooms'].set(assignment.classrooms.all())
            messages.success(request, 'Assignment created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentCreateForm(teacher=teacher_profile)

    assignments = Assignment.objects.filter(teacher=teacher_profile, subject=subject).order_by('-due_date')

    context = {
        'form': form,
        'assignments': assignments
    }
    return render(request, 'assignment/create_assignment.html', context)


@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('teacher_dashboard')
    else:
            form = AssignmentCreateForm(instance=assignment)

    context = {
       'form': form,
       'assignment': assignment
     }
    return render(request, 'assignment/update_assignment.html', context)


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
    return render(request, 'assignment/delete_assignment.html', context)   



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
    return render(request, 'assignment/submit_assignment.html', {'form': form, 'assignment': assignment})



@login_required
def assignment_view(request, assignment_id):
    student = request.user.studentprofile
    assignment = get_object_or_404(Assignment, id=assignment_id, school=student.school)
    subject  = assignment.subject
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
        context = {'submission': submission, 'assignment':assignment}
        return render(request, 'assignment/assignment_view.html', context)
    except AssignmentSubmission.DoesNotExist:
        return render(request, 'assignment/assignment_view.html', {'assignment':assignment, 'subject':subject})
    
    
    
@login_required
def submitted_assignments(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    teacher_profile = get_teacher_profile(request.user)

    # Get all assignments for this classroom and teacher
    assignments = Assignment.objects.filter(classrooms=classroom, teacher=teacher_profile)

    # Get only the students in the selected classroom
    students_in_classroom = StudentProfile.objects.filter(assigned_class=classroom)

    # Collect all submissions for the selected assignments and the students in the classroom
    submissions = AssignmentSubmission.objects.filter(
        assignment__in=assignments, student__in=students_in_classroom
    ).order_by('submitted_at')

    #filtering
    ungraded_only = request.GET.get('ungraded_only', False) #get the query parameter
    subject_filter = request.GET.get('subject', None)

    if ungraded_only:
        submissions = submissions.filter(graded=False)

    if subject_filter:
        submissions = submissions.filter(assignment__subject_id=subject_filter)
        
    #get the subjects that are taught by the teacher.
    all_subjects = teacher_profile.subjects_taught.all() #only the subjects taught by the teacher

    context = {
        'classroom': classroom,
        'submissions': submissions,
        'assignments': assignments,
        'all_subjects':all_subjects,
    }
    return render(request, 'assignment/submitted_assignments.html', context)



@login_required
def assignment_submission(request, assignment_id):
    """
    View for students to submit their assignments.
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.studentprofile  # Assuming you have a StudentProfile related to User

    try:
        existing_submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
        #if there is an existing submission we do not allow any more submissions.
        messages.warning(request, "You have already submitted this assignment.")
        return redirect('assignment_view', assignment_id=assignment_id)
    except AssignmentSubmission.DoesNotExist:
         if request.method == 'POST':
            form = AssignmentSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = student
                submission.save()
                messages.success(request, 'Assignment submitted successfully!')
                return redirect('assignment_view', assignment_id=assignment_id)
         else:
            form = AssignmentSubmissionForm()

    context = {
        'form': form,
        'assignment': assignment,
    }
    return render(request, 'assignment/assignment_submission.html', context)