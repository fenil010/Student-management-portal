from django.urls import path
from .views import home, add_student, student_list, student_detail, admin_dashboard

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_student, name='add_student'),
    path('students/', student_list, name='student_list'),
    path('student/<int:id>/', student_detail, name='student_detail'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]
