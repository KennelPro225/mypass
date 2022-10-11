from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from mypass.models import Users


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
