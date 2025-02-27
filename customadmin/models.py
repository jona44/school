import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
import random
import string

def generate_unique_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,  password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name,  password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('student', 'STUDENT'),
        ('teacher', 'TEACHER'),
        ('school_admin', 'SCHOOL_ADMIN'),
        ('school_head', 'SCHOOL_HEAD'),
        ('district_admin', 'DISTRICT_ADMIN'),
    )

    email       = models.EmailField(unique=True)
    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    user_type   = models.CharField(max_length=30, choices=USER_TYPE)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_school_superuser = models.BooleanField(default=False)
    created_by  = models.ForeignKey(
        'self', null=True, blank=True, 
        on_delete=models.SET_NULL, 
        related_name='created_students'
    )  # Track who registered the student

    objects     = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


import random
import string
from django.contrib.auth.hashers import make_password

def save(self, *args, **kwargs):
    if not self.pk:  # Only on creation
        if not getattr(self, "is_superuser", False):  # Skip for superusers
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            self.activation_token = generate_unique_token()  # Ensure this function exists
            self.set_unusable_password()
            self.is_active = False  # Account not active until user sets password
            # Send activation email logic here...
        else:  # Superuser creation
            if not self.password:  # Ensure password is set manually if not provided
                random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                self.password = make_password(random_password)  # Hash random password
            self.is_active = True  # Superuser is immediately active

    super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'


