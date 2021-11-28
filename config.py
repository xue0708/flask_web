import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


class Config(object):
	SECRET_KEY = 'a9087FFJFF9nnvc2@#$%FSD'


class Config(object):
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/test_system?charset=utf8'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
