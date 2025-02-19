from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from student.models import ClassRoom
from teacher.models import TeacherProfile
from .forms import *
from .models import *
from district.models import AcademicCalendar
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import filter_by_school 
from django.http import JsonResponse
from customadmin.models import CustomUser
from .forms import CustomUserSearchForm


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'District_admin')
def assign_schoolAdmin(request, user_id):
    """
    View to create a SchoolAdmin for a given CustomUser.
    """
    user = CustomUser.objects.get(pk=user_id)

    if request.method == 'POST':
        form = AssignSchoolAdminForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.school_admin = user  # Assign the CustomUser to the profile
            profile.save()
            messages.success(request, 'SchoolAdmin  created successfully.')
            return redirect('schoolAdmin_profile_detail',profile_id=profile.id)  # Redirect to profile details
    else:
        form = AssignSchoolAdminForm()

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'schoolconfig/assign_schoolAdmin.html', context)


#-------------------------------admin_profile----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def admin_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    profile = get_object_or_404(SchoolAdminProfile, user=user)
    return render(request, 'district/admin_profile.html', {'profile': profile})


#---------------------------schoolAdmin_profile_detail-------------------------------------


from django.shortcuts import get_object_or_404

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'district_admin')
def schoolAdmin_profile_detail(request, profile_id):
    """Displays the details of a SchoolAdminProfile."""
    profile = get_object_or_404(SchoolAdminProfile, id=profile_id)
   
    return render(request, 'schoolconfig/schoolAdmin_profile_detail.html', {'profile': profile})


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def school_profile_create_step1(request):
    """
    Handles the creation and updating of a school profile.
    Only allows one school profile per registered school.
    """
    # Get the SchoolAdminProfile associated with the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)

    # Get the registered school related to the logged-in school admin
    registered_school = school_admin_profile.school

    # Try to get an existing school profile for this school
    try:
        school_profile = SchoolProfile.objects.get(school=registered_school)
    except SchoolProfile.DoesNotExist:
        school_profile = None

    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES, instance=school_profile)  # Include request.FILES
        if form.is_valid():
            schoolprofile = form.save(commit=False)

            # Automatically set the school from the logged-in school admin's profile
            schoolprofile.school = registered_school

            schoolprofile.save()  # Save the SchoolProfile instance first
            # Assign many-to-many relationships
            selected_subjects_ids = form.cleaned_data.get('school_subjects')
            if selected_subjects_ids:
                schoolprofile.school_subjects.set(selected_subjects_ids)
            schoolprofile.save()
            return redirect('schoolprofile_details', id=schoolprofile.id)  # Redirect to a success page or another step
        else:
            print("Form is invalid:")
            print(form.errors)
    else:
        form = SchoolProfileForm(instance=school_profile)

    return render(request, 'schoolconfig/school_profile_form_step1.html', {
        'form': form,
        'registered_school': registered_school
    })
    
#---------------------------------schoolprofile_details------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def schoolprofile_details(request, id):
    # Get the SchoolAdminProfile associated with the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # Get the registered school related to the logged-in school admin
    registered_school = school_admin_profile.school
    print(registered_school)
    # Get the school profile associated with the registered school and the provided ID
    schoolprofile = get_object_or_404(SchoolProfile, school=registered_school, id=id)
    print(schoolprofile)
    return render(request, 'schoolconfig/schoolprofile_details.html', {'schoolprofile': schoolprofile})


#---------------------------------update_schoolprofile--------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def update_schoolprofile(request, pk):
    schoolprofile = get_object_or_404(SchoolProfile, pk=pk)
    if request.method == 'POST':
        form = SchoolProfileForm(request.POST, request.FILES, instance=schoolprofile)
        if form.is_valid():
            
            form.save()
            return redirect('schoolprofile_details',id=schoolprofile.id)
    else:
        form = SchoolProfileForm(instance=schoolprofile)
    return render(request, 'schoolconfig/update_schoolprofile.html', {'form': form})


