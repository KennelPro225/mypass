from mypass import app, db, bcrypt
import secrets
import os
import pdfkit
from datetime import datetime
from mypass.models import Category, Type_Event, Users, Events, Tickets
from flask import Response, abort, make_response, render_template, url_for, flash, redirect, request
from mypass.forms import EditForm, LoginForm, RegistrationForm, PostForm, EventViewt, Ticket
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
        user = Users(last_name=form.lastName.data, first_name=form.firstName.data,
                     email=form.email.data, password=hashpassword, user_id=userId)
        db.session.add(user)
        db.session.commit()
        flash(f"Votre inscription a bien été pris en compte s'il vous plaît", 'success')
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Inscription', form=form)


def author(user_id):
    user = Users.query.filter_by(id=user_id).first()
    return user.first_name + ' ' + user.last_name


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/thumbnails/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@ app.route('/create_event', methods=['GET', 'POST'])
@ login_required
def createEvent():
    form = PostForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(
            category=form.category.data).first()
        type = Type_Event.query.filter_by(name=form.type.data).first()
        post = Events(title=form.title.data, category=category.id, author=current_user.id, type=type.id, place=form.place.data,
                      date_event=form.date.data, time_event=form.hour.data, seat=form.seat.data)
        if form.image.data:
            image_file = save_picture(form.image.data)
            post = Events(title=form.title.data, category=category.id, author=current_user.id, type=type.id, place=form.place.data,
                          date_event=form.date.data, time_event=form.hour.data, seat=form.seat.data, image=image_file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('Event'))
    return render_template('createEvent.html', form=form, title='Créer un Evènement')


@app.route('/event', methods=['GET', 'POST'])
@login_required
def Event():
    button = EventViewt()
    data = []
    events = Events.query.all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('event.html', datas=data, button=button, title="Plus d'évènements")


@app.route('/event/<event_id>', methods=['GET', 'POST'])
def EventView(event_id):
    data = []
    button = Ticket()
    event = Events.query.get(event_id)
    # event = Events.query.filter_by(id=event_id).all()
    author = Users.query.get(event.author)
    data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), 'author_id': event.author, 'author': author.first_name + ' ' + author.last_name, "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                 "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('eventview.html', datas=data, button=button, title='Prendre sont ticket')


@ app.route('/event/ticket/<event_id>/<user_id>', methods=['GET'])
@ login_required
def ticket(event_id, user_id):
    data = []
    event = Events.query.get(event_id)
    current_user.id = user_id
    data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), 'user_id': current_user.id, 'user': current_user.first_name + ' ' + current_user.last_name, "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                 "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    rendered = render_template('ticket.html', datas=data)
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    css = ['mypass/{}'.format(url_for('static', filename='ticket.css'))]
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdf = pdfkit.from_string(rendered, configuration=config, css=css)
    response = make_response(pdf)
    response.headers['Context-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=evenTicket.pdf'
    return response


@ app.route('/event/e/<event_id>/update', methods=['GET', 'POST'])
@ login_required
def editEvent(event_id):
    form = EditForm()
    event = Events.query.get(event_id)

    if event.author != current_user.id:
        abort(403)
    else:
        if form.is_submitted():
            if form.image.data:
                picture_file = save_picture(form.image.data)
                event.image = picture_file
            event.title = form.title.data
            event.seat = form.seat.data
            event.date_event = form.date.data
            event.time_event = form.hour.data
            event.place = form.place.data
            db.session.commit()
            flash('Les modifications ont été pris en compte Merci!')
            return render_template('event.html')
        elif request.method == 'GET':
            form.title.data = event.title
            form.seat.data = event.seat
            form.image.data = event.image
            form.date.data = event.date_event
            form.hour.data = event.time_event
            form.place.data = event.place
    return render_template('editeEvent.html', form=form, title='Editer cet évènement', event=event)


@ app.route('/delete_event', methods=['GET', 'POST'])
@ login_required
def deleteEvent():
    return render_template('deleteEvent.html', title='Supprimer cet évènement')


@ app.route('/profile/', methods=['GET'])
@ login_required
def profile():
    data = []
    image_file = url_for(
        'static', filename='/thumbnails/profile_pics/' + current_user.image_profile)
    events = Events.query.filter_by(author=current_user.id).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))})

    return render_template('profile.html', title='Profile', image=image_file, datas=data)


@ app.route('/profile/user/<user_id>', methods=['GET', 'POST'])
@ login_required
def profileuser(user_id):
    events = Users.query.get(int(user_id))
    return render_template('profile.html', title='Profile')


@ app.route('/category/', methods=['GET', 'POST'])
@ login_required
def category():
    return render_template('category.html', title='Catégories')
