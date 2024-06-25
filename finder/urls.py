from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path('logout/', views.user_logout, name='logout'),
    path("company_registration/", views.company_registration),
    path("company_login/", views.company_login, name='company_login'),
    path('add_job/', views.add_job, name='add_job'),
    path('company_profile/<int:comp_id>/', views.company_profile, name='company-profile'),
    path('my_joblist/<int:comp_id>/', views.my_joblist, name='my_joblist'),
    path('user_register/', views.user_register),
    path('user_login/', views.user_login, name='user_login'),
    path('user_job_list/', views.user_job_list, name='user_job_list'),
    path('student_profile/<int:stu_id>/', views.student_profile, name='student-profile'),
    path('job_details/<int:job_id>/', views.job_details, name='job_details'),
    path('edit_job/<int:job_id>/<int:comp_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),

]