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


'''
回调函数
如果user参数无值，通过调用回调函数来得到user
'''
@login.user_loader
def load_user(id):
	return User.query.get(int(id))


'''
数据库模型
用户信息表，包括：ID、用户名、邮箱、手机号码、密码、所属公司、上次登陆时间
'''
class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	telephone = db.Column(db.String(20), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	company = db.Column(db.String(40))
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


'''
数据库模型
入侵信息表，包括：ID、摄像机ID、图片路径、视频路径、入侵时间
'''
class Camera_Information(db.Model):
	__tablename__ = 'camera_information'
	id = db.Column(db.Integer, primary_key=True)
	cameraid = db.Column(db.String(10))
	imagepath = db.Column(db.String(120))
	videopath = db.Column(db.String(120))
	last_time = db.Column(db.DateTime, default=datetime.utcnow)


'''
数据库模型
检测信息表，包括：ID、摄像机ID、图片路径、视频路径、检测时间
'''
class Yolo_abnormaldetect(db.Model):
	__tablename__ = 'yolo_abnormaldetect'
	id = db.Column(db.Integer, primary_key=True)
	cameraid = db.Column(db.String(10))
	imagepath = db.Column(db.String(120))
	videopath = db.Column(db.String(120))
	last_time = db.Column(db.DateTime, default=datetime.utcnow)


