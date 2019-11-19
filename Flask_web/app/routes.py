# -*- coding: utf-8 -*-
import sys
import os
import importlib
import json
import base64
import random
import cv2 as cv
importlib.reload(sys)

from werkzeug.urls import url_parse
from app.models import *
from app.forms import LoginForm, RegistrationForm, EditProfileForm, IntrusionForm, DetectForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from sqlalchemy import *
from flask_redis import FlaskRedis
from app import app

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


'''
首页
未登录前/退出登录时，进入此页面
'''
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Sylincom')


'''
用户登录
进入登录页面，输入用户名和登录密码完成登录
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	#表单数据被提交
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		#用户不存在或者密码不匹配
		if user is None or not user.check_password(form.password.data):
			flash('无效的用户名或密码')
			return redirect(url_for('login'))
		#将用户登录状态注册为已登录，用户实例赋值给current_user变量
		login_user(user, remember=form.remember_me.data)
		#登录后的页面重定向到首页
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
			return redirect(next_page)
	return render_template('login.html', title='登录', form=form)


'''
用户注册
进入注册页面，完成注册信息的填写，信息会存储在数据库中
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	#表单数据被提交
	if form.validate_on_submit():
		#提交按钮按下
		if form.submit.data:
			user = User(username=form.username.data, email=form.email.data, telephone=form.telephone.data)
			if form.password.data != '':
				#明文密码进行加密
				user.set_password(form.password.data)
				try:
					#数据提交到数据库中
					db.session.add(user)
					db.session.commit()
					flash('恭喜你成为中科晶上的新用户')
					#注册成功，返回登录的页面
					return redirect(url_for('login'))
				except:
					traceback.print_exc()
					db.rollback()
					flash("注册失败")
					return redirect(url_for('register'))
			else:
				flash('请输入密码')
	return render_template('register.html', title='注册', form=form)


'''
退出登录
退出当前用户登录的状态，返回首页
'''
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


'''
用户中心
进入用户中心页面，当前页面会记录上次登录的时间以及查看相关信息
'''
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)


'''
资料编辑
进入用户资料编辑页面，修改用户的部分资料(用户名和所处公司)
'''
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	#表单数据被提交
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.company = form.company.data
		#修改内容提交到数据库中
		db.session.commit()
		flash('你的提交已变更')
		return redirect(url_for('edit_profile'))
	#请求方式为GET时，当前页面显示的是当前用户的信息
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.company.data = current_user.company
	return render_template('edit_profile.html', title='资料编辑',form=form)


'''
打开图片
利用OpenCV作为媒介，读取图片并编码
'''
class OpenPic(object):
	def get_frame(self, path):
		image = cv.imread(path) 
		ret, jpeg = cv.imencode('.jpg', image)
		return jpeg.tobytes()


'''
数据迭代
图片编码后的数据借用迭代器，使占用的内存最小
'''
def gen1(camera,path):
	while True:
		frame = camera.get_frame(path)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


'''
入侵相机对应图片查询
借由前端得到的相机ID查询图片路径，返回前端显示
'''
@app.route('/PicPath1/<cameraid>')
def PicPath1(cameraid):
	camera_information = Camera_Information.query.filter_by(cameraid=cameraid).order_by(desc('id')).first_or_404()
	path = camera_information.imagepath
	return Response(gen1(OpenPic(),path), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
入侵页面
打开入侵页面，输入需要查询的额摄像机的ID
'''
@app.route('/open_image',methods=['GET', 'POST'])
def open_image():
	form = IntrusionForm()
	cameraid = ""
	if form.validate_on_submit():
		cameraid=form.cameraid.data
	return render_template('intrusion.html', cameraid=cameraid, form=form)


'''
数据迭代
图片编码后的数据借用迭代器，使占用的内存最小
'''
def gen2(camera,path):
	while True:
		frame = camera.get_frame(path)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


'''
检测相机对应图片查询
借由前端得到的相机ID查询图片路径，返回前端显示
'''
@app.route('/PicPath2/<cameraid>')
def PicPath2(cameraid):
	camera_information = Camera_Information.query.filter_by(cameraid=cameraid).order_by(desc('id')).first_or_404()
	path = camera_information.imagepath
	return Response(gen2(OpenPic(), path), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
检测页面
打开检测页面，输入需要查询的额摄像机的ID
'''
@app.route('/yolo_detect',methods=['GET', 'POST'])
def yolo_detect():
	form = DetectForm()
	cameraid = ""
	if form.validate_on_submit():
		cameraid=form.cameraid.data
	return render_template('yolo_detect.html', cameraid=cameraid, form=form)


