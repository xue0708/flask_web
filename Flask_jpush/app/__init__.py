import sys
import os

from flask_login import LoginManager
from config import Config
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append('.')
sys.path.append("..")


'''
一些配置
指定模板位置、绑定app、绑定数据库等
'''
app = Flask(__name__, template_folder='../templates', static_folder="", static_url_path="")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
