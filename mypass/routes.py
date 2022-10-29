import os
from unittest import result
import pdfkit
import secrets
from PIL import Image
from random import choice
from datetime import datetime
from mypass import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mypass.models import Category, Type_Event, Users, Events, Tickets, Admins
from flask import Response, abort, make_response, render_template, url_for, flash, redirect, request, session
from mypass.forms import EditForm, LoginForm, RegistrationForm, PostForm, EventViewt, Ticket, UpdateAccountForm, AdminForm, AdminLoginForm, Checker


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Bienvenue Sur EvenTicket!", 'success')
            return redirect(url_for('home'))
        else:
            flash(
                "Erreur lors de la connexion, verifez si le mot de passe et l'email sont correctes ", 'danger')
    return render_template('auth/login.html', title='Connexion', form=form)


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
        flash(f"Votre inscription a bien été pris en compte. Vous pouvez maintenant vous connecter!", 'success')
        return redirect(url_for('login'))
    return render_template('auth/signUp.html', title='Inscription', form=form)


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
    output_size = (543, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/thumbnails/profile_pics', picture_fn)
    form_picture.save(picture_path)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/create_event', methods=['GET', 'POST'])
@login_required
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
    return render_template('post/createEvent.html', form=form, title='Créer un Evènement')


@app.route('/event', methods=['GET', 'POST'])
@login_required
def Event():
    button = EventViewt()
    data = []
    events = Events.query.order_by(Events.date_event.asc()).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),

    print(data)
    return render_template('post/event.html', datas=data, button=button, title="Plus d'évènements")


@app.route('/event/<event_id>', methods=['GET', 'POST'])
def EventView(event_id):
    data = []
    button = Ticket()
    event = Events.query.order_by(Events.date_event.asc()).get(event_id)
    # event = Events.query.filter_by(id=event_id).all()
    author = Users.query.get(event.author)
    data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %d %B %Y'), 'author_id': event.author, 'author': author.first_name + ' ' + author.last_name, "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                 "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('post/eventview.html', datas=data, button=button, title='Prendre sont ticket')


@app.route('/event/ticket/<event_id>/<user_id>', methods=['POST', 'GET'])
@login_required
def ticket(event_id, user_id):
    number = range(2999999929, 10000000000, 1)
    code = choice(number)
    data = []
    event = Events.query.order_by(Events.date_event.asc()).get(event_id)
    current_user.id = user_id
    a = 1
    b = current_user.id
    c = event.id
    d = code
    tass = Tickets(user=b, event=c, nombre_ticket=a, numero_ticket=d)
    db.session.add(tass)
    db.session.commit()
    data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %d %B %Y'), 'user_id': current_user.id, 'user': current_user.first_name + ' ' + current_user.last_name, "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                 "image": "file:///mypass/{}".format(url_for('static', filename='thumbnails/images/{}'.format(event.image))), 'numero_ticket': code}),
    rendered = render_template('post/ticket.html', datas=data)
    # path_to_file = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration()
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers['Context-Type'] = 'Application/PDF'
    response.headers['Content-Disposition'] = 'attachment;filename={}.pdf'.format(
        code)
    return response


@app.route('/event/e/<event_id>/update', methods=['GET', 'POST'])
@login_required
def editEvent(event_id):
    form = EditForm()
    event = Events.query.order_by(Events.date_event.asc()).get(event_id)

    if event.author != current_user.id:
        abort(403)
    else:
        if form.is_submitted():
            button = EventViewt()
            if form.image.data:
                picture_file = save_picture(form.image.data)
                event.image = picture_file
            event.title = form.title.data
            event.seat = form.seat.data
            event.date_event = form.date.data
            event.time_event = form.hour.data
            event.place = form.place.data
            db.session.commit()
            flash('Les modifications ont été pris en compte Merci!', 'success')
            data = []
            events = Events.query.order_by(Events.date_event.asc()).all()
            for event in events:
                data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                        "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
            return render_template('post/event.html', datas=data, button=button, title="Plus d'évènements")
        elif request.method == 'GET':
            form.title.data = event.title
            form.seat.data = event.seat
            form.image.data = event.image
            form.date.data = event.date_event
            form.hour.data = event.time_event
            form.place.data = event.place
    return render_template('post/editeEvent.html', form=form, title='Editer cet évènement', event=event)


@app.route('/delete_event/<event_id>', methods=['GET', 'POST'])
@login_required
def deleteEvent(event_id):
    event = Events.query.order_by(Events.date_event.asc()).get(event_id)
    ticket = Tickets.query.filter_by(event=event_id)
    db.session.delete(ticket)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('profile', event_id=event.id))


