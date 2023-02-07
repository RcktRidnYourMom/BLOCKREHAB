from flask import Flask, render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Doctor, Patient, Messages
from app.forms import LoginForm, FormIns, RegisterForm
from wtforms.validators import DataRequired, ValidationError, Email, email_validator
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, UserMixin, LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
import smtplib
import os



# route principale, reindirizzamento al login
@app.route('/')
def index():
    return render_template('login.html')

# route della dashboard ( pagina principale), accedibile solo se effettuato login altrimenti reindirizzamento a login
@app.route('/index1')
@login_required
def index1():
    return render_template('index.html')

    
# route della pagina di login, gli viene passato il form di login e vengono validati i campi. allarmi personalizzati per ogni errore
# reindirizzamento alla pagina dashboard se il login ha successo, altrimenti si ricarica il login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    title="BLOCKREHAB"
    form = LoginForm()
    if request.method == "POST":
        if form.validate_username: 
            doctor = Doctor.query.filter_by(username=form.username.data).first()
            if doctor:
                if check_password_hash(doctor.password, form.password.data):
                    if (doctor.firmadig == form.firmadig.data):
                        login_user(doctor)
                        flash(f'Login successfull!')
                        return redirect(url_for('index1'))
                    else:
                        flash(f'Wrong digital signature!! Try again')
                        return render_template('login.html',  form=form) 

                else:
                    flash(f'Wrong password!! Try again')
                    return render_template('login.html',  form= form)
            else:
                flash(f'Doctor not registred with this username! Try again')
                return render_template('login.html', form=form)
    else:
        flash(f'Warning all fields are required')
        return render_template('login.html', title=title, form=form)
    


# metodo di logout, semplicemente una route per una pagina che esegue la funzione di logout
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("Successfully logged out!")
    return redirect(url_for('login'))



# route per la registrazione del dottore, non accedibile dalla piattaforma. Solamente il team di sviluppo ha i privilegi necessari
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    title = 'BLOCKREHAB'
    if request.method == "POST":
        name_ = request.form['name']
        username_ = request.form['username']
        password_ = generate_password_hash(request.form['password'])
        firmadig_ = request.form['firmadig']
        
        new_doctor = Doctor(name=name_, username=username_, password=password_, firmadig=firmadig_)
        if not name_ or not username_ or not password_ or not firmadig_:
            error_statement = "All Form Fields Required...."
            return render_template("login.html",  title=title, name=name_, username=username_, password=password_, firmadig=firmadig_, error_statement=error_statement)
        else:

            try:
                db.session.add(new_doctor)
                db.session.commit()
                return redirect('/login')
            except:
                return "There was an error adding the patient"

    else:
        patients = Patient.query.order_by(Patient.date)
        return render_template('signup.html',  title=title, patients=patients)






# route al form di inserimento del paziente, in questo caso specifico per la riabilitazione da infortunio
@app.route('/infortuni', methods=['POST', 'GET'])
@login_required
def infortuni():
    title = 'BLOCKREHAB'
    if request.method == "POST":
        firstname_ = request.form['firstname']
        lastname_ = request.form['lastname']
        address_ = request.form['address']
        email_ = request.form['email']

        new_patient = Patient(firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        if not firstname_ or not lastname_ or not address_ or not email_:
            error_statement = "All Form Fields Required...."
            return render_template("infortuni.html", error_statement=error_statement, title=title, firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        else:

            try:
                db.session.add(new_patient)
                db.session.commit()
                return redirect('/index1')
            except:
                return "There was an error adding the patient"

    else:
        patients = Patient.query.order_by(Patient.date)
        return render_template('infortuni.html',  title=title, patients=patients)


# route al form di inserimento del paziente, in questo caso specifico per la riabilitazione da ictus        
@app.route('/ictus', methods=['POST', 'GET'])
@login_required
def ictus():
    title = 'BLOCKREHAB'
    if request.method == "POST":
        firstname_ = request.form['firstname']
        lastname_ = request.form['lastname']
        address_ = request.form['address']
        email_ = request.form['email']
        new_patient = Patient(firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        if not firstname_ or not lastname_ or not address_ or not email_:
            error_statement = "All Form Fields Required...."
            return render_template("ictus.html", error_statement=error_statement, title=title, firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        else:

            try:
                db.session.add(new_patient)
                db.session.commit()
                return redirect('/index1')
            except:
                return "There was an error adding the patient"

    else:
        patients = Patient.query.order_by(Patient.date)
        return render_template('ictus.html',  title=title, patients=patients)



# route al form di inserimento del paziente, in questo caso specifico per la riabilitazione da sla       
@app.route('/sclerosimultipla', methods=['POST', 'GET'])
@login_required
def sclerosimultipla():
    title = 'BLOCKREHAB'
    if request.method == "POST":
        firstname_ = request.form['firstname']
        lastname_ = request.form['lastname']
        address_ = request.form['address']
        email_ = request.form['email']
        new_patient = Patient(firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        if not firstname_ or not lastname_ or not address_ or not email_:
            error_statement = "All Form Fields Required...."
            return render_template("sclerosimultipla.html", error_statement=error_statement, title=title, firstname=firstname_, lastname=lastname_, address=address_, email=email_)
        else:

            try:
                db.session.add(new_patient)
                db.session.commit()
                return redirect('/index1')
            except:
                return "There was an error adding the patient"

    else:
        patients = Patient.query.order_by(Patient.date)
        return render_template('sclerosimultipla.html',  title=title, patients=patients)
        




# route di testing con la visualizzazione dei pazienti. Non sarebbe presente nella piattaforma
@app.route('/pazienti', methods=['GET'])
def pazienti():
    patients = Patient.query.order_by(Patient.date)
    doctors = Doctor.query.order_by(Doctor.id)

    return render_template('pazienti.html', patients=patients, doctors =doctors)


# route per il form di assistenza, verrà inviato al database ma non verra visualizzato in nessuna pagina
@app.route('/assistenza', methods=['GET', 'POST'])
@login_required
def assistenza():
    title = 'BLOCKREHAB'
    if request.method == "POST":
        username_ = request.form['username']
        email_ = request.form['email']
        message_ = request.form['message']
        new_message = Messages(username=username_, email=email_, message=message_)
        if not username_ or not email_ or not message_ :
            error_statement = "All Form Fields Required...."
            return render_template("assistenza.html", error_statement=error_statement, title=title, username=username_, email=email_, message=message_)
        else:

            try:
                print(new_message)
                db.session.add(new_message)
                db.session.commit()
                return redirect('/index1')
            except:
                return "There was an error sending the message"

    else:
       
        return render_template('assistenza.html',  title=title)


'''firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    address = request.form.get("address")
    email = request.form.get("email")

    message = "You have  successfully inserted the patient into the allowlist"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("miromiri007@gmail.com", "PASSWORD")
    server.sendmail("miromiri007@gmail.com", email, message)


    if not firstname or not lastname or not address or not email:
        error_statement = "All Form Fields Required...."
        return render_template("infortuni.html", error_statement=error_statement, title=title, firstname=firstname, lastname=lastname, address=address, email=email)
   '''
        
    
    











