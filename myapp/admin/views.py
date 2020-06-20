#external
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

#internal
from . import admin
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from .. import db
from ..models import Department, Role, Employee

def check_admin():
    '''Prevent non-admins from accessing the page'''
    if not current_user.is_admin:
        abort(403)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    ''' List all departments'''
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html',
                            departments=departments, title='Departments')



@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    '''Add a department to the database'''
    check_admin()
    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            #add department to the db
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists!')
        return redirect(url_for('admin.list_departments'))
    #load department template
    return render_template('admin/departments/department_form.html', action='Add',
                            add_department=add_department, form=form,
                            title='Add Department')


@admin.route('/departments/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_department(id):
    '''Edit a department'''
    check_admin()

    add_department = False
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have edited the department successfully!')

        #redirect
        return redirect(url_for('admin.list_departments'))

    # fill data to the fields
    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department_form.html', action='Edit',
                            add_department=add_department, form=form,
                            department=department, title='Edit Department')


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    '''Delete a department from the db'''
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have deleted the department successfully.')
    return redirect(url_for('admin.list_departments'))


@admin.route('/roles')
@login_required
def list_roles():
    '''List all roles'''
    check_admin()
    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    '''Add a role to the DB'''
    check_admin()

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            #add role to the DB
            db.session.add(role)
            db.session.commit()
            flash('You have added a new role successfully.')
        except:
            flash('Error: role name already exists.')

        #redirect to the roles page
        return redirect(url_for('admin.list_roles'))
    #load role template
    return render_template('admin/roles/role_form.html', add_role=add_role,
                            form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_role(id):
    '''Edit a role'''
    check_admin()

    add_role = False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        #db.session.add(role)
        db.session.commit()
        flash('You have edited the role successfully!')

        #redirect
        return redirect(url_for('admin.list_roles'))

    # fill data to the fields
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role_form.html', action='Edit',
                            add_role=add_role, form=form, title='Edit Role')


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    '''Delete a role from the db'''
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have deleted the role successfully.')
    return redirect(url_for('admin.list_roles'))


@admin.route('/employees')
@login_required
def list_employees():
    '''List all employees'''
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                            employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    '''Assign a department and role to an employee'''
    check_admin()
    employee = Employee.query.get_or_404(id)
    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        return redirect(url_for('admin.list_employees'))
    return render_template('admin/employees/employee_form.html',
                            employee=employee, form=form,
                            title='Assign Employee')