@app.route('/profile/', methods=['GET'])
@login_required
def profile():
    data = []
    image_file = url_for(
        'static', filename='/thumbnails/profile_pics/' + current_user.image_profile)
    events = Events.query.order_by(Events.date_event.asc()).filter_by(
        author=current_user.id).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))})
    return render_template('account/profile.html', title='Profile {} {}'.format(current_user.first_name, current_user.last_name), image=image_file, datas=data)


@app.route('/updateAccount', methods=['GET', 'POST'])
@login_required
def updateAccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_profile = picture_file
        current_user.first_name = form.firstName.data
        current_user.last_name = form.lastName.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.firstName.data = current_user.first_name
        form.lastName.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account/updateAccount.html', form=form)


@app.route('/profile/user/<user_id>', methods=['GET', 'POST'])
@login_required
def profileuser(user_id):
    data = []
    user = Users.query.get(int(user_id))
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(author=user.id).all()
    if user.id == current_user.id:
        return redirect(url_for('profile'))
    else:
        for event in events:
            data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%a, %b. %y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place, "image": url_for(
                "static", filename="thumbnails/images/{}".format(event.image)), "username": user.first_name + " " + user.last_name, "profile_image":  url_for("static", filename="/thumbnails/profile_pics/" + user.image_profile)})
        return render_template('account/userProfile.html', title='Profile', datas=data)


@app.route('/app/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admins.query.filter_by(mail=form.email.data)
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            flash(f"Bienvenue Sur EvenTicket!", 'success')
            session['adminView']
            return redirect(url_for('home'))
        else:
            flash(
                "Erreur lors de la connexions, verifez si le mot de passe et l'email sont correctes ", 'danger')
    return render_template('administration/adminLogin.html', form=form)


@app.route('/app/adminSignup', methods=['GET', 'POST'])
def adminSignUp():
    form = AdminForm()
    if form.validate_on_submit():
        hashpassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # db.session.add(user)
        # db.session.commit()
        flash(f"Votre inscription a bien été pris en compte. Vous pouvez maintenant vous connecter!", 'success')
        return redirect(url_for('login'))
    return render_template('administration/adminLogin.html', form=form)


@app.route('/app/adminView', methods=['GET', 'POST'])
def adminView():
    pass


@app.route('/category/affaire/', methods=['GET', 'POST'])
@login_required
def affaire():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=9).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/affaire.html', title='Catégories', datas=data, button=button)


@app.route('/category/art_du_spetacle/', methods=['GET', 'POST'])
@login_required
def art_du_spectacle():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=8).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/art_du_spetacle.html', title='Catégories', datas=data, button=button)


@app.route('/category/education/', methods=['GET', 'POST'])
@login_required
def education():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=5).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/education.html', title='Catégories', datas=data, button=button)


@app.route('/category/environnement/', methods=['GET', 'POST'])
@login_required
def environnement():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=3).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/environnement.html', title='Catégories', datas=data, button=button)


@app.route('/category/formation/', methods=['GET', 'POST'])
@login_required
def formation():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=6).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/formation.html', title='Catégories', datas=data, button=button)


@app.route('/category/gastronomie/', methods=['GET', 'POST'])
@login_required
def gastronomie():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=1).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/gastronomie.html', title='Catégories', datas=data, button=button)


@app.route('/category/loisirs/', methods=['GET', 'POST'])
@login_required
def loisirs():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=10).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/loisirs.html', title='Catégories', datas=data, button=button)


@app.route('/category/musique/', methods=['GET', 'POST'])
@login_required
def musique():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=4).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/musique.html', title='Catégories', datas=data, button=button)


@app.route('/category/sport/', methods=['GET', 'POST'])
@login_required
def sport():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=2).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/sport.html', title='Catégories', datas=data, button=button)


@app.route('/category/voyages/', methods=['GET', 'POST'])
@login_required
def voyages():
    button = EventViewt()
    data = []
    events = Events.query.order_by(
        Events.date_event.asc()).filter_by(category=7).all()
    for event in events:
        data.append({'id': event.id, "title": event.title, "date": event.date_event.strftime('%A, %d %B %Y'), "heure": event.time_event.strftime('%H:%M'), "lieu": event.place,
                    "image": url_for('static', filename='thumbnails/images/{}'.format(event.image))}),
    return render_template('category/voyages.html', title='Catégories', datas=data, button=button)


@app.route('/checkTickets/<event_id>', methods=['GET', 'POST'])
@login_required
def checker(event_id):
    form = Checker()
    data = []
    if form.is_submitted():
        tickets = Tickets.query.filter_by(
            numero_ticket=int(form.numero.data),event=event_id).all()
        for ticket in tickets:
            data.append({'numero_ticket': ticket.numero_ticket,'event':ticket.event})
            print(data)
        return render_template('/post/result.html', tickets=data)
    return render_template('/post/ticketChecker.html', form=form)
