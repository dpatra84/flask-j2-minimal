from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from app.forms.auth import LoginForm, RegistrationForm
from app.models import db
from app.models.auth import User
from datetime import datetime,timezone


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for("members_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("members_page"))
        flash("Invalid email or password")
    return render_template("user/login.j2", form=form)


@app.route("/logout")
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('members_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        user.created_at = datetime.now(tz=timezone.utc)
        user.updated_at = datetime.now(tz=timezone.utc)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('user/register.j2', form=form)