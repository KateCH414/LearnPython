# 了解了WSGI框架，我们发现：其实一个Web App，就是写一个WSGI的处理函数，针对每个HTTP请求进行响应。
# 问题是如何处理100个不同的URL
# 每一个URL可以对应GET和POST请求，当然还有PUT、DELETE等请求，但是我们通常只考虑最常见的GET和POST请求。
# 最简单的想法是从environ变量里取出HTTP请求的信息，然后逐个判断：
from wsgiref.simple_server import make_server
def application1(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method=='GET' and path=='/':
        return handle_home(environ, start_response)
    if method=='POST' and path=='/signin':
        return handle_signin(environ, start_response)
    ...

def handle_home():
    pass
def handle_signin():
    pass
# 这么写下去代码是肯定没法维护了

# 我们需要在WSGI接口之上能进一步抽象，让我们专注于用一个函数处理一个URL，
# 至于URL到函数的映射，就交给Web框架来做。
# Python有上百个开源的Web框架
# 选择一个比较流行的Web框架——Flask来使用。

# 安装Flask
# pip install flask

# 编写app.py, 处理3个URL，分别是：
#   GET/: 首页，返回Home
#   GET/signin :登陆页，显示登陆表单
#   POST/signin :处理登陆表单，显示登陆结果
# 注意噢，同一个URL/signin分别有GET和POST两种请求，映射到两个处理函数中。
# Flask 通过python 装饰器 在内部自动地吧URL和函数给关联起来，所以，我们写出来的代码如下


from flask import Flask,request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>home</h1>'


@app.route('/signin', methods=['GET'])
def signin_from():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>bad username or password.</h3>'


if __name__ == '__main__':
    app.run()
    # 运行程序，Flask自带的Server在端口5000上监听
    # 打开浏览器，输入首页地址http://localhost:5000/：

# 除了Flask，常见的Python Web框架还有：
# Django：全能型Web框架； https://www.djangoproject.com/
# web.py：一个小巧的Web框架；https://webpy.org/
# Bottle：和Flask类似的Web框架；http://bottlepy.org/docs/dev/
# Tornado：Facebook的开源异步Web框架。https://www.tornadoweb.org/en/stable/

# 有了Web框架，我们在编写Web应用时，注意力就从WSGI处理函数转移到URL+对应的处理函数，这样，编写Web App就更加简单了。
# 在编写URL处理函数时，除了配置URL外，从HTTP请求拿到用户数据也是非常重要的。
# Web框架都提供了自己的API来实现这些功能。Flask通过request.form['name']来获取表单的内容。



