import jpush
from jpush import common

#app_key = "c88e109c1974c010bf098b31"
#master_secret = "8a0a0b209b1a2392c5745e75"

app_key = "2f49f406f3e2c404bd1e99b3"
master_secret = "be09b33bd76513ea0d6be976"

_jpush = jpush.JPush(app_key,master_secret)
_jpush.set_logging("DEBUG")


#设置别名
def alias():
	push = _jpush.create_push()
	alias=["alias1", "alias2"]
	alias1={"alias": alias}
	#print(alias1)
	push.audience = jpush.audience(
		jpush.tag("tag1", "tag2"),
		alias1
	)

	push.notification = jpush.notification(alert = "Hello world with audience!")
	push.platform = jpush.all_
	#print(push.payload)
	push.send()


#设置错误提示
def all():
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(alert="!hello python jpush api")
	push.platform = jpush.all_
	try:
		response=push.send()
	except common.Unauthorized:
		raise common.Unauthorized("Unauthorized")
	except common.APIConnectionException:
		raise common.APIConnectionException("conn")
	except common.JPushFailure:
		print ("JPushFailure")
	except:
		print ("Exception")


#设置传播方式接口
def audience():
	push = _jpush.create_push()
	push.audience = jpush.audience(
				jpush.tag("tag1", "tag2"),
				jpush.alias("alias1", "alias2")
			)

	push.notification = jpush.notification(alert="Hello world with audience!")
	push.platform = jpush.all_
	#print (push.payload)
	push.send()


#设置消息推送接口
def notification():
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.platform = jpush.all_

	ios = jpush.ios(alert="Hello, IOS JPush!", sound="a.caf", extras={'k1':'v1'})
	android = jpush.android(alert="Hello, Android msg", priority=1, style=1, alert_type=1,big_text='jjjjjjjjjj', extras={'k1':'v1'})
	push.notification = jpush.notification(alert="Hello, JPush!", android=android, ios=ios)

	#print (push.payload)
	result = push.send()


def options():
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(alert="Hello, world!")
	push.platform = jpush.all_
	push.options = {"time_to_live":86400, "sendno":12345,"apns_production":True}
	push.send()


#各个平台的消息推送
def platfrom_msg():
	push = _jpush.create_push()
	push.audience = jpush.all_
	ios_msg = jpush.ios(alert="Hello, IOS JPush!", badge="+1", sound="a.caf", extras={'k1':'v1'})
	android_msg = jpush.android(alert="Hello, android msg")
	push.notification = jpush.notification(alert="Hello, JPush!", android=android_msg, ios=ios_msg)
	push.message=jpush.message("content",extras={'k2':'v2','k3':'v3'})
	push.platform = jpush.all_
	push.send()


def silent():
	push = _jpush.create_push()
	push.audience = jpush.all_
	ios_msg = jpush.ios(alert="Hello, IOS JPush!", badge="+1", extras={'k1':'v1'}, sound_disable=True)
	android_msg = jpush.android(alert="Hello, android msg")
	push.notification = jpush.notification(alert="Hello, JPush!", android=android_msg, ios=ios_msg)
	push.platform = jpush.all_
	push.send()


def sms():
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(alert="a sms message from python jpush api")
	push.platform = jpush.all_
	push.smsmessage=jpush.smsmessage("a sms message from python jpush api",0)
	#print (push.payload)
	push.send()


def validate():
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(alert="Hello, world!")
	push.platform = jpush.all_
	push.send_validate()


def jpush_grouping(company,message):
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(alert = message)
	push.platform = jpush.all_
	#参数数量可变，设置别名分组类型 conpany。
	alias=[company, "alias2"]
	alias1={"alias": alias}
	#print(alias1)
	push.audience = jpush.audience(
	jpush.tag("tag1", "tag2"),
	alias1
	)
	push.send()


#分组推送，推送群体，通知消息，图片url
def jpush_grouping(company,notification,url):
	push = _jpush.create_push()
	#推送平台，可以为手机的三种操作系统
	push.platform = jpush.all_
	#推送目标，参数数量可变，设置别名分组类型 conpany。
	alias=[company, "alias2"]
	alias1={"alias": alias}
	push.audience = jpush.audience(jpush.tag("tag1", "tag2"),alias1)
	#推送通知体，显示在app端的通知体
	push.notification = jpush.notification(alert = notification)
	#自定义消息图片url，点击app端show的图片
	push.message=jpush.message(url)
	push.send()


#广播推送，通知消息，图片url
def jpush_all(notification,url):
	push = _jpush.create_push()
	#推送平台，可以为手机的三种操作系统
	push.platform = jpush.all_
	#推送目标，可以为自定义的群体
	push.audience = jpush.all_
	#推送通知体，显示在app端的通知体
	push.notification = jpush.notification(alert = notification)
	#自定义消息图片url，点击app端show的图片url
	push.message=jpush.message(notification,extras={'ID':url})
	push.options = {"time_to_live":86400, "sendno":12345,"apns_production":False}
	push.send()



