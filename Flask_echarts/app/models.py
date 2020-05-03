# -*- coding: utf-8 -*-
import sys
import os

from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from hashlib import md5

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	#明文密码进行加密
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
	#验证密码
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	#当前用户信息打印
	def __repr__(self):
		return '<用户名:{}>'.format(self.username)


class Table1(db.Model):
    __tablename__ = 'data1'
    id = db.Column(db.Integer, primary_key=True)
    timetag = db.Column(db.DateTime)
    dx = db.Column(db.Integer)
    dy = db.Column(db.Integer)
    dz = db.Column(db.Integer)
    gx = db.Column(db.Integer)
    gy = db.Column(db.Integer)
    gz = db.Column(db.Integer)



