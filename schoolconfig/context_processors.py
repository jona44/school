import logging
from district.models import SchoolHeadProfile
from teacher.models import TeacherProfile
from student.models import StudentProfile
from schoolconfig.models import SchoolAdminProfile, SchoolProfile

def get_user_school_profile(user):
    try:
        if user.user_type == 'student':
            return StudentProfile.objects.get(student=user).school
        elif user.user_type == 'teacher':
            return TeacherProfile.objects.get(teacher=user).school
        elif user.user_type == 'school_admin':
            return SchoolAdminProfile.objects.get(school_admin=user).school
        elif user.user_type == 'school_head':
            return SchoolHeadProfile.objects.get(user=user).school
        
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist,
            SchoolAdminProfile.DoesNotExist, SchoolHeadProfile.DoesNotExist
            ) as e:
        # Handle the case where the profile does not exist
        return None
    return None

def school_profile(request):
    if request.user.is_authenticated:
        profile = get_user_school_profile(request.user)
        if profile:
            return {'school_profile': profile}
    return {}



logger = logging.getLogger(__name__)

def get_user_school_profile(user):
    try:
        if user.user_type == 'student':
            return StudentProfile.objects.get(student=user).school
        elif user.user_type == 'teacher':
            return TeacherProfile.objects.get(teacher=user).school
        elif user.user_type == 'school_admin':
            return SchoolAdminProfile.objects.get(school_admin=user).school
        elif user.user_type == 'school_head':
            return SchoolHeadProfile.objects.get(user=user).school
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist,
            SchoolAdminProfile.DoesNotExist, SchoolHeadProfile.DoesNotExist) as e:
        # Handle the case where the profile does not exist
        logger.warning(f"Profile not found for user {user}: {e}")
        return None
    return None

def school_info(request):
    """
    Adds school logo URL and school name to the template context.
    """
    context = {
        'school_logo_url': None,
        'school': None,
    }

    if not request.user.is_authenticated:
        return context

    try:
        school = get_user_school_profile(request.user)
        if school:
            context['school'] = school
            school_profile = SchoolProfile.objects.get(school=school)
            if school_profile.school_logo:
                context['school_logo_url'] = school_profile.school_logo.url
    except SchoolProfile.DoesNotExist:
        logger.warning(f"SchoolProfile not found for school {school}")
    except Exception as e:
        logger.error(f"Error retrieving school info: {e}", exc_info=True)

    return context