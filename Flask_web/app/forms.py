# -*- coding: utf-8 -*-
import sys
import os

from wtforms.validators import ValidationError, Email, EqualTo
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

sys.path.append("..")
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


'''
处理WEB表单数据
登录表单
'''
class LoginForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(message='请输入名户名')])
	password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
	remember_me = BooleanField('记住此信息')
	submit = SubmitField('登录')


'''
处理WEB表单数据
注册表单
'''
class RegistrationForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired()])
	email = StringField('邮箱', validators=[DataRequired(), Email()])
	telephone = StringField('手机号', validators=[DataRequired()])
	password = PasswordField('密码')
	password2 = PasswordField('确认密码', validators=[EqualTo('password')])
	submit = SubmitField('注册')
	#验证用户名是否被使用
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('此用户名已经被使用！')
	#验证邮箱是否被使用
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('此邮箱已经被使用！')
	#验证手机号是否被使用
	def validate_telephone(self, telephone):
		user = User.query.filter_by(telephone=telephone.data).first()
		if user is not None:
			raise ValidationError('此手机号已经被使用！')


'''
处理WEB表单数据
个人信息表单
'''
class EditProfileForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
	company = TextAreaField('公司名称', validators=[Length(min=0, max=40)])
	submit = SubmitField('提交')


'''
处理WEB表单数据
入侵相机选择表单
'''
class IntrusionForm(FlaskForm):
	cameraid = StringField('摄像机ID', validators=[DataRequired(message='请输入摄像机ID')])
	submit = SubmitField('确定')


'''
处理WEB表单数据
检测相机选择表单
'''
class DetectForm(FlaskForm):
	cameraid = StringField('摄像机ID', validators=[DataRequired(message='请输入摄像机ID')])
	submit = SubmitField('确定')


