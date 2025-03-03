from django.urls import path, include   
from . import views

urlpatterns = [
    path('create_assignment/<int:subject_id>/', views.create_assignment, name='create_assignment'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments_list/<int:subject_id>/', views.assignments_list, name='assignments_list'),
    path('assignment_submission/<int:assignment_id>/', views.assignment_submission, name='assignment_submission'),
    path('assignment_view/<int:assignment_id>/', views.assignment_view, name='assignment_view'),
    path('update_assignment/<int:assignment_id>/', views.update_assignment, name='update_assignment'),
    path('submitted_assignments/<int:classroom_id>/', views.submitted_assignments, name='submitted_assignments'),  # Add this line
]

