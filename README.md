# 🎓 Student Management System


![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Flowbite](https://img.shields.io/badge/Flowbite-1A56DB?style=for-the-badge&logo=flowbite&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge&logo=greensock&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5)

A comprehensive, modern, and user-friendly web application for managing student data, attendance, grades, fees, and notices. Built with Django, this system creates a seamless bridge between school administrators and students.

---

## ✨ Key Features

### 👨‍💼 For Administrators (Staff)
*   **📊 Interactive Dashboard**: Real-time overview of total students, active accounts, pending fees, and average grades.
*   **👥 Student Management**: Complete CRUD (Create, Read, Update, Delete) operations for student profiles.
*   **📝 Attendance Tracking**: Mark and monitor daily attendance (Present/Absent/Late).
*   **🎓 Grade Management**: Record and manage exam marks and grades.
*   **💰 Fee Management**: Track fee payments, generate pending lists, and update payment statuses.
*   **📢 Notice Board**: Create and publish important announcements for students.
*   **📈 Reports & Analytics**: Visual breakdown of student distribution by branch, fee collection stats, and academic performance.

### 👨‍🎓 For Students
*   **📱 Personal Dashboard**: A personalized view showing attendance percentage, GPA, and overdue fees at a glance.
*   **📅 Attendance History**: View detailed day-by-day attendance records.
*   **🏆 Academic Progress**: Track grades across all subjects and exams.
*   **💳 Fee Status**: Check payment history and pending dues.
*   **🔔 Real-time Notices**: Stay updated with the latest college announcements.

---

## 🛠️ Tech Stack
*   **Backend**: Django (Python)
*   **Frontend**: HTML5, Tailwind CSS
*   **UI Components**: Flowbite
*   **Animations**: GSAP (GreenSock)

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Student_sys
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Initialize the database and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Populate Demo Data (Important!)
Use the included script to clean the database and create test accounts (Admin & Students):
```bash
python populate_demo_data.py
```
*This script automatically creates a default admin and sample student data.*

### 6. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔐 Test Credentials

Use the following credentials to explore the different user roles after running `populate_demo_data.py`.

### 👑 Administrator Access
| Role | Username | Password |
|------|----------|----------|
| **Super Admin** | `admin` | `admin123` |

### 🎓 Student Access
| Student Type | Username | Password | Description |
|--------------|----------|----------|-------------|
| **Topper** | `alice` | `password123` | High grades, 90%+ attendance. |
| **Average** | `bob` | `password123` | Average performance, 70% attendance. |
| **Struggling** | `charlie` | `password123` | Low attendance, pending fees. |

---

## 📸 Screenshots
*(Add screenshots of your dashboard here)*

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

---

Made with ❤️ by Fenil
