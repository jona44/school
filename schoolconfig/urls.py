from django.urls import path
from .import views


urlpatterns = [
    path('setup_landing/', views.setup_landing, name='setup_landing'),
    path('school_profile_create_step1/', views.school_profile_create_step1, name='school_profile_create_step1'),
    path('update_schoolprofile/<int:pk>/', views.update_schoolprofile, name='update_schoolprofile'),
    path('schoolprofile_details/<int:id>/', views.schoolprofile_details, name='schoolprofile_details'),
   
    path('class_name/', views.class_name, name='class_name'),
    path('setup_step7/', views.setup_step7, name='setup_step7'),
    path('select_school_subjects_step2/',views.select_school_subjects_step2,name='select_school_subjects_step2'),
    path('subject_list/',views.subject_list,name='subject_list'),
    path('edit_schoolsubjects/<int:pk>/', views.edit_schoolsubjects, name='edit_schoolsubjects'),
    path('all_classes/', views.all_classes,name='all_classes'),
    path('teacher_list/',views.teacher_list, name='teacher_list'),
    
    path('assign_schoolAdmin/<int:user_id>/', views.assign_schoolAdmin, name='assign_schoolAdmin'),
    
    path('schoolAdmin_profile_detail/<int:profile_id>/', views.schoolAdmin_profile_detail,name='schoolAdmin_profile_detail'),
    path('schoolAdmin_profile/<int:profile_id>/', views.schoolAdmin_profile, name='schoolAdmin_profile'),
    # New URL
    path('update_custom_user/<int:user_id>/', views.update_custom_user, name='update_custom_user'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('search_custom_user/', views.search_custom_user, name='search_custom_user'),

]
