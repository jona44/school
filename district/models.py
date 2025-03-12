import datetime
import random
import uuid
from django.db import models
from customadmin.models import CustomUser


from django.conf import settings

class District(models.Model):
    district = models.CharField(max_length=255, unique=True)  # Ensure district names are unique
    # Track when the district was created
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Track who created the district

    def __str__(self):
        return self.district



from django.conf import settings

class District_School_Registration(models.Model):
    district      = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    school        = models.CharField(max_length=255, blank=True, null=True)
    address       = models.TextField(blank=True, null=True)
    phone_number  = models.CharField(max_length=20, blank=True, null=True)
    email         = models.EmailField(blank=True, null=True)
    created_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)  # Track who created the school registration

    def __str__(self):
        return f'{self.school}'
 


class DistrictAdminProfile(models.Model):
    district_admin   = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='district_admin_profile')
    district_name    = models.CharField(max_length=255,blank=True, null=True)
    contact_number   = models.CharField(max_length=255,blank=True, null=True)
    email            = models.EmailField(blank=True, null=True)
    district_schools = models.ManyToManyField(District_School_Registration)
    admin   = models.CharField(max_length=10,choices=[('admin1','admin1'),('admin2','admin2'),('admin3','admin3')],null=True,blank=True)

    def __str__(self):
        return f'{self.district_admin}' 
    
    
    
from django.conf import settings

class SchoolHeadProfile(models.Model):
    school_head    = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='SchoolHead_profile')
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    email          = models.EmailField(blank=True, null=True)
    school         = models.ForeignKey(District_School_Registration, on_delete=models.CASCADE, blank=True, null=True)
    address        = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth  = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='school_head_profiles/', blank=True, null=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    last_updated    = models.DateTimeField(auto_now=True)
    is_complete     = models.BooleanField(default=False)

    # Additional field to track who created the profile
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.school_head.first_name} {self.school_head.last_name} - {self.school}'

        
        
class SubjectsManager(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID Field
    subjects   = models.CharField(max_length=50, blank=True, null=True, unique=True)
    color = models.CharField(max_length=7, blank=True, null=True)  # Store the color code

    def __str__(self):
        return f'{self.subjects}'

    class Meta:
        verbose_name_plural = 'Subjects'

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = self.generate_random_color()
        super(SubjectsManager, self).save(*args, **kwargs)

    def generate_random_color(self):
        """Generates a random hex color code."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

        
        
class Holiday(models.Model):

    date = models.DateField()
    name = models.CharField(max_length=200)
    note = models.TextField()
   
    def __str__(self):
        return self.name         
        
        
class AcademicCalendar(models.Model):
    
    academic_year = models.PositiveIntegerField(default=datetime.datetime.now().year, blank=True, null=True)

    # Fields for each term
    term_1_start_date = models.DateField(blank=True, null=True)
    term_1_end_date   = models.DateField(blank=True, null=True)
    term_2_start_date = models.DateField(blank=True, null=True)
    term_2_end_date   = models.DateField(blank=True, null=True)
    term_3_start_date = models.DateField(blank=True, null=True)
    term_3_end_date   = models.DateField(blank=True, null=True)
    term_4_start_date = models.DateField(blank=True, null=True)
    term_4_end_date   = models.DateField(blank=True, null=True)
    holidays          = models.ManyToManyField(Holiday, related_name="academic_calendars")
    is_current        = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.academic_year}'    
    
    
class GradeLevel(models.Model):
    class GradeLevels(models.IntegerChoices):
        EIGHT  = 8, '8'
        NINE   = 9, '9'
        TEN    = 10, '10'
        ELEVEN = 11, '11'
        TWELVE = 12, '12'
        
    grade_level = models.IntegerField(choices=GradeLevels.choices)
   
    
    def __str__(self):
        return str(self.grade_level)    