#-----------------------------------create_schoolsubjects_step2------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def select_school_subjects_step2(request):
    """
    Handles the creation of SchoolSubject instances for a specific school.

    Ensures each SchoolSubject instance is created per subject.
    """
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    registered_school = school_admin_profile.school

    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data['school_subjects']

            # Ensure the school profile exists
            school_profile, _ = SchoolProfile.objects.get_or_create(school=registered_school)

            # Delete existing subject relations (optional: only remove subjects not in the new selection)
            SchoolSubject.objects.filter(school=school_profile).delete()

            # Create a SchoolSubject instance and assign subjects properly
            school_subject = SchoolSubject.objects.create(school=school_profile)
            school_subject.subjects.add(*subjects)
            school_subject.save()

            return redirect('subject_list')
    else:
        form = SchoolSubjectForm()

    return render(request, 'schoolconfig/select_school_subjects_step2.html', {'form': form})


         
def subject_list(request, pk=None):
    # Get the school admin profile for the logged-in user
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    # Get the registered school related to the logged-in school admin
    current_school = school_admin_profile.school
    school  = SchoolProfile.objects.get(school=current_school)
    all_subjects = SchoolSubject.objects.filter(school=school)

    # Get the primary key of the first school subject (if exists)
    pk = all_subjects.first().pk if all_subjects else None

    return render(request, 'schoolconfig/subject_list.html', {'all_subjects': all_subjects, 'pk': pk})         


#-------------------------- edit_schoolsubjects------------------------------------------

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def edit_schoolsubjects(request, pk):
    school_subject = get_object_or_404(SchoolSubject, pk=pk)

    # Ensure the logged-in admin can only edit subjects from their school
    profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    if school_subject.school != profile.school:
        return render(request, 'schoolconfig/error.html', {'message': 'Unauthorized access.'})

    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST, instance=school_subject)
        if form.is_valid():
            edited = form.save(commit=False)
            edited.save()
            form.save_m2m()  # Ensure ManyToMany relations are saved
            return redirect('subject_list')  # Update with actual URL name
    else:
        form = SchoolSubjectForm(instance=school_subject)

    return render(request, 'schoolconfig/edit_schoolsubjects.html', {'form': form})

#-----------------------------------ClassName----------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def class_name(request):
    """
    View to manually create class names based on GradeLevels and SchoolName
    """
    # Retrieve the SchoolAdminProfile for the logged-in user
    profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    school = profile.school  # This should be a SchoolProfile instance
    registered_school = SchoolProfile.objects.filter(school=school).first()
                                               # Ensure there's a current academic year defined
    try:
        academic_year = AcademicCalendar.objects.get(is_current=True)
    except AcademicCalendar.DoesNotExist:
        messages.error(request, "No current academic year found. Please define one.")
        return redirect('class_name')  # Or handle the error differently

    if request.method == 'POST':
        form = ClassNameForm(request.POST)
        if form.is_valid():
            grade_level = form.cleaned_data['grd_level']
            classname = form.cleaned_data['classname']

            # Check if the class name already exists for the combination
            existing_class = ClassName.objects.filter(
                schoolprofile=registered_school,
                grd_level=grade_level,
                classname=classname,
                academic_year=academic_year
            ).first()

            if existing_class:
                messages.error(request, "Class name already exists.")
            else:
                new_class = ClassName(
                    schoolprofile=registered_school,
                    grd_level=grade_level,
                    classname=classname,
                    academic_year=academic_year
                )
                new_class.save()
                messages.success(request, "Class name has been created successfully.")
                return redirect('class_name')
    else:
        form = ClassNameForm()
        allclasses = ClassName.objects.filter(schoolprofile=registered_school)
    return render(request, 'schoolconfig/class_name.html', {'form': form, 'allclasses':allclasses})

#-----------------------------------is_setup_complete------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='school_admin').exists())
def setup_step7(request):
    try:
        # Get the SchoolAdminProfile associated with the current user
        school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
        registered_school = school_admin_profile.school
        # Retrieve the existing SchoolName instance associated with the SchoolAdminProfile
        try:
            school = SchoolProfile.objects.get(school=registered_school)
        except SchoolProfile.DoesNotExist:
            # Handle the case where no SchoolName instance exists
            return render(request, 'schoolconfig/setup_step6.html', {
                'error': 'No SchoolName instance found for the current SchoolAdminProfile.'
            })
        
        if request.method == 'POST':
            school.is_setup_complete = True
            school.save()
            return redirect('school_admin_dashboard')
    
    except SchoolAdminProfile.DoesNotExist:
        # Handle the case where the SchoolAdminProfile does not exist
        return render(request, 'schoolconfig/setup_step6.html', {
            'error': 'SchoolAdminProfile not found for the current user.'
        })

    return render(request, 'schoolconfig/setup_step7.html')

