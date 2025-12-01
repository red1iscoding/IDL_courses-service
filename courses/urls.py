from django.urls import path
from . import views

urlpatterns = [
    # Course endpoints
    path('add/', views.add_course, name='add_course'),
    path('getAll/', views.get_all_courses, name='get_all_courses'),
    path('get/<int:course_id>/', views.get_course, name='get_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('search/', views.search_courses, name='search_courses'),
    
    # Student-Course association endpoints
    path('enroll/', views.enroll_student, name='enroll_student'),
    path('unenroll/<int:enrollment_id>/', views.unenroll_student, name='unenroll_student'),
    path('enrollments/course/<int:course_id>/', views.get_course_enrollments, name='get_course_enrollments'),
    path('enrollments/student/<int:student_id>/', views.get_student_enrollments, name='get_student_enrollments'),
    path('courses-with-students/', views.get_courses_with_students, name='get_courses_with_students'),
]