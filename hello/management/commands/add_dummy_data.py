from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hello.models import Student, Attendance, Grade, Fee, Notice
from datetime import datetime, timedelta
from random import randint, choice

class Command(BaseCommand):
    help = 'Add dummy data to the database for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating dummy data...'))
        
        # Create Users and Students
        students_data = [
            {'name': 'Amit Sharma', 'roll_number': '2023CS001', 'email': 'amit@student.edu', 'branch': 'Computer Science', 'semester': 3, 'phone': '+91 9876543210'},
            {'name': 'Priya Patel', 'roll_number': '2023CS002', 'email': 'priya@student.edu', 'branch': 'Computer Science', 'semester': 3, 'phone': '+91 9876543211'},
            {'name': 'Rahul Kumar', 'roll_number': '2023EC001', 'email': 'rahul@student.edu', 'branch': 'Electronics', 'semester': 5, 'phone': '+91 9876543212'},
            {'name': 'Sneha Gupta', 'roll_number': '2023ME001', 'email': 'sneha@student.edu', 'branch': 'Mechanical', 'semester': 1, 'phone': '+91 9876543213'},
            {'name': 'Vikram Singh', 'roll_number': '2023CV001', 'email': 'vikram@student.edu', 'branch': 'Civil', 'semester': 7, 'phone': '+91 9876543214'},
            {'name': 'Ananya Reddy', 'roll_number': '2023EE001', 'email': 'ananya@student.edu', 'branch': 'Electrical', 'semester': 2, 'phone': '+91 9876543215'},
            {'name': 'Rohan Mehta', 'roll_number': '2023IT001', 'email': 'rohan@student.edu', 'branch': 'Information Technology', 'semester': 4, 'phone': '+91 9876543216'},
            {'name': 'Kavitha Nair', 'roll_number': '2023CS003', 'email': 'kavitha@student.edu', 'branch': 'Computer Science', 'semester': 6, 'phone': '+91 9876543217'},
            {'name': 'Mohammed Ali', 'roll_number': '2023EC002', 'email': 'mohammed@student.edu', 'branch': 'Electronics', 'semester': 4, 'phone': '+91 9876543218'},
            {'name': 'Divya Krishnan', 'roll_number': '2023ME002', 'email': 'divya@student.edu', 'branch': 'Mechanical', 'semester': 8, 'phone': '+91 9876543219'},
        ]
        
        students = []
        for data in students_data:
            username = data['roll_number'].lower()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=data['email'],
                    password='password123'
                )
            else:
                user = User.objects.get(username=username)
            
            if not Student.objects.filter(roll_number=data['roll_number']).exists():
                student = Student.objects.create(
                    user=user,
                    name=data['name'],
                    email=data['email'],
                    roll_number=data['roll_number'],
                    phone=data['phone'],
                    branch=data['branch'],
                    semester=data['semester'],
                    address=f'{randint(1, 100)}, Sample Street, City - {randint(10000, 99999)}',
                    admission_date=datetime.now().date() - timedelta(days=randint(30, 365))
                )
                students.append(student)
                self.stdout.write(f'  Created student: {student.name}')
            else:
                students.append(Student.objects.get(roll_number=data['roll_number']))
        
        # Create Attendance Records
        subjects = ['Data Structures', 'Database Management', 'Web Development', 'Computer Networks', 'Operating Systems', 'Algorithms']
        attendance_data = []
        
        for student in students:
            for i in range(randint(5, 15)):
                date = datetime.now().date() - timedelta(days=randint(1, 90))
                status = choice(['Present', 'Present', 'Present', 'Absent', 'Late'])
                subject = choice(subjects)
                
                if not Attendance.objects.filter(student=student, date=date, subject=subject).exists():
                    attendance = Attendance.objects.create(
                        student=student,
                        date=date,
                        status=status,
                        subject=subject,
                        remarks='' if status == 'Present' else choice(['Medical leave', 'Personal work', 'Late due to traffic'])
                    )
                    attendance_data.append(attendance)
        
        self.stdout.write(f'  Created {len(attendance_data)} attendance records')
        
        # Create Grade Records
        exam_types = ['Assignment', 'Quiz', 'Midterm', 'Final']
        grade_data = []
        
        for student in students:
            for i in range(randint(4, 10)):
                subject = choice(subjects)
                exam_type = choice(exam_types)
                max_marks = 100 if exam_type == 'Final' else 50
                obtained_marks = randint(40, max_marks)
                percentage = (obtained_marks / max_marks) * 100
                
                if percentage >= 90:
                    grade = 'A+'
                elif percentage >= 85:
                    grade = 'A'
                elif percentage >= 80:
                    grade = 'A-'
                elif percentage >= 75:
                    grade = 'B+'
                elif percentage >= 70:
                    grade = 'B'
                elif percentage >= 65:
                    grade = 'B-'
                elif percentage >= 60:
                    grade = 'C+'
                elif percentage >= 55:
                    grade = 'C'
                elif percentage >= 50:
                    grade = 'C-'
                elif percentage >= 40:
                    grade = 'D'
                else:
                    grade = 'F'
                
                if not Grade.objects.filter(student=student, subject=subject, exam_type=exam_type).exists():
                    grade_record = Grade.objects.create(
                        student=student,
                        subject=subject,
                        exam_type=exam_type,
                        grade=grade,
                        max_marks=max_marks,
                        obtained_marks=obtained_marks,
                        date=datetime.now().date() - timedelta(days=randint(1, 60))
                    )
                    grade_data.append(grade_record)
        
        self.stdout.write(f'  Created {len(grade_data)} grade records')
        
        # Create Fee Records
        fee_types = ['Tuition', 'Hostel', 'Library', 'Lab', 'Other']
        fee_data = []
        
        for student in students:
            for i in range(3):
                fee_type = choice(fee_types)
                amount = choice([5000, 7500, 10000, 15000, 20000])
                due_date = datetime.now().date() + timedelta(days=randint(-30, 60))
                status = choice(['Paid', 'Paid', 'Pending', 'Overdue'])
                
                if not Fee.objects.filter(student=student, fee_type=fee_type, due_date=due_date).exists():
                    fee = Fee.objects.create(
                        student=student,
                        fee_type=fee_type,
                        amount=amount,
                        due_date=due_date,
                        status=status,
                        paid_date=datetime.now().date() - timedelta(days=randint(1, 30)) if status == 'Paid' else None,
                        transaction_id=f'TXN{randint(100000, 999999)}' if status == 'Paid' else ''
                    )
                    fee_data.append(fee)
        
        self.stdout.write(f'  Created {len(fee_data)} fee records')
        
        # Create Notice Records
        notices_data = [
            {'title': 'Mid Semester Exams Schedule', 'content': 'The mid-semester examinations will be conducted from next week. Please check the detailed schedule on the notice board and prepare accordingly.'},
            {'title': 'Library Book Return Deadline', 'content': 'All students are requested to return borrowed library books before the end of this month to avoid late fees.'},
            {'title': 'Annual Tech Fest 2024', 'content': 'Our annual tech fest "Innovation 2024" will be held next month. Register your teams for various competitions and showcase your talents!'},
            {'title': 'Hostel Fee Payment Reminder', 'content': 'This is a reminder for all hostel residents to pay their hostel fees before the due date to avoid any inconvenience.'},
            {'title': 'Guest Lecture on AI', 'content': 'We are organizing a guest lecture on "Artificial Intelligence in Modern Computing" by Dr. Smith from IIT. All students are encouraged to attend.'},
        ]
        
        for data in notices_data:
            if not Notice.objects.filter(title=data['title']).exists():
                notice = Notice.objects.create(
                    title=data['title'],
                    content=data['content'],
                    is_active=choice([True, True, True, False])
                )
                self.stdout.write(f'  Created notice: {notice.title}')
        
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total: {len(students)} students, {len(attendance_data)} attendance records, {len(grade_data)} grades, {len(fee_data)} fees'))