#-----------------------------all_classes------------------------------------------------------


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def all_classes(request):
    # Get the school assigned to the current school admin
    school_admin_profile = get_object_or_404(SchoolAdminProfile, school_admin=request.user)
    assigned_school = school_admin_profile.school
    school = SchoolProfile.objects.get(school=assigned_school)
    # Filter classrooms by the students' school
    classes = ClassRoom.objects.filter(school=school).distinct().select_related('name__grd_level')
    myclasses = classes.count()

    grade_level_data = {}
    for classroom in classes:
        class_students = classroom.students.all()
        total_students = class_students.count()
        male_count = class_students.filter(gender='male').count()
        female_count = class_students.filter(gender='female').count()
        grade_level = classroom.name.grd_level
        if grade_level not in grade_level_data:
            grade_level_data[grade_level] = []
        
        # Calculate percentage of female and male students
        total_count = male_count + female_count
        female_percentage = (female_count / total_count) * 100 if total_count > 0 else 0
        male_percentage = (male_count / total_count) * 100 if total_count > 0 else 0
        
        # Include classroom PK in the context data
        grade_level_data[grade_level].append({
            'classroom_pk': classroom.pk,  
            'classroom': classroom,
            'total_students': total_students,
            'male_count': male_count,
            'female_count': female_count,
            'female_percentage': female_percentage,
            'male_percentage': male_percentage,
        })
        print(assigned_school)
    return render(request, 'schoolconfig/all_classes.html', {'grade_level_data': grade_level_data,'myclasses':myclasses})


from django.db.models import Q

@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def teacher_list(request):
    # Get the school associated with the logged-in school admin
    school_admin = SchoolAdminProfile.objects.get(school_admin=request.user)
    the_school = school_admin.school
     
    school= SchoolProfile.objects.get(school=the_school)
    # Base queryset
    all_teachers = TeacherProfile.objects.filter(school=school)

    # Apply filters based on query parameters
    base_subject = request.GET.get('base_subject')
     # Assuming gender is an attribute of the teacher's CustomUser model
    on_medical_leave = request.GET.get('on_medical_leave')
    on_vocational_leave = request.GET.get('on_vocational_leave')

    if base_subject:
        all_teachers = all_teachers.filter(base_subject__id=base_subject)
    if on_medical_leave:
        all_teachers = all_teachers.filter(on_medical_leave=(on_medical_leave == 'true'))
    if on_vocational_leave:
        all_teachers = all_teachers.filter(on_vocational_leave=(on_vocational_leave == 'true'))

    context = {
        'all_teachers': all_teachers,
        'base_subject': SchoolSubject.objects.all(),
    }
    return render(request, 'schoolconfig/teacher_list.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type in ['District_admin', 'school_admin'])
def schoolAdmin_profile(request, profile_id):
    """
    View to update a SchoolAdminProfile for a given CustomUser.
    """
    profile = get_object_or_404(SchoolAdminProfile, pk=profile_id)
    user = profile.school_admin

    if request.method == 'POST':
        form = SchoolAdminProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_complete = True  # Set is_complete to True
            profile.save()
            messages.success(request, 'SchoolAdmin Profile updated successfully.')
            return redirect('schoolAdmin_profile_detail', profile_id=profile.id)  # Redirect to profile details
    else:
        form = SchoolAdminProfileForm(instance=profile)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'schoolconfig/update_schoolAdmin_profile.html', context)

def setup_landing(request):
    return render(request, 'schoolconfig/setup_landing.html')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def update_custom_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_detail', user_id=user.id)  # Redirect to user detail view
    else:
        form = CustomUserUpdateForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'schoolconfig/update_custom_user.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'school_admin')
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'schoolconfig/user_detail.html', {'user': user})



@login_required
def search_custom_user(request):
    if request.method == 'GET':
        form = CustomUserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            users = CustomUser.objects.filter(email__icontains=query) | CustomUser.objects.filter(first_name__icontains=query) | CustomUser.objects.filter(last_name__icontains=query)
            results = [{'id': user.id, 'name': f'{user.first_name} {user.last_name}', 'email': user.email} for user in users]
            return JsonResponse({'results': results})
    return JsonResponse({'results': []})