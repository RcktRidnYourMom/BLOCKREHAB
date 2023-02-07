from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, InputRequired
from app.models import Doctor, Patient
from app import db



# form per il login del dottore che passeremo alle routes

class LoginForm(FlaskForm):
    username= StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firmadig = StringField('Firma Digitale', validators=[InputRequired()])
    submit = SubmitField('Login')

#funzione per validare lo username

    def validate_username(self, username ):
        doctor = Doctor.query.filter_by(username=username.data).first()
        if not doctor:
            raise ValidationError("Dottore non presente nel database!")
        return

   


#form di registrazione del dottore, non visibile. Solo per team di sviluppo
    
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    firmadig = StringField('Firma Digitale', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

#form per l'inserimento del paziente nella allowlist

class FormIns(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()] )
    address = StringField('Address', validators=[DataRequired()] )
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign In')
