from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import uuid
from .models import Student, Attendance, Grade, Fee, Notice, EmailVerification

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
            # Check if email is verified
            try:
                verification = EmailVerification.objects.get(user=user)
                if not verification.is_verified:
                    return render(request, 'login.html', {'error': 'Please verify your email before logging in. Check your inbox.'})
            except EmailVerification.DoesNotExist:
                pass  # Old users without verification can login
            
            login(request, user)
            # Check if user is admin (staff) or student
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                # Check if user has a student profile
                try:
                    Student.objects.get(user=user)
                    return redirect('student_dashboard')
                except Student.DoesNotExist:
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


# ============= EMAIL VERIFICATION HELPER =============

def send_verification_email(user, request):
    """Send verification email to the user"""
    token = str(uuid.uuid4())
    
    # Create or update verification record
    EmailVerification.objects.update_or_create(
        user=user,
        defaults={'token': token, 'is_verified': False}
    )
    
    # Build verification URL
    verification_url = request.build_absolute_uri(f'/verify-email/{token}/')
    
    # Email content
    subject = 'Verify Your StudentSys Account'
    message = f'''
Hello {user.first_name or user.username},

Welcome to StudentSys! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create an account, please ignore this email.

Best regards,
StudentSys Team
'''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


# ============= STUDENT SIGNUP =============

def student_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        phone = request.POST.get('phone')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        address = request.POST.get('address', '')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "student_signup.html", {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, "student_signup.html", {'error': 'Email already registered'})
        
        if Student.objects.filter(roll_number=roll_number).exists():
            return render(request, "student_signup.html", {'error': 'Roll number already registered'})
        
        # Create user (inactive until email verified)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name.split()[0] if name else '',
            last_name=' '.join(name.split()[1:]) if name else ''
        )
        
        # Create student profile
        Student.objects.create(
            user=user,
            name=name,
            email=email,
            roll_number=roll_number,
            phone=phone,
            branch=branch,
            semester=semester,
            address=address
        )
        
        # Send verification email
        if send_verification_email(user, request):
            return render(request, "email_verification_sent.html", {'email': email})
        else:
            # If email sending fails, delete the user and show error
            user.delete()
            return render(request, "student_signup.html", {'error': 'Failed to send verification email. Please try again.'})
    
    return render(request, "student_signup.html")


def verify_email(request, token):
    """Verify email using the token"""
    try:
        verification = EmailVerification.objects.get(token=token)
        
        if verification.is_expired():
            return render(request, "email_verification_result.html", {
                'success': False,
                'message': 'This verification link has expired. Please signup again.'
            })
        
        if verification.is_verified:
            return render(request, "email_verification_result.html", {
                'success': True,
                'message': 'Your email has already been verified. You can login now.'
            })
        
        # Mark as verified
        verification.is_verified = True
        verification.save()
        
        return render(request, "email_verification_result.html", {
            'success': True,
            'message': 'Your email has been verified successfully! You can now login.'
        })
        
    except EmailVerification.DoesNotExist:
        return render(request, "email_verification_result.html", {
            'success': False,
            'message': 'Invalid verification link.'
        })


# ============= TEACHER SIGNUP =============

def teacher_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        department = request.POST.get('department', 'Faculty')
        phone = request.POST.get('phone', '')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "teacher_signup.html", {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, "teacher_signup.html", {'error': 'Email already registered'})
        
        # Create user (teacher - not superuser, but staff for admin access)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True  # Allow admin access
        )
        
        # Login the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
    
    return render(request, "teacher_signup.html")


# ============= STUDENT DASHBOARD =============

@login_required
def student_dashboard(request):
    # Try to get student profile from the logged in user
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # If no student profile, redirect to admin dashboard
        return redirect('admin_dashboard')
    
    # Get full QuerySets for calculations
    all_attendance = student.attendances.all()
    all_grades = student.grades.all()
    all_fees = student.fees.all()
    notices = Notice.objects.filter(is_active=True)[:3]
    
    # Calculate stats on full QuerySets (before slicing)
    total_attendance = all_attendance.count()
    present_count = all_attendance.filter(status='Present').count()
    attendance_percentage = round((present_count / total_attendance * 100), 1) if total_attendance > 0 else 0
    
    avg_grade = all_grades.aggregate(avg=Avg('obtained_marks'))['avg'] or 0
    pending_fees = all_fees.filter(status='Pending').count()
    total_pending_amount = all_fees.filter(status='Pending').aggregate(total=Sum('amount'))['total'] or 0
    
    # Now slice for display (after calculating stats)
    attendance = all_attendance[:10]
    grades = all_grades[:10]
    fees = all_fees[:5]
    
    return render(request, "student_dashboard.html", {
        'student': student,
        'attendance': attendance,
        'grades': grades,
        'fees': fees,
        'notices': notices,
        'attendance_percentage': attendance_percentage,
        'avg_grade': round(avg_grade, 2),
        'pending_fees': pending_fees,
        'total_pending_amount': total_pending_amount
    })

