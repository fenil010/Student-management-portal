from django.urls import path
from .views import (
    home, login_view, logout_view, admin_dashboard,
    student_list, student_detail, add_student, edit_student, delete_student,
    attendance_list, add_attendance,
    grade_list, add_grade,
    fee_list, add_fee, update_fee,
    notice_list, add_notice, delete_notice,
    reports
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # Student CRUD
    path('students/', student_list, name='student_list'),
    path('student/<int:id>/', student_detail, name='student_detail'),
    path('add/student/', add_student, name='add_student'),
    path('edit/student/<int:id>/', edit_student, name='edit_student'),
    path('delete/student/<int:id>/', delete_student, name='delete_student'),
    
    # Attendance CRUD
    path('attendance/', attendance_list, name='attendance_list'),
    path('add/attendance/', add_attendance, name='add_attendance'),
    
    # Grade CRUD
    path('grades/', grade_list, name='grade_list'),
    path('add/grade/', add_grade, name='add_grade'),
    
    # Fee CRUD
    path('fees/', fee_list, name='fee_list'),
    path('add/fee/', add_fee, name='add_fee'),
    path('update/fee/<int:id>/', update_fee, name='update_fee'),
    
    # Notice CRUD
    path('notices/', notice_list, name='notice_list'),
    path('add/notice/', add_notice, name='add_notice'),
    path('delete/notice/<int:id>/', delete_notice, name='delete_notice'),
    
    # Reports
    path('reports/', reports, name='reports'),
]
