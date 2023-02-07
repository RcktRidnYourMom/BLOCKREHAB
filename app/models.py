from datetime import datetime
from app import db
from flask_login import UserMixin


#modello del paziente, verrà utilizzato per la creazione della tabella pazienti nel database
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(128))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Patient %r>' % self.id



#modello del dottore, verrà utilizzato per la creazione della tabella dottori nel database
class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(140), nullable=False)
    firmadig = db.Column(db.String(140), nullable=False)
    
    def __repr__(self):
        return '<Doctor {}>'.format(self.id)

#modello del messaggio di assistenza che verrà inviato al db. Niente visualizzazione grafica. Non necessaria        

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    message = db.Column(db.String(2000), nullable=False)
   
    
    def __repr__(self):
        return '<Message {}>'.format(self.id)