from django.contrib import admin
from schoolconfig.models import *

# Register your models here.
admin.site.register(SchoolProfile)
admin.site.register(SchoolSubject)
admin.site.register(GradeLevel)
admin.site.register(ClassName)
admin.site.register(SchoolAdminProfile)
admin.site.register(ClassProfile)

