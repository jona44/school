from django.urls import path
from. import views


urlpatterns = [
    
    path('create_assignment/<int:subject_id>/', views.create_assignment, name='create_assignment'),
    path('update_assignment/<int:assignment_id>/', views.update_assignment, name='update_assignment'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments_list/<int:subject_id>/', views.assignments_list, name='assignments_list'),
    
    
]

