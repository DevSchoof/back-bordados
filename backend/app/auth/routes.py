from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Credenciais inválidas')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))