from itertools import count
from multiprocessing import context
from django import views
from django.views import View
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str 
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from schoolconfig.models import SchoolProfile, SchoolSubject, SchoolAdminProfile
from teacher.models import TeacherProfile
from student.models import StudentProfile

from . forms import *
import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    user = request.user
    context = {}
    # print(f"User: {user.email}, Groups: {user.groups.all()}")  # Debugging statement:

#--------------------------------------Student Dashboard---------------------------------------

    if request.user.groups.filter(name='student').exists():
        try:
            student_profile = StudentProfile.objects.get(student=request.user)
            school = student_profile.school
            assigned_class = student_profile.assigned_class

            if assigned_class:
                # Get subjects from the ClassProfile instead of SchoolSubject
                class_profile = assigned_class.profile
                subjects = class_profile.subjects.all() if class_profile else []

                # Get classmates within the same school
                class_students = assigned_class.students.filter(school=school)
                female_classmates = class_students.filter(gender='female')
                male_classmates = class_students.filter(gender='male')

                # Populate context
                context.update({
                    'classmates_count': class_students.count(),
                    'female_classmates': female_classmates.count(),
                    'male_classmates': male_classmates.count(),
                    'assigned_class': assigned_class,
                    'subjects': subjects
                })

                return render(request, 'customadmin/dashboard/student_dashboard.html', context)

        except StudentProfile.DoesNotExist:
            pass

        return render(request, 'customadmin/dashboard/student_dashboard.html', context)

#-----------------------------------------Teacher Dashboard-------------------------------------


    if request.user.groups.filter(name='teacher').exists():
            try:
                profile = TeacherProfile.objects.get(teacher=request.user)
                school =  profile.school
                my_assigned_class = profile.assigned_class
                
                # Get Classes and Students for Teacher
                my_classes = profile.classes_taught.all()
                my_classes_students = []
                for class_ in my_classes:
                    students = class_.students.all()
                    female_students = students.filter(gender='female')
                    male_students = students.filter(gender='male')
                    students_count = students.count()
                    my_classes_students.append({
                        'class_': class_,
                        'students': students,
                        'female_students': female_students,
                        'students_count': students_count,
                        'male_students': male_students,
                    })
                
                context = {
                    'my_classes_students': my_classes_students,
                    'my_subjects': profile.subjects_taught.all(),
                    'my_assigned_class':my_assigned_class
                }

                return render(request, 'customadmin/dashboard/teacher_dashboard.html', context)

            except TeacherProfile.DoesNotExist:
                logger.error("TeacherProfile does not exist for user: %s", request.user)
                messages.error(request, "Teacher profile not found.")
                return redirect('error_page')  # Replace 'error_page' with the actual error page URL name

       
#---------------------------------school_admin dashboard---------------------------------------

    elif request.user.groups.filter(name='school_admin').exists():
        try:
            logger.info(f"User {request.user} is in 'school_admin' group.")
            
            # Get SchoolAdminProfile and validate
            profile = SchoolAdminProfile.objects.filter(school_admin=request.user).select_related('school').first()
           
            
            if not profile.is_complete:
                return redirect('schoolAdmin_profile', profile_id=profile.id)
            
            # Ensure profile.school is not None
            if not profile.school:
                context['error'] = "No school associated with this admin profile."
                return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)

            # Query SchoolProfile using the school from SchoolAdminProfile
            school_profile = SchoolProfile.objects.filter(school=profile.school).first()
            if not school_profile:
                return redirect('setup_landing')

            if not school_profile.is_setup_complete:
                return redirect('setup_landing')

            # Collect dashboard data using optimized queries
            school_data = SchoolProfile.objects.filter(school=profile.school).annotate(
                subject_count=Count('schoolsubject', distinct=True),
                student_count=Count('studentprofile', distinct=True),
                male_count=Count('studentprofile', filter=Q(studentprofile__gender='male'), distinct=True),
                female_count=Count('studentprofile', filter=Q(studentprofile__gender='female'), distinct=True),
                teacher_count=Count('teacher_profiles', distinct=True),
                class_count=Count('classname', distinct=True)
            ).first()

            if not school_data:
                context['error'] = "School data not found."
                return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)

            # Prepare context
            context.update({
                'school': school_data,
                'all_teachers': school_data.teacher_count,
                'students_count': school_data.student_count,
                'male_count': school_data.male_count,
                'female_count': school_data.female_count,
                'classes': school_data.class_count,
                'subject_count': school_data.subject_count,
            })
            return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)
        
        except Exception as e:
                logger.error(f"Error processing the school admin dashboard: {str(e)}", exc_info=True)
                context['error'] = "An unexpected error occurred. Please try again later."
                return render(request, 'customadmin/dashboard/school_admin_dashboard.html', context)#-----------------------------------------deputy_head dashboard-------------------------------------------     
    

    elif request.user.groups.filter(name='deputy_head').exists():
                # Show deputy_head_dashboard
        return render(request, 'customadmin/dashboard/deputy_head_dashboard.html')
            
    elif request.user.groups.filter(name='school_head').exists():
                # Show school_head_dashboard
        return render(request, 'customadmin/dashboard/school_head_dashboard.html')
    
    #----------------------------------------------------------------------------------------
        
    elif request.user.groups.filter(name='district_admin').exists():
        # Show district_admin_dashboard
        return render(request, 'customadmin/dashboard/district_admin_dashboard.html')
    
    else:
        # Check if there is any district admin, if not, redirect to secure high school setup
        if not CustomUser.objects.filter(groups__name='district_admin').exists():
            return redirect('register_district_admin')
    
    #----------------------------------------------------------------------------------------
    # Show default dashboard
    return render(request, 'customadmin/dashboard/district_admin_dashboard.html')
    

@login_required
def login_redirect(request):
    user = request.user
    print(f"User: {user.email}, Groups: {user.groups.all()}")
    # Debugging statement
    if request.user.groups.filter(name='student').exists():
        return redirect('student_dashboard')
    
    elif request.user.groups.filter(name='teacher').exists():
        return redirect('teacher_dashboard')
    
    elif request.user.groups.filter(name='school_admin').exists():
        return redirect('school_admin_dashboard')
    
    elif request.user.groups.filter(name='deputy_head').exists():
        return redirect('deputy_head_dashboard')
    
    elif request.user.groups.filter(name='school_head').exists():
        return redirect('school_head_dashboard')
    
    elif request.user.groups.filter(name='district_admin').exists():
        return redirect('district_admin_dashboard')
    
    elif request.user.is_superuser:
        return redirect('district_admin_dashboard')
    
    else:
        return redirect('default_dashboard')
    
def  registration_complete(request):
    return render(request,'customadmin/registration_complete.html')

def error_page(request):
    return render(request,'customadmin/error_page.html')
