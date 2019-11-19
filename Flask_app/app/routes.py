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
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from sqlalchemy import *
from app import app
from app.jpush import jpush_grouping

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


'''
用户登录
进入登录页面，输入用户名和登录密码完成登录
'''
@app.route('/login', methods=['POST'])
def login():
	#判断用户是否注册
	haveregisted = User.query.filter_by(username=request.form['username']).first()
	if haveregisted is not None:
		#判断密码是否一致
		passwordRight = User.query.filter_by(username=request.form['username'],password_hash=request.form['password']).first()
		if passwordRight is not None:
			dict1 = {"msg":"登录成功","code":0}
			return jsonify(dict1)
		else:
			dict2 = {"msg":"密码错误","code":1}
			return jsonify(dict2)
	else:
		dict3 = {"msg":"用户不存在","code":2}
		return jsonify(dict3)


'''
用户注册
进入注册页面，完成注册信息的填写，信息会存储在数据库中
'''
@app.route('/register', methods=['POST'])
def register():
	#判断用户是否注册
	haveregisted = User.query.filter_by(username=request.form['username']).first()
	if haveregisted is not None:
		dict1 = {"msg":"用户已存在","code":1}
		return jsonify(dict1)
	else:
		#判断邮箱是否已被占用
		haveEmail = User.query.filter_by(email=request.form['email']).first()
		if haveEmail is not None:
			dict2 = {"msg":"邮箱已被占用","code":2}
			return jsonify(dict2)
		else:
			#判断手机号是否已被占用
			havephone = User.query.filter_by(telephone=request.form['telephone']).first()
			if havephone is not None:
				dict3 = {"msg":"手机号已被占用","code":3}
				return jsonify(dict3)
			else:
				#数据库数据提交
				userInfo = User(username=request.form['username'],email=request.form['email'],telephone=request.form['telephone'],password_hash=request.form['password'])
				db.session.add(userInfo)
				db.session.commit()
				dict0 = {"msg":"注册成功","code":0}
				return jsonify(dict0)


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
def gen(camera,path):
	while True:
		frame = camera.get_frame(path)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


'''
入侵摄像机
输入需要查询的摄像机ID
'''
@app.route('/intrusion', methods=['POST'])
def intrusion():
	cameraid = request.form['cameraid']
	if cameraid is not None:
		dict0 = {"msg":"查询成功","code":0}
		return jsonify(dict0)
	else:
		dict1 = {"msg":"查询失败","code":1}
		return jsonify(dict1)


'''
查看入侵图片
返回HTML网页供手机端加载显示
'''
@app.route('/intrusion/<cameraid>', methods=['POST','GET'])
def intrusion_display(cameraid):
	return render_template('intrusion.html',cameraid=cameraid)


'''
入侵相机对应图片查询
借由前端得到的相机ID查询图片路径，将图片编码，返回前端显示
'''
@app.route('/PicPath1/<cameraid>',methods=['GET'])
def PicPath1(cameraid):
	#查询图片所在的路径
	camera_information = Camera_Information.query.filter_by(cameraid=cameraid).order_by(desc('id')).first_or_404()
	path = camera_information.imagepath
	return Response(gen(OpenPic(),path), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
检测摄像机
输入需要检测的摄像机ID
'''
@app.route('/detect', methods=['POST'])
def detect():
	cameraid = request.form['cameraid']
	if cameraid is not None:
		dict0 = {"msg":"查询成功","code":0}
		return jsonify(dict0)
	else:
		dict1 = {"msg":"查询失败","code":1}
		return jsonify(dict1)


'''
查看检测图片
返回HTML网页供手机端加载显示
'''
@app.route('/detect/<cameraid>', methods=['POST','GET'])
def detect_display(cameraid):
	return render_template('detect.html',cameraid=cameraid)


'''
检测相机对应图片查询
借由前端得到的相机ID查询图片路径，将图片编码，返回前端显示
'''
@app.route('/PicPath2/<cameraid>',methods=['GET'])
def PicPath2(cameraid):
	#查询图片所在的路径
	abnormaldetect = Abnormaldetect.query.filter_by(cameraid=cameraid).order_by(desc('id')).first_or_404()
	path = abnormaldetect.imagepath
	return Response(gen2(OpenPic(), path), mimetype='multipart/x-mixed-replace; boundary=frame')


'''
资料编辑
进入用户资料编辑页面，修改用户的部分资料(邮箱/手机号/所处公司)
'''
@app.route('/edit_profile/<name>', methods=['POST'])
def edit_profile():
	#查询当前用户
	user = User.query.filter_by(username=name).first()
	if user is not None:
		#资料修改
		user.email = request.form['email']
		user.telephone = request.form['telephone']
		user.company = request.form['company']
		db.session.add(user)
		db.session.commit()
		dict0 = {"msg":"资料修改成功","code":0}
		return jsonify(dict0)



