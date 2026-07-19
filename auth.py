import functools
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, g
from models import db, User
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            # Redirect to login page and remember original destination
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # Load user from db. Handled safely.
        g.user = db.session.get(User, user_id)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to dashboard
    if g.user:
        return redirect(url_for('routes.dashboard'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if g.user:
        return redirect(url_for('routes.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            
            # Check next parameter for redirection
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('routes.dashboard')
            return redirect(next_page)
            
        flash('Invalid email or password.', 'danger')
        
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/social-login/<provider>')
def social_login(provider):
    if provider not in ['google', 'github']:
        flash('Invalid provider.', 'danger')
        return redirect(url_for('auth.login'))
        
    email = f"{provider}_user@example.com"
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.set_password('mock-social-password-12345')
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Error signing in with social provider. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
            
    session.clear()
    session['user_id'] = user.id
    flash(f'Successfully logged in with {provider.capitalize()}.', 'success')
    return redirect(url_for('routes.dashboard'))
