# Student Management System

A complete full-stack web application built using Python (Flask, SQLAlchemy ORM, SQLite) and a modern, responsive frontend (HTML5, CSS3 with Glassmorphism, Vanilla JS, and Jinja2).

## Technologies Used

- **Backend**: Python 3, Flask, SQLAlchemy ORM, SQLite database
- **Frontend**: HTML5, CSS3 (custom responsive styling), Vanilla JavaScript, Jinja2 Templates
- **Security**: Werkzeug secure password hashing, Flask session-based authentication, custom form validations, route-level protection

---

## Features

1. **User Authentication**
   - User registration with secure email validation and password matching.
   - Secure login with Werkzeug password hashing.
   - Route protection: Dashboard, Profiles, and Student CRUD operations are strictly restricted to logged-in users. Unauthenticated requests are redirected back to the login screen.
   - Logout and session clearance.

2. **Dashboard Overview**
   - Welcomes logged-in users with their email.
   - Displays real-time statistics: Total student count.
   - Lists the 5 most recently added student records.
   - Responsive sidebar and header navbars.

3. **Student Directory & CRUD Module**
   - **Create**: Add a student with Full Name, Email, Phone, Department, Semester, and Address.
   - **View**: A responsive table layout detailing all students.
   - **Search**: Dynamic case-insensitive search across name, email, phone, department, and semester.
   - **Edit**: Pre-populated updates for any student.
   - **Delete**: Safely delete a record with a custom modal confirmation.

4. **Data Validation**
   - Custom WTForms validation preventing duplicate email addresses.
   - Proper email formatting validation.
   - Comprehensive error reporting directly displayed underneath form fields.

---

## Setup & Running Instructions

Follow these steps to run the application on your system:

### 1. Navigate to the project directory
```powershell
cd "C:\Users\SWG\.gemini\antigravity\scratch\student-system"
```

### 2. Install dependencies
Install all required libraries using pip:
```powershell
pip install -r requirements.txt
```

### 3. Run the application
Run the Flask server script:
```powershell
python app.py
```

### 4. Access in your browser
Open your preferred web browser and navigate to:
```
http://127.0.0.1:5000/
```

- Click **Register Here** to create your first administrator credentials.
- Login with your registered email and password.
- Start managing students!

---

## Git Integration (GitHub)

The project directory has been initialized with a local Git repository. To push this application to your GitHub account:

1. Create a new repository on your GitHub account.
2. In your terminal, run the following commands:
```powershell
# Set main branch
git branch -M main

# Add your remote GitHub URL
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# Push the codebase to GitHub
git push -u origin main
```
