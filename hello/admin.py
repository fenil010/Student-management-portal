from django.contrib import admin
from .models import Student, Attendance, Grade, Fee, Notice

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'email', 'branch', 'semester', 'is_active']
    list_filter = ['branch', 'semester', 'is_active']
    search_fields = ['name', 'roll_number', 'email']
    ordering = ['name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'subject', 'status']
    list_filter = ['date', 'status', 'subject']
    search_fields = ['student__name']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'exam_type', 'grade', 'obtained_marks', 'max_marks', 'date']
    list_filter = ['subject', 'exam_type', 'grade']
    search_fields = ['student__name']

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount', 'due_date', 'status']
    list_filter = ['fee_type', 'status']
    search_fields = ['student__name']

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
