from flask import render_template, redirect, request, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .. import db
from .forms import LoginForm, RegForm, LogoutForm
from ..models import User
from sqlalchemy.exc import IntegrityError


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # if not work, try request.method == 'POST'
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.upass.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.user', username=current_user.username)
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/user/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if request.method == 'POST':
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('main.index'))
    
    return render_template('auth/logout.html', form=form) # move to auth folder


@auth.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        user = User(
            uid=form.uid.data,
            email=form.email.data.lower(),
            username=form.username.data,
            password=form.password.data
            )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: username or email already exists.')
            return redirect(url_for('auth.register')) # These two parts, need to move from main to auth folder
    return render_template('auth/register.html', form=form)
