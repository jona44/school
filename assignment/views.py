from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib import messages
from schoolconfig.models import SchoolSubject
from student.models import ClassRoom
from teacher.models import TeacherProfile
from .forms import AssignmentCreateForm, AssignmentSubmissionForm
from .models import Assignment, AssignmentSubmission
from core.utils import get_teacher_profile


@login_required
def create_assignment(request, subject_id):
    subject = get_object_or_404(SchoolSubject, pk=subject_id)
    teacher_profile = get_teacher_profile(request.user)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES, teacher_profile=teacher_profile) #pass the teacher_profile to the form
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher_profile
            assignment.subject = subject
            assignment.save() #save the assignment first
            assignment.classrooms.set(form.cleaned_data['classrooms']) #add the classrooms selected in the form
            messages.success(request, 'Assignment created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentCreateForm(teacher_profile=teacher_profile) # pass the teacher profile to the form

    assignments = Assignment.objects.filter(teacher=teacher_profile, subject=subject).order_by('-due_date')

    context = {
        'form': form,
        'assignments': assignments
    }
    return render(request, 'assignment/create_assignment.html', context)


#-------------------------update assignment--------------------------------


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
   return render(request, 'assignment/update_assignment.html', context)

#-------------------------delete assignment--------------------------------

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

#-------------------------assignment list--------------------------------

@login_required
def assignments_list(request, subject_id):
   subject = get_object_or_404(SchoolSubject, id=subject_id)
   assignments = Assignment.objects.filter(subject=subject)  # Fetch only assignments for this subject

   context = {
       'assignments': assignments,
       'subject': subject,
   }
   return render(request, 'assignment/assignments_list.html', context)

#-------------------------assignment submission--------------------------------

@login_required
def assignment_submission(request, assignment_id):
   assignment = get_object_or_404(Assignment, pk=assignment_id)
   student = request.user.studentprofile
   try:
       existing_submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
       messages.warning(request, 'You have already submitted this assignment.')
       return redirect('assignment_list', assignment_id)
   except AssignmentSubmission.DoesNotExist:
       if request.method == 'POST':
           form = AssignmentSubmissionForm(request.POST, request.FILES)
           if form.is_valid():
               submission = form.save(commit=False)
               submission.assignment = assignment
               submission.student = student
               submission.save()
               messages.success(request, 'Assignment submitted successfully!')
               return redirect('assignments_list', assignment_id)
       else:
           form = AssignmentSubmissionForm()

       context = {
           'form': form,
           'assignment': assignment,
       }
       return render(request, 'assignment/assignment_submission.html', context)
   
#-------------------------assignment list-------------------------------- 

@login_required
def assignment_view(request, assignment_id):
    student = request.user.studentprofile
    assignment = get_object_or_404(Assignment, id=assignment_id)
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
        context = {'submission': submission, 'assignment':assignment}
        return render(request, 'assignment/assignment_view.html', context)
    except AssignmentSubmission.DoesNotExist:
        return render(request, 'assignment/assignment_view.html', {'assignment':assignment})
from django.shortcuts import render


#-------------------------submitted assignments--------------------------------
# c:\Users\tjman\OneDrive\school\assignment\views.py
@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'teacher')
def submitted_assignments(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, pk=classroom_id)
    teacher_profile = get_teacher_profile(request.user)

    # Get all assignments for this classroom and teacher
    assignments = Assignment.objects.filter(classrooms=classroom, teacher=teacher_profile) #filter by classrooms

    # Collect all submissions for the selected assignments
    submissions = AssignmentSubmission.objects.filter(assignment__in=assignments).order_by('submitted_at')

    context = {
        'classroom': classroom,
        'submissions': submissions,
        'assignments': assignments,
    }
    return render(request, 'assignment/submitted_assignments.html', context)

