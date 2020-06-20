#external
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

#internal
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    '''Handle request to the /register route
       Add an employee to the database through the RegistrationForm'''
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
        #add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You can log-in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Handle request to the /login route
       Log an employee in through the login form'''
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            login_user(employee)
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    '''Handle requests to the /logout route
    Log an enployee out through the logout link'''
    logout_user()
    flash('You have successfully been logged out!')
    return redirect(url_for('auth.login'))
