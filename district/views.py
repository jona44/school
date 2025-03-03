import logging
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from customadmin.models import CustomUser
from .models import*
from .forms import   *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger(__name__)
from .models import GradeLevel
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from teacher.models import TeacherProfile



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def register_school_admin(request):
    form = SchoolAdminRegistrationForm()

    if request.method == 'POST':
        form = SchoolAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until activation
            user.user_type = 'school_admin'  # Set user_type to school_admin
            user.save()

            # Assign the user to the 'school_admin' group
            group_name = 'school_admin'
            
            desired_group = Group.objects.get(name=group_name)
            user.groups.add(desired_group)

            # Send activation email
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            subject = 'Activate Your Account'
            message = render_to_string('district/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            })
            send_mail(
                subject,
                '',  # The message parameter will be used for the email body
                settings.EMAIL_HOST_USER,  # Replace with your email address
                [user.email],  # Send to the user's email address
                fail_silently=False,
                html_message=message,  # Pass the 'message' as HTML content
            )

            # Redirect to the profile creation view for school admin
            return redirect('assign_schoolAdmin', user_id=user.id)
        else:
            messages.error(request, 'Form submission failed. Please correct the errors below.')

    return render(request, 'district/register_school_admin.html', {'form': form})

logger = logging.getLogger(__name__)


#------------------------------------create_districtAdmin_profile----------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_districtAdmin_profile(request, user_id):
    
    # View to create a DistrictAdminProfile for a newly registered user.

    district_schools = District_School_Registration.objects.all()
    CustomUser = get_user_model()
    district_admin = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = DistrictAdminProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.district_admin = district_admin
            # Fetch the DistrictAdmin associated with the user:
           
            profile.district_admin = district_admin
            profile.save() 

            profile.district_schools.set(district_schools)
            profile.save() 

            return redirect('districtAdmin_profile_detail', profile_id=profile.id)
    else:
        form = DistrictAdminProfileForm()

    context = {
        'form': form,
        'district_admin': district_admin,
    }
    return render(request, 'district/create_district_admin_profile.html', context)



#--------------------------------create_schoolHead_profile-----------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_schoolHead_profile(request, user_id):
    # View for creating or updating a SchoolHead profile associated with a user.
    user = CustomUser.objects.get(pk=user_id)  # Get the user from the passed user_id
    
    # Check if a SchoolHead profile already exists for this user
    try:
        school_head = SchoolHeadProfile.objects.get(school_head=user)
        # Existing profile, display update form
        form = SchoolHeadProfileForm(instance=school_head)
        if request.method == 'POST':
            form = SchoolHeadProfileForm(request.POST, instance=school_head)
            if form.is_valid():
                # Set the user who updated the profile
                school_head = form.save(commit=False)
                school_head.created_by = request.user  # Track who updated the profile
                school_head.save()
                messages.success(request, f'{user.get_full_name()} profile updated successfully.')
                return redirect('schoolHead_profile_detail', profile_id=school_head.id)  # Redirect to the same view
    except SchoolHeadProfile.DoesNotExist:
        # No existing profile, display creation form
        form = SchoolHeadProfileForm(initial={'school_head': user})  # Set the initial school_head to the user
        if request.method == 'POST':
            form = SchoolHeadProfileForm(request.POST)
            if form.is_valid():
                school_head = form.save(commit=False)
                school_head.school_head = user
                school_head.created_by = request.user  # Track who created the profile
                school_head.save()
                messages.success(request, f'{user.get_full_name()} profile created successfully.')
                return redirect('schoolHead_profile_detail', profile_id=school_head.id)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'district/create_schoolHead_profile.html', context)



#----------------------------------- school_list---------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def school_list(request):
    schools = District_School_Registration.objects.all()
    return render(request, 'district/school_list.html', {'schools': schools})


#----------------------------------- school_detail-----------------------------------


def school_detail(request, school_id):
    school = get_object_or_404(District_School_Registration, pk=school_id)
    return render(request, 'district/school_detail.html', {'school': school})


#------------------------------- create_school---------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_school(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school=form.save(commit=False)
            school.created_by = request.user
            
            school.save()
            return redirect('school_detail', school_id=school.id)   # Redirect to a list of schools or relevant page
    else:
        form = SchoolRegistrationForm()
    return render(request, 'district/create_school.html', {'form': form})


