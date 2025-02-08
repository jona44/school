from urllib import request
from django.contrib.auth.models import Group
from district.models import SchoolHeadProfile
from student.models import  StudentProfile
from teacher.models import TeacherProfile
from customsettings.models import  SchoolAdminProfile, SchoolProfile


def get_user_school(user):
    # Check for user type and return the corresponding school attribute
    if user.groups.filter(name='student').exists():
        return StudentProfile.objects.get(student=user).school  # Use `student=user` and `school`
    
    elif user.groups.filter(name='teacher').exists():
        return TeacherProfile.objects.get(teacher=user).school
    
    elif user.groups.filter(name='school_admin').exists():
        return SchoolAdminProfile.objects.get(school_admin=user).school  # Adjust to match the field in SchoolProfile
    
    elif user.groups.filter(name='school_head').exists() or user.groups.filter(name='school_head').exists():
        return SchoolHeadProfile.objects.get(admin=user).school  # Adjust for school_head/deputy_head
    else:
        return None
    
    
def get_school_logo(user):
    """
    Retrieves the school logo URL for a given user.

    Args:
        user: The user object.

    Returns:
        The URL of the school logo if found, otherwise None.
    """
    if user.is_authenticated:
        try:
            # Check user type and get school from profile
            if hasattr(user, 'studentprofile'):
                school = user.studentprofile.school
            elif hasattr(user, 'teacherprofile'):
                school = user.teacherprofile.school
            elif hasattr(user, 'schoolheadprofile'):
                school = user.schoolheadprofile.school
            elif hasattr(user, 'schooladminprofile'):
                school = user.schooladminprofile.school
            else:
                # District admin or other user type without school
                return None

            if school and school.logo:
                return school.logo.url
            else:
                return None  # School or logo not found

        except Exception as e:
            # Handle exceptions (e.g., profile does not exist)
            print(f"Error retrieving school logo: {e}")
            return None
    else:
        return None  # User not authenticated    
