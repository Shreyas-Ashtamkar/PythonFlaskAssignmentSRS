from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from ..utils.authutils import register_user, check_login, delete_user, edit_user
from ..forms import Users

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    register_form = Users.RegisterForm()
    response = render_template('auth/register.html', form=register_form)
    
    if request.method == 'POST' and register_form.validate_on_submit():
        try:
            fullname = register_form.fullname.data
            username = register_form.username.data
            password1 = register_form.password1.data
            password2 = register_form.password2.data
            
            if password1 == password2:
                register_user(fullname, username, password2)
                
            response = redirect(url_for('auth.login'))
        except Exception as e:
            flash(e)
            response = render_template('auth/register.html', form=register_form)

    return response


@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    edit_form = Users.EditForm(obj=current_user)
    
    response = render_template('auth/edit.html', form=edit_form)
    
    if request.method == 'POST' and edit_form.validate_on_submit():
        try:
            fullname = edit_form.fullname.data
            password = edit_form.password.data
            
            if check_login(current_user.username, password):
                edit_user(current_user.id, fullname)
                
            response = redirect(url_for('auth.view_profile'))
        except Exception as e:
            flash(e)
            response = render_template('auth/edit.html', form=edit_form)
  
    return response


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user:
        if current_user.is_authenticated:
            return redirect(url_for('home.home_page'))
        
    login_form = Users.LoginForm()
    
    if request.method == 'POST' and login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        try:
            user = check_login(username, password)
            if user:
                login_user(user)
                return redirect(url_for('home.home_page'))
            else:
                raise Exception("Incorrect Password")
        except Exception as e:
            flash(e.__str__())
            print(e)
            return render_template('auth/login.html', form=login_form)
    return render_template('auth/login.html', form=login_form)



@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'POST':
        user = current_user
        password = request.form.get('password')
        if check_login(user.username, password):
            delete_user(user.id)
            flash("User deleted successfully.")
            return redirect(url_for('home.home_page'))
    return render_template('auth/delete.html')



@bp.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@bp.route('/profile', methods=('GET',))
@login_required
def view_profile():
    return render_template('auth/profile.html', user=current_user)
