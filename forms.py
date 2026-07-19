from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User, Student

class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address format."),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('Email address is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address format.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])


class StudentForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message="Full Name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email address format."),
        Length(max=120)
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(message="Phone Number is required."),
        Length(min=7, max=20, message="Phone number must be between 7 and 20 characters.")
    ])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('Computer Science', 'Computer Science'),
        ('Information Technology', 'Information Technology'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration')
    ], validators=[DataRequired(message="Department is required.")])
    
    semester = SelectField('Semester', choices=[
        ('', 'Select Semester'),
        ('1st Semester', '1st Semester'),
        ('2nd Semester', '2nd Semester'),
        ('3rd Semester', '3rd Semester'),
        ('4th Semester', '4th Semester'),
        ('5th Semester', '5th Semester'),
        ('6th Semester', '6th Semester'),
        ('7th Semester', '7th Semester'),
        ('8th Semester', '8th Semester')
    ], validators=[DataRequired(message="Semester is required.")])
    
    address = TextAreaField('Address', validators=[
        Length(max=500, message="Address cannot exceed 500 characters.")
    ])

    def __init__(self, *args, **kwargs):
        # We accept a student_id to exclude the current student from duplicate email checks during edits
        self.student_id = kwargs.pop('student_id', None)
        super(StudentForm, self).__init__(*args, **kwargs)

    def validate_email(self, email):
        query = Student.query.filter_by(email=email.data.strip().lower())
        if self.student_id:
            query = query.filter(Student.id != self.student_id)
        student = query.first()
        if student:
            raise ValidationError('A student with this email address is already registered.')
