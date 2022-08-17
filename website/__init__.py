#initiation file for website, ran on import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

app = Flask(__name__)
DB_NAME= "user_database.db"
app.config['SECRET_KEY'] = 'Your mother is hawt'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)
db.init_app(app)
 
from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

from .models import User, ACdatum, FanData

if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('Created Database!')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

