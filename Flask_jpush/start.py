from app import app


'''
主函数
代码从此处开始运行，声明IP地址和端口号
'''
if __name__ == '__main__':
	app.run(host='10.171.1.4',port=5000,debug=True)
