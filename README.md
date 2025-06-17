# Student Management System

A comprehensive web application for managing student records, academic performance, and communications in educational institutions.

## Overview

The Student Management System is designed to simplify administrative tasks in schools and colleges by providing a centralized platform for managing students, teachers, subjects, academic results, and communications. The system supports different user roles with specific permissions, ensuring data security and appropriate access levels.

## Features

### User Management
- Multiple user roles: Admin, Teacher, Student
- User registration and authentication using JWT
- Profile management
- Soft delete functionality for users

### Academic Management
- Subject creation and assignment
- Teacher assignment to subjects
- Student enrollment in subjects
- Grade tracking and management

### Assessment System
- Mark entry and management
- Result publishing
- Performance reports

### Communication
- Notice board functionality
- Role-specific notices (for students, teachers, or both)
- Notice creation and management

### Role-Specific Features
- **Admin Dashboard**: Complete system oversight, user management, subject creation, notice management
- **Teacher Dashboard**: Mark entry, student management, notice creation for students
- **Student Dashboard**: View assigned subjects, check published results, view notices

## Technology Stack

### Backend
- Python 3.x
- Django 5.x
- Django REST Framework
- Simple JWT for authentication
- SQLite/PostgreSQL

### Frontend
- Vue.js 3.x
- Vue Router
- Axios for API communication
- Tailwind CSS for styling

## Installation

### Prerequisites
- Python 3.x
- Node.js and npm
- Git

### Backend Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd Stud_managemnt_from-drf
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   cd Student_Managment_system
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```
   
6. The backend API will be available at http://127.0.0.1:8000/

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

4. The frontend application will be available at http://localhost:5173/

## API Endpoints

### Authentication
- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Users
- `GET /api/users/`: List all users
- `POST /api/users/`: Create new user
- `GET /api/users/{id}/`: Get user details
- `PATCH /api/users/{id}/`: Update user
- `DELETE /api/users/{id}/`: Soft delete user
- `PATCH /api/users/{id}/change-username/`: Change username
- `POST /api/users/{id}/restore/`: Restore soft-deleted user
- `GET /api/users/deleted/`: List soft-deleted users
- `GET /api/users/{id}/profile/`: Get user's profile

### Student Profiles
- `GET /api/student-profiles/`: List student profiles
- `POST /api/student-profiles/`: Create student profile
- `GET /api/student-profiles/{id}/`: Get student profile
- `PATCH /api/student-profiles/{id}/`: Update student profile
- `DELETE /api/student-profiles/{id}/`: Delete student profile
- `POST /api/student-profiles/{id}/assign-subjects/`: Assign subjects to student
- `GET /api/student-profiles/list-students/`: List all students

### Subjects
- `GET /api/subjects/`: List all subjects
- `POST /api/subjects/`: Create new subject
- `GET /api/subjects/{id}/`: Get subject details
- `PATCH /api/subjects/{id}/`: Update subject
- `DELETE /api/subjects/{id}/`: Delete subject
- `GET /api/subjects/unassigned/`: List unassigned subjects
- `GET /api/subjects/my-subjects/`: List teacher's assigned subjects

### Marks
- `GET /api/marks/`: List marks
- `POST /api/marks/`: Create marks
- `GET /api/marks/{id}/`: Get mark details
- `PATCH /api/marks/{id}/`: Update marks
- `DELETE /api/marks/{id}/`: Delete marks
- `POST /api/marks/publish/`: Publish marks
- `POST /api/marks/bulk-create/`: Create multiple marks at once

### Notices
- `GET /api/notices/`: List notices
- `POST /api/notices/`: Create notice
- `GET /api/notices/{id}/`: Get notice details
- `PATCH /api/notices/{id}/`: Update notice
- `DELETE /api/notices/{id}/`: Delete notice

## User Roles and Permissions

### Admin
- Full access to all system functionalities
- Can create, update, delete, and restore all users
- Can create and manage subjects
- Can view all student profiles and marks
- Can create notices for all user types

### Teacher
- Can update their own profile
- Can manage students enrolled in their subjects
- Can add and publish marks for their taught subjects
- Can assign their taught subjects to students
- Can create notices for students only
- Can edit and delete notices they created

### Student
- Can view their own profile and subjects
- Can view their published marks
- Can view notices meant for students
- Limited access to system information

## Usage Examples

### Admin Tasks
1. Create a new teacher account and assign subjects
2. Create student accounts and set up their profiles
3. Create new subjects and assign teachers
4. View and manage all users and academic data
5. Create notices for students, teachers, or both

### Teacher Tasks
1. View assigned subjects
2. Manage students enrolled in taught subjects
3. Enter and publish marks for students
4. Create notices for students
5. Update student information

### Student Tasks
1. View profile and assigned subjects
2. Check published academic results
3. View notices posted for students

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
