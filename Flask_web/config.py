import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


'''
密钥
密码加密的密钥
'''
class Config(object):
	SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'


'''
数据库
数据库的连接，数据库类型是mysql
'''
class Config(object):
	#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask_demo?charset=utf8'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/jdh_system?charset=utf8'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
