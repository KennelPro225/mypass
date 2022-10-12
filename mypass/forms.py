from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TimeField, DateField, FileField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from mypass.models import Users, Category, Type_Event


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(
        message='Addresse email est invalide')])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Me garder Connecter')
    submit = SubmitField('Se connecter')
    


class RegistrationForm(FlaskForm):
    firstName = StringField('Prénom(s)', validators=[DataRequired()])
    lastName = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(
        message='Addresse email est invalide')])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    cpassword = PasswordField('Confirmez Mot de passe', validators=[
        DataRequired(), EqualTo('password', message="Le mot de passe saisi n'est pas compatible.")])
    submit = SubmitField("S'inscrire")

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Cet Email a déjà un compte. Choisissez en un autre.')


category = Category.query.all()
choice = []
for cate in category:
    choice.append("{}".format(cate.category))

type = Type_Event.query.all()
choices = []
for typeE in type:
    choices.append("{}".format(typeE.name))


class PostForm(FlaskForm):
    title = StringField("Titre de l'évènement")
    type = SelectField("Type d'évènement", choices=choices)
    # description = TextAreaField("Desription de l'évènement")
    category = SelectField("Catégories", choices=choice)
    seat = IntegerField('Nombre de Places')
    image = FileField('Image Illustrative')
    place = StringField('Lieu')
    date = DateField('Date')
    hour = TimeField('Heure')


class EditForm(FlaskForm):
    title = StringField("Titre de l'évènement", validators=[DataRequired()])
    seat = IntegerField('Nombre de Places', validators=[DataRequired()])
    image = FileField('Image Illustrative')
    date = DateField('Date', validators=[DataRequired()])
    hour = TimeField('Heure', validators=[DataRequired()])
    submit = SubmitField("Add")
