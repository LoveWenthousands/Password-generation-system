from flask import render_template, redirect, url_for, flash, request
from flask.blueprints import Blueprint
from app import db
from app.models import User
from flask_login import current_user, login_user, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User(username=request.form['username'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已成功注册！')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='注册')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash('无效的用户名或密码')
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))