#-------------------------------activation_sent---------------------------


def activation_sent(request):
    return render(request, 'district/activation_sent.html')  


#-------------------------------activate_account---------------------------


import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        # Decode the UID and fetch the user
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Log the activation attempt
        logger.info(f"Attempting to activate user with UID: {uid}")

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Activate the user account
            user.is_active = True
            user.save()

            # Log successful activation
            logger.info(f"User {user.email} activated successfully.")

            # Add a success message
            messages.success(request, 'Your account has been activated. Please set your password.')

            # Redirect to password reset view
            return redirect('account_reset_password')

        else:
            # Log invalid token
            logger.error(f"Invalid token for user with UID: {uid}")

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        # Log the exception
        logger.error(f"Invalid activation link: {e}")

    # Handle invalid activation links
    messages.error(request, 'Invalid activation link. Please contact support.')
    return redirect('home')  # Redirect to a safe page (e.g., home page)

#-------------------------------registration_complete---------------------------


def  registration_complete(request):
    return render(request,'district/registration_complete.html')

#------------------------------------create_subject---------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_subject(request):
    all_subjects = Subjects.objects.all()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject_name = form.cleaned_data['subjects'].strip().title()  # Clean and format input
            if not subject_name:
                 messages.error(request, "Subject name cannot be blank.")
                 return render(request, 'district/subject_form.html', {'form': form, 'all_subjects': all_subjects})

            # Check for duplicates (case-insensitive)
            if Subjects.objects.filter(subjects__iexact=subject_name).exists():
                messages.error(request, f"Subject '{subject_name}' already exists.")
                return render(request, 'district/subject_form.html', {'form': form, 'all_subjects': all_subjects})
            
            # If no duplicates, save the new subject
            subject = form.save(commit=False)
            subject.subjects = subject_name
            subject.save()
            messages.success(request, f"Subject '{subject_name}' created successfully.")

            return redirect('subject')
        else:
            messages.error(request, "Invalid form submission. Please check the form.")
            return render(request, 'district/subject_form.html', {'form': form, 'all_subjects': all_subjects})

    else:
        form = SubjectForm()

    return render(request, 'district/subject_form.html', {'form': form,'all_subjects':all_subjects})



#----------------------------districtAdmin_profile_detail---------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')

def districtAdmin_profile_detail(request, profile_id):
    
    """Displays the details of a DistrictAdminProfile."""
    
    profile = DistrictAdminProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'district/districtAdmin_profile_detail.html', context)



#---------------------------------schoolHead_profile_detail----------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def schoolHead_profile_detail(request, profile_id):
    
    """Displays the details of a DistrictAdminProfile."""
    
    profile = SchoolHeadProfile.objects.get(pk=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'district/schoolHead_profile_detail.html', context)

#-----------------------------------grade_level-----------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='district_admin').exists())
def grade_level(request):
    created_instances = []
    for choice in GradeLevel.GradeLevels.choices: 
        grade_level, created = GradeLevel.objects.get_or_create(grade_level=choice[0])
        if created:
            created_instances.append(f'Created GradeLevel instance for {choice[1]} ({choice[0]})')
        else:
            created_instances.append(f'GradeLevel instance for {choice[1]} ({choice[0]}) already exists')

    context = {
        'created_instances': created_instances
    }
    
    return render(request, 'district/grade_level.html', context)



def teacher_list_view(request):
    # Retrieve all teacher profiles
    teachers = TeacherProfile.objects.select_related('teacher', 'school', 'base_subject', 'assigned_class').all()

    # Get distinct schools and subjects
    distinct_schools = TeacherProfile.objects.values_list('school', 'school').distinct()
    distinct_subjects = TeacherProfile.objects.values_list('base_subject', 'base_subject').distinct()

    # Apply filters based on query parameters
    base_subject = request.GET.get('base_subject')
    school = request.GET.get('school')
    position = request.GET.get('position')
    assigned_class = request.GET.get('assigned_class')

    if base_subject:
        teachers = teachers.filter(base_subject__id=base_subject)
    if school:
        teachers = teachers.filter(school__id=school)
    if position:
        teachers = teachers.filter(position=position)
    if assigned_class:
        teachers = teachers.filter(assigned_class__id=assigned_class)

    # Render the results to the template
    context = {
        'teachers': teachers,
        'distinct_schools': distinct_schools,
        'distinct_subjects': distinct_subjects,
    }
    return render(request, 'district/all_teachers.html', context)


