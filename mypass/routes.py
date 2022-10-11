from mypass import app, db, bcrypt
from mypass.models import Users
from flask import render_template, url_for, flash, redirect, request
from mypass.forms import LoginForm, RegistrationForm
from random import choice
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(
                "Erreur lors de la connexion, verifez si le mot de passe et l'email sont correctes ", 'danger')
    return render_template('login.html', title='Connexion', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashpassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        name1 = form.lastName.data
        name = form.firstName.data
        number = range(100000, 1000000000, 345)
        code = choice(number)

        userId = '{}{}{}'.format((str(name1)[0].capitalize()), (str(
            name)[0].capitalize()), (str(name)[1].lower())+str(code))

        user = Users(last_name=form.lastName.data, first_name=form.lastName.data,
                     email=form.email.data, password=hashpassword, user_id=userId)

        db.session.add(user)
        db.session.commit()

        flash(f"Votre inscription a bien été pris en compte s'il vous plaît", 'success')
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Inscription', form=form)


@app.route('/event')
@login_required
def Event():
    return render_template('event.html')


@app.route('/create_event')
@login_required
def createEvent():
    return render_template('createEvent.html')


@app.route('/edit_event')
@login_required
def editEvent():
    return render_template('editEvent.html')


@app.route('/delete_event')
@login_required
def deleteEvent():
    return render_template('deleteEvent.html')


@app.route('/user/profile')
def profile():
    pass
