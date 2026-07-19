from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from models import db, Student
from forms import StudentForm
from auth import login_required

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
@routes_bp.route('/dashboard')
@login_required
def dashboard():
    total_students = Student.query.count()
    # Fetch 5 most recently created students
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', total_students=total_students, recent_students=recent_students)


@routes_bp.route('/students')
@login_required
def view_students():
    search_query = request.args.get('search', '').strip()
    if search_query:
        # Case-insensitive search on name, email, department, semester, phone
        search_filter = f"%{search_query}%"
        students = Student.query.filter(
            (Student.name.ilike(search_filter)) |
            (Student.email.ilike(search_filter)) |
            (Student.phone.ilike(search_filter)) |
            (Student.department.ilike(search_filter)) |
            (Student.semester.ilike(search_filter))
        ).order_by(Student.name.asc()).all()
    else:
        students = Student.query.order_by(Student.name.asc()).all()
        
    return render_template('students.html', students=students, search_query=search_query)


@routes_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            department=form.department.data,
            semester=form.semester.data,
            address=form.address.data.strip() if form.address.data else ''
        )
        try:
            db.session.add(student)
            db.session.commit()
            flash(f"Student '{student.name}' added successfully.", 'success')
            return redirect(url_for('routes.view_students'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding student. Please try again.', 'danger')
            
    return render_template('add_student.html', form=form)


@routes_bp.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('routes.view_students'))
        
    form = StudentForm(obj=student, student_id=student.id)
    if form.validate_on_submit():
        student.name = form.name.data.strip()
        student.email = form.email.data.strip().lower()
        student.phone = form.phone.data.strip()
        student.department = form.department.data
        student.semester = form.semester.data
        student.address = form.address.data.strip() if form.address.data else ''
        
        try:
            db.session.commit()
            flash(f"Student '{student.name}' updated successfully.", 'success')
            return redirect(url_for('routes.view_students'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating student. Please try again.', 'danger')
            
    return render_template('edit_student.html', form=form, student=student)


@routes_bp.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('routes.view_students'))
        
    name = student.name
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f"Student '{name}' deleted successfully.", 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting student. Please try again.', 'danger')
        
    return redirect(url_for('routes.view_students'))


@routes_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
