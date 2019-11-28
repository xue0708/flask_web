from app import app


'''
主函数
代码从此处开始运行，声明IP地址和端口号
'''
if __name__ == '__main__':
	app.run(host='172.17.126.219',port=30021,debug=True)