#-----------------------------------create_district-------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def create_district(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            district=form.save(commit=False)
            district.created_by = request.user
            district.save()
            return redirect('school_list')   # Redirect to a list of schools or relevant page
    else:
        form = DistrictForm()
    return render(request, 'district/create_district.html',  {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def register_school_head(request):
    form =SchoolHeadRegistrationForm()

    if request.method == 'POST':
        form =SchoolHeadRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until activation
            user.user_type = 'school_head'  # Set user_type to school_head
            user.save()

            # Assign the user to the 'school_head' group
            group_name = 'school_head'
            desired_group = Group.objects.get(name=group_name)
            user.groups.add(desired_group)

            # Send activation email
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            subject = 'Activate Your Account'
            message = render_to_string('district/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            })
            send_mail(
                subject,
                '',  # The message parameter will be used for the email body
                settings.EMAIL_HOST_USER,  # Replace with your email address
                [user.email],  # Send to the user's email address
                fail_silently=False,
                html_message=message,  # Pass the 'message' as HTML content
            )

            # Redirect to the profile creation view for school head
            return redirect('assign_schoolHead', user_id=user.id)
        else:
            messages.error(request, 'Form submission failed. Please correct the errors below.')

    return render(request, 'district/register_school_head.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def assign_schoolHead(request, user_id):
    """
    View to create a SchoolAdmin for a given CustomUser.
    """
    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = AssignSchoolHeadForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.school_admin = user  # Assign the CustomUser to the profile
            profile.save()
            messages.success(request, 'SchoolAdmin  created successfully.')
            return redirect('schoolAdmin_profile_detail',profile_id=profile.id)  # Redirect to profile details
    else:
        form = AssignSchoolHeadForm()

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'schoolconfig/assign_schoolAdmin.html', context)



logger = logging.getLogger(__name__)

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            logger.info(f"Password reset requested for user with email: {email}")

            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            subject = 'Password Reset Requested'
            message = render_to_string('account/password_reset.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            })
            send_mail(
                subject,
                '',  # The message parameter will be used for the email body
                settings.EMAIL_HOST_USER,  # Replace with your email address
                [user.email],  # Send to the user's email address
                fail_silently=False,
                html_message=message,  # Pass the 'message' as HTML content
            )
            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
        except User.DoesNotExist:
            logger.error(f"No user found with email: {email}")
            messages.error(request, 'No user found with this email address.')

    return render(request, 'district/password_reset.html')


# View to create a group
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['name']
            # Check if group already exists
            if not Group.objects.filter(name=group_name).exists():
                Group.objects.create(name=group_name)
                messages.success(request, f"Group '{group_name}' created successfully!")
                return redirect('create_group')  # Adjust the redirect as needed
            else:
                messages.error(request, f"Group '{group_name}' already exists.")
    else:
        form = GroupForm()
    
    groups = Group.objects.all()  # Fetch all groups
    return render(request, 'district/make_group.html', {'form': form, 'groups': groups})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def register_district_admin(request):
    form =DistrictAdminRegistrationForm()

    if request.method == 'POST':
        form =DistrictAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until activation
            user.user_type = 'district_admin'  # Set user_type to district_admin
            user.save()

            # Assign the user to the 'district_admin' group
            group_name = 'district_admin'
            desired_group = Group.objects.get(name=group_name)
            user.groups.add(desired_group)

            # Send activation email
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            subject = 'Activate Your Account'
            message = render_to_string('district/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': protocol,
            })
            send_mail(
                subject,
                '',  # The message parameter will be used for the email body
                settings.EMAIL_HOST_USER,  # Replace with your email address
                [user.email],  # Send to the user's email address
                fail_silently=False,
                html_message=message,  # Pass the 'message' as HTML content
            )

            # Redirect to the profile creation view for school head
            return redirect('create_districtAdmin_profile', user_id=user.id)
        else:
            messages.error(request, 'Form submission failed. Please correct the errors below.')

    return render(request, 'district/register_district_admin.html', {'form': form})
