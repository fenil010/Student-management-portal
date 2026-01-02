from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def home(request):
    return render(request, "home.html")


def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            roll_number=request.POST['roll'],
            branch=request.POST['branch'],
            semester=request.POST['semester']
        )
        return redirect('student_list')
    return render(request, "add_student.html")


def student_list(request):
    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})


def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "student_detail.html", {"student": student})


def admin_dashboard(request):
    total_students = Student.objects.count()
    return render(request, "admin_dashboard.html", {"total": total_students})
