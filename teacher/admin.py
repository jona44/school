from django.contrib import admin

from . models import  TeacherProfile,Assignment,AssignmentSubmission



admin.site.register(TeacherProfile)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
