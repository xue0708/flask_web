# -*- coding: utf-8 -*-
import sys
import os
import importlib
import json
import base64
import random
importlib.reload(sys)

from datetime import datetime
from werkzeug.urls import url_parse
from app.models import *
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from sqlalchemy import *
from flask_redis import FlaskRedis
from app import app

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Sylincom')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	#表单数据被提交
	if form.validate_on_submit():
		#提交按钮按下
		if form.submit.data:
			user = User(username=form.username.data)
			if form.password.data != '':
				#明文密码进行加密
				user.set_password(form.password.data)
				try:
					#数据提交到数据库中
					db.session.add(user)
					db.session.commit()
					flash('恭喜注册成功')
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


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    #表单数据被提交
    if form.validate_on_submit():
        current_user.username = form.username.data
        #修改内容提交到数据库中
        db.session.commit()
        flash('你的提交已变更')
        return redirect(url_for('edit_profile'))
    #请求方式为GET时，当前页面显示的是当前用户的信息
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='资料编辑',form=form)


@app.route('/overview')
def overview():
    return render_template('overview.html')


@app.route('/setData/', methods=["GET","POST"])
def setData():
    table_data = Table1.query.order_by(desc('id')).first_or_404()
    data = {"echatX":table_data.timetag, "echatY":table_data.dx, "echatY2":table_data.dy, "echatY3":table_data.dz, 
            "echatY4":table_data.gx, "echatY5":table_data.gy, "echatY6":table_data.gz}    
    return jsonify(data)

