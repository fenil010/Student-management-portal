from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    BRANCH_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Electronics', 'Electronics'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Electrical', 'Electrical'),
        ('Information Technology', 'Information Technology'),
    ]

    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(default='student@example.com')
    roll_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    admission_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    subject = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Grade(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
        ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
        ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
        ('D', 'D'), ('F', 'F'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=30)  # Midterm, Final, Quiz, Assignment
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES)
    max_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.grade}"

    @property
    def percentage(self):
        return (self.obtained_marks / self.max_marks) * 100


class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]

    FEE_TYPE_CHOICES = [
        ('Tuition', 'Tuition Fee'),
        ('Hostel', 'Hostel Fee'),
        ('Library', 'Library Fee'),
        ('Lab', 'Laboratory Fee'),
        ('Other', 'Other'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    paid_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.student.name} - {self.fee_type} - ₹{self.amount}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EmailVerification(models.Model):
    """Model to store email verification tokens for new signups"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        """Token expires after 24 hours"""
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"Verification for {self.user.username}"
