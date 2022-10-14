from mypass import app, db, bcrypt
import secrets
import os
from mypass.models import Category, Type_Event, Users, Events
from flask import render_template, url_for, flash, redirect, request
from mypass.forms import EditForm, LoginForm, RegistrationForm, PostForm
from random import choice
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
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


def author(user_id):
    user = Users.query.filter_by(id=user_id).first()
    return user.first_name + ' ' + user.last_name


@app.route('/event', methods=['GET', 'POST'])
@login_required
def Event():
    events = Events.query.all()
    print(events)
    # auteur= sql-select
    # for event in events:
    # filename = url_for('static', filename='./thumbnails/images/'+ events[0].place)
    return render_template('event.html', events=events)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/thumbnails/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = PostForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(
            category=form.category.data).first()
        type = Type_Event.query.filter_by(name=form.type.data).first()
        if form.image.data:
            image_file = save_picture(form.image.data)
            post = Events(title=form.title.data, category=category.id, author=current_user.id, type=type.id, place=form.place.data,
                          date_event=form.date.data, time_event=form.hour.data, seat=form.seat.data, image=image_file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Event'))
    return render_template('createEvent.html', form=form, title='Evènements')


@app.route('/edit_event', methods=['GET', 'POST'])
@login_required
def editEvent():
    form = EditForm()
    return render_template('editeEvent.html', form=form, title='Editer cet évènement')


@app.route('/delete_event', methods=['GET', 'POST'])
@login_required
def deleteEvent():
    return render_template('deleteEvent.html', title='Supprimer cet évènement')


@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/category/', methods=['GET', 'POST'])
@login_required
def category():
    return render_template('category.html', title='Catégories')


@app.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    return render_template('ticket.html')
