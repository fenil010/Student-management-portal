from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Student, Attendance, Grade, Fee, Notice

def home(request):
    notices = Notice.objects.filter(is_active=True)[:5]
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    return render(request, "home.html", {
        'notices': notices,
        'total_students': total_students,
        'active_students': active_students
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    total_fees = Fee.objects.filter(status='Pending').count()
    avg_grade = Grade.objects.aggregate(avg=Avg('obtained_marks'))['avg'] or 0
    
    # Recent students
    recent_students = Student.objects.all().order_by('-admission_date')[:5]
    
    # Fee summary
    pending_fees = Fee.objects.filter(status='Pending')[:5]
    total_pending_amount = Fee.objects.filter(status='Pending').aggregate(total=Count('id'))['total']
    
    return render(request, "admin_dashboard.html", {
        'total_students': total_students,
        'active_students': active_students,
        'total_fees': total_fees,
        'avg_grade': round(avg_grade, 2),
        'recent_students': recent_students,
        'pending_fees': pending_fees,
    })


# ============= STUDENT CRUD =============

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})


@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    attendance = student.attendances.all()[:10]
    grades = student.grades.all()[:10]
    fees = student.fees.all()[:5]
    return render(request, "student_detail.html", {
        "student": student,
        "attendance": attendance,
        "grades": grades,
        "fees": fees
    })


@login_required
def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            roll_number=request.POST['roll_number'],
            phone=request.POST['phone'],
            branch=request.POST['branch'],
            semester=request.POST['semester'],
            address=request.POST['address'],
        )
        return redirect('student_list')
    return render(request, "add_student.html")


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.roll_number = request.POST['roll_number']
        student.phone = request.POST['phone']
        student.branch = request.POST['branch']
        student.semester = request.POST['semester']
        student.address = request.POST['address']
        student.is_active = 'is_active' in request.POST
        student.save()
        return redirect('student_detail', id=student.id)
    return render(request, "edit_student.html", {"student": student})


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, "delete_confirm.html", {"object": student, "type": "Student"})


# ============= ATTENDANCE CRUD =============

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, "attendance_list.html", {"attendances": attendances})


@login_required
def add_attendance(request):
    students = Student.objects.filter(is_active=True)
    if request.method == "POST":
        student = get_object_or_404(Student, id=request.POST['student_id'])
        Attendance.objects.create(
            student=student,
            date=request.POST['date'],
            status=request.POST['status'],
            subject=request.POST['subject'],
            remarks=request.POST.get('remarks', '')
        )
        return redirect('attendance_list')
    return render(request, "add_attendance.html", {"students": students})


# ============= GRADE CRUD =============

@login_required
def grade_list(request):
    grades = Grade.objects.all()
    return render(request, "grade_list.html", {"grades": grades})


@login_required
def add_grade(request):
    students = Student.objects.filter(is_active=True)
    if request.method == "POST":
        student = get_object_or_404(Student, id=request.POST['student_id'])
        Grade.objects.create(
            student=student,
            subject=request.POST['subject'],
            exam_type=request.POST['exam_type'],
            grade=request.POST['grade'],
            max_marks=request.POST['max_marks'],
            obtained_marks=request.POST['obtained_marks'],
        )
        return redirect('grade_list')
    return render(request, "add_grade.html", {"students": students})


# ============= FEE CRUD =============

@login_required
def fee_list(request):
    fees = Fee.objects.all()
    return render(request, "fee_list.html", {"fees": fees})


@login_required
def add_fee(request):
    students = Student.objects.filter(is_active=True)
    if request.method == "POST":
        student = get_object_or_404(Student, id=request.POST['student_id'])
        Fee.objects.create(
            student=student,
            fee_type=request.POST['fee_type'],
            amount=request.POST['amount'],
            due_date=request.POST['due_date'],
            status=request.POST['status'],
            paid_date=request.POST.get('paid_date'),
            transaction_id=request.POST.get('transaction_id', '')
        )
        return redirect('fee_list')
    return render(request, "add_fee.html", {"students": students})


@login_required
def update_fee(request, id):
    fee = get_object_or_404(Fee, id=id)
    if request.method == "POST":
        fee.status = request.POST['status']
        fee.paid_date = request.POST.get('paid_date')
        fee.transaction_id = request.POST.get('transaction_id', '')
        fee.save()
        return redirect('fee_list')
    return render(request, "update_fee.html", {"fee": fee})


# ============= NOTICE CRUD =============

@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, "notice_list.html", {"notices": notices})


@login_required
def add_notice(request):
    if request.method == "POST":
        Notice.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            is_active='is_active' in request.POST
        )
        return redirect('notice_list')
    return render(request, "add_notice.html")


@login_required
def delete_notice(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.method == "POST":
        notice.delete()
        return redirect('notice_list')
    return render(request, "delete_confirm.html", {"object": notice, "type": "Notice"})


# ============= REPORTS =============

@login_required
def reports(request):
    # Branch-wise student count
    branch_stats = Student.objects.values('branch').annotate(count=Count('id')).order_by('-count')
    
    # Fee collection summary
    fee_stats = Fee.objects.values('status').annotate(count=Count('id'))
    
    # Average grade by subject
    grade_stats = Grade.objects.values('subject').annotate(avg=Avg('obtained_marks'))
    
    return render(request, "reports.html", {
        'branch_stats': branch_stats,
        'fee_stats': fee_stats,
        'grade_stats': grade_stats
    })
