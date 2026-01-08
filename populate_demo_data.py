
import os
import random
import django
from datetime import datetime, timedelta
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project1.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from hello.models import Student, Attendance, Grade, Fee, Notice

def populate():
    print("🧹 Cleaning database...")
    # Delete all data except superusers
    Student.objects.all().delete()
    Attendance.objects.all().delete()
    Grade.objects.all().delete()
    Fee.objects.all().delete()
    Notice.objects.all().delete()
    
    # Remove non-superuser accounts to keep it clean
    User.objects.filter(is_superuser=False).delete()
    
    print("✨ Creating Demo Data...")

    # ==========================================
    # 1. Create Notices
    # ==========================================
    notices = [
        ("Mid-Semester Exam Schedule", "The mid-semester examinations will commence from October 15th. Detailed schedule is attached on the notice board."),
        ("Diwali Holidays", "The college will remain closed for Diwali break from Nov 1st to Nov 7th. Classes resume on Nov 8th."),
        ("TechFest 2026 Registration", "Registrations for the annual TechFest are now open. Visit the student council office to sign up."),
        ("Library Due Date Extension", "Due to system maintenance, all library book returns due this week are extended by 2 days."),
        ("Campus Recruitment Drive", "TCS and Infosys will be visiting campus next Monday. Final year students please update your resumes.")
    ]
    
    for title, content in notices:
        Notice.objects.create(title=title, content=content)
    print(f"   Created {len(notices)} notices")

    # ==========================================
    # 2. Define Hero Students (for Demo)
    # ==========================================
    hero_students = [
        {
            "username": "alice",
            "name": "Alice Topper",
            "roll": "CS1001",
            "branch": "Computer Science",
            "sem": 4,
            "type": "topper", # High attendance, good grades
            "email": "alice@student.com"
        },
        {
            "username": "bob",
            "name": "Bob Average",
            "roll": "ME2005",
            "branch": "Mechanical",
            "sem": 6,
            "type": "average", # Medium attendance, mixed grades
            "email": "bob@student.com"
        },
        {
            "username": "charlie",
            "name": "Charlie Late",
            "roll": "EC3042",
            "branch": "Electronics",
            "sem": 2,
            "type": "struggling", # Low attendance, fees due
            "email": "charlie@student.com"
        }
    ]

    # Names for background students
    first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohan", "Kavita", "Aditya", "Neha", "Suresh", "Pooja", "Arjun", "Divya", "Karan"]
    last_names = ["Sharma", "Patel", "Verma", "Singh", "Gupta", "Kumar", "Yadav", "Reddy", "Nair", "Iyer", "Das", "Chopra", "Malhotra", "Jain", "Mehta"]

    students_to_create = hero_students.copy()
    
    # Add 17 random students
    for i in range(17):
        first = random.choice(first_names)
        last = random.choice(last_names)
        students_to_create.append({
            "username": f"user{i+100}",
            "name": f"{first} {last}",
            "roll": f"XY{1000+i}",
            "branch": random.choice([b[0] for b in Student.BRANCH_CHOICES]),
            "sem": random.randint(1, 8),
            "type": "random",
            "email": f"{first.lower()}{i}@student.com"
        })

    # ==========================================
    # 3. Create Students & Related Data
    # ==========================================
    password = "password123"
    
    subjects = ["Mathematics", "Physics", "Data Structures", "Algorithms", "Database Systems", "Operating Systems", "Electronics"]
    
    for data in students_to_create:
        # Create User
        user = User.objects.create_user(username=data['username'], email=data['email'], password=password)
        
        # Create Student Profile
        student = Student.objects.create(
            user=user,
            name=data['name'],
            roll_number=data['roll'],
            email=data['email'],
            phone=f"98765{random.randint(10000, 99999)}",
            branch=data['branch'],
            semester=data['sem'],
            address=f"{random.randint(1, 99)}, College Road, City",
            is_active=True
        )
        
        # --- Generate Attendance (Last 30 days) ---
        today = timezone.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            if date.weekday() >= 5: continue # Skip weekends
            
            # Determine status based on student type
            if data['type'] == 'topper':
                status = 'Present' if random.random() > 0.05 else 'Absent'
            elif data['type'] == 'average':
                status = 'Present' if random.random() > 0.2 else 'Absent'
            elif data['type'] == 'struggling':
                status = 'Present' if random.random() > 0.4 else 'Absent'
            else:
                status = 'Present' if random.random() > 0.15 else 'Absent'
                
            # Random 'Late' status
            if status == 'Present' and random.random() < 0.1:
                status = 'Late'
                
            Attendance.objects.create(
                student=student,
                date=date,
                status=status,
                subject="General Class"
            )

        # --- Generate Grades ---
        num_grades = random.randint(3, 6)
        for i in range(num_grades):
            subj = random.choice(subjects)
            exam = random.choice(["Midterm", "Final", "Quiz 1", "Assignment"])
            
            if data['type'] == 'topper':
                marks = random.randint(85, 100)
                grade_char = 'A+' if marks > 90 else 'A'
            elif data['type'] == 'average':
                marks = random.randint(60, 85)
                grade_char = random.choice(['B+', 'B', 'B-', 'A-'])
            elif data['type'] == 'struggling':
                marks = random.randint(35, 65)
                grade_char = random.choice(['C+', 'C', 'D', 'F'])
            else:
                marks = random.randint(50, 95)
                grade_char = random.choice(['A', 'B', 'C', 'B+'])
                
            Grade.objects.create(
                student=student,
                subject=subj,
                exam_type=exam,
                grade=grade_char,
                max_marks=100,
                obtained_marks=marks
            )

        # --- Generate Fees ---
        fee_types = [
            ('Tuition', 50000), 
            ('Hostel', 25000), 
            ('Library', 2000)
        ]
        
        for f_type, amt in fee_types:
            # Set status
            if data['type'] == 'topper':
                status = 'Paid'
            elif data['type'] == 'struggling':
                status = random.choice(['Pending', 'Overdue'])
            else:
                status = random.choice(['Paid', 'Paid', 'Pending'])
                
            fee = Fee.objects.create(
                student=student,
                fee_type=f_type,
                amount=amt,
                due_date=today + timedelta(days=random.randint(-30, 30)),
                status=status
            )
            
            if status == 'Paid':
                fee.paid_date = today - timedelta(days=random.randint(1, 20))
                fee.transaction_id = f"TXN{random.randint(100000, 999999)}"
                fee.save()

    # ==========================================
    # 4. Create Admin User
    # ==========================================
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@school.com", "admin123")
        print("   Created default admin (admin/admin123)")
    else:
        print("   Admin account already exists")

    print(f"   Created {len(students_to_create)} students with full data.")
    print("\n✅ DATA POPULATION COMPLETE")
    print("------------------------------------------------")
    print("Demo Accounts:")
    print("1. Admin:    admin / admin123")
    print("2. Topper:   alice / password123")
    print("3. Average:  bob / password123")
    print("4. Late:     charlie / password123")
    print("------------------------------------------------")

if __name__ == '__main__':
    populate()
