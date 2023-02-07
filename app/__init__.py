from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager,login_user, UserMixin, login_required, logout_user, current_user


app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models

from app.models import Doctor

@login_manager.user_loader
def load_user(doctor_id):
    return Doctor.query.get(int(doctor_id))

if __name__=='__main__':
        app.run(debug=True)





