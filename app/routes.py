# -*- coding: utf-8 -*-
import sys
import os
import importlib
import json
import base64
import random
import pymysql
import cv2
importlib.reload(sys)

from datetime import datetime
from werkzeug.urls import url_parse
from app.models import *
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CSVDownloadForm, SetMaxNumForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from sqlalchemy import *
from flask_redis import FlaskRedis
from app import app

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


'''
数据库连接
'''
SQLdb = pymysql.connect("localhost", "root", "123456", "test_system")

num = 1
maxNum = []


'''
读取json文件
'''
def read_json():
    filename="camera_cfg.json"
    f_obj=open(filename)
    file=json.load(f_obj)
    return file


'''
查询设置的阈值
'''
@login_required
def SetMaxNum():
    maxNum.clear()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    maxNum.append(user.maxdx)
    maxNum.append(user.maxdy)
    maxNum.append(user.maxdz)
    maxNum.append(user.maxgx)
    maxNum.append(user.maxgy)
    maxNum.append(user.maxgz)


'''
opencv打开摄像头
'''
class VideoCamera():
    def __init__(self,vurl):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(vurl)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        #转化为字节流
        return jpeg.tobytes()


'''
返回数据流
'''
def gen1(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


'''
返回rtsp视频流响应
'''
@app.route('/video_feed')
def video_feed():
    address = request.args.get('address')
    rtsp_address = "\"" + address + "\""
    return Response(gen1(VideoCamera(rtsp_address)), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
首页
'''
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Sylincom')


'''
登录
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
注册
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


'''
退出
'''
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


'''
设置
'''
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)


'''
名称编辑
'''
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


'''
导出CSV
'''
@app.route('/CSV_download', methods=['GET', 'POST'])
def CSV_download():
    form = CSVDownloadForm()
    #表单数据被提交
    if form.validate_on_submit():
        num = form.number.data
        StartTime = form.startTime.data
        EndTime = form.endTime.data
        table = "data" + str(num)
        cursor = SQLdb.cursor()
        str1 = "SELECT * FROM " + table + " where timetag>='" + StartTime + "' and timetag<='" + EndTime + "'"
        str2 = " INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output.csv'"
        str3 = " Fields TERMINATED BY ',' OPTIONALLY ENCLOSED BY'\"' LINES TERMINATED BY '\n'; "
        sql = str1 + str2 + str3
        cursor.execute(sql)
        SQLdb.commit()
        flash("CSV文件导出成功")
        return redirect(url_for('CSV_download'))
    return render_template('CSV_download.html', title='导出CSV',form=form)


'''
设置阈值
'''
@app.route('/setMax', methods=['GET', 'POST'])
@login_required
def setMax():
    form = SetMaxNumForm()
    #表单数据被提交
    if form.validate_on_submit():
        current_user.maxdx = form.maxdx.data
        current_user.maxdy = form.maxdy.data
        current_user.maxdz = form.maxdz.data
        current_user.maxgx = form.maxgx.data
        current_user.maxgy = form.maxgy.data
        current_user.maxgz = form.maxgz.data
        #修改内容提交到数据库中
        db.session.commit()
        flash('你的阈值已设置')
        return redirect(url_for('setMax'))
    return render_template('setMax.html', title='设置阈值',form=form)


'''
总览
'''
@app.route('/overview')
def overview():
    return render_template('overview.html')


'''
返回数据
'''
@app.route('/setData/', methods=["GET","POST"])
def setData():
    global num
    warnText = ""
    table_datas = []
    data_timetag = []
    data_dx = []
    data_dy = []
    data_dz = []
    data_gx = []
    data_gy = []
    data_gz = []
    if num == 1:
        table_datas = Table1.query.order_by(desc('id')).limit(20).all()
        warnText = "第一组数据"
    else:
        table_datas = Table2.query.order_by(desc('id')).limit(20).all()
        warnText = "第二组数据"
    for table_data in table_datas:
        data_timetag.append(table_data.timetag)
        data_dx.append(table_data.dx)
        data_dy.append(table_data.dy)
        data_dz.append(table_data.dz)
        data_gx.append(table_data.gx)
        data_gy.append(table_data.gy)
        data_gz.append(table_data.gz)
    data = {"echatX":data_timetag, "echatY":data_dx, "echatY2":data_dy, "echatY3":data_dz, 
            "echatY4":data_gx, "echatY5":data_gy, "echatY6":data_gz, "warnText":warnText}
    num = num + 1
    if num > 2:
        num = 1 
    return jsonify(data)


'''
测点页选择组数
下述是每组数据的页面显示
'''
@app.route('/choose')
def choose():
    return render_template('choose.html')


@app.route('/Data1')
def Data1():
    file = read_json()
    if len(file)<1:
        return render_template('error.html')
    else:
        return render_template('data1.html', file=file)


@app.route('/Data2')
def Data2():
    file = read_json()
    if len(file)<2:
        return render_template('error.html')
    else:
        return render_template('data2.html', file=file)


'''
返回每组数据
'''
@app.route('/choosedata/<number>', methods=["GET","POST"])
def choosedata(number):
    table_data = []
    warnText = ""
    SetMaxNum()
    num = int(number)
    if num == 1:
        table_data = Table1.query.order_by(desc('id')).first_or_404()
    else:
        table_data = Table2.query.order_by(desc('id')).first_or_404()
    maxNum1 = list(filter(None, maxNum))
    if len(maxNum1):
        if table_data.dx>=int(maxNum1[0]) or table_data.dy>=int(maxNum1[1]) or table_data.dz>=int(maxNum1[2]) or table_data.gx>=int(maxNum1[3]) or table_data.gy>=int(maxNum1[4]) or table_data.gz>=int(maxNum1[5]) :
            warnText = "存在数据超出阈值"
    data = {"echatX":table_data.timetag, "echatY":table_data.dx, "echatY2":table_data.dy, "echatY3":table_data.dz, 
            "echatY4":table_data.gx, "echatY5":table_data.gy, "echatY6":table_data.gz, "warnText":warnText}
    return jsonify(data)

