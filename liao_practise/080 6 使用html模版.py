# --*-- coding:utf-8 --*--
# Web App不仅仅是处理逻辑，展示给用户的页面也非常重要,在函数中返回一个包含HTML的字符串，简单的页面还可以，但是，想想新浪首页的6000多行的HTML，你确信能在Python的字符串中正确地写出来么？
# 有Web开发经验的同学都明白，Web App最复杂的部分就在HTML页面。HTML不仅要正确，还要通过CSS美化，再加上复杂的JavaScript脚本来实现各种交互和动画效果。总之，生成HTML页面的难度很大。

# 模板技术出现
# 使用模板，我们需要预先准备一个HTML文档，这个HTML文档不是普通的HTML，而是嵌入了一些变量和指令，然后，根据我们传入的数据，替换后，得到最终的HTML，发送给用户：
# 这就是传说中的MVC：Model-View-Controller，中文名“模型-视图-控制器”。
# Python处理URL的函数就是C：Controller，Controller负责业务逻辑，比如检查用户名是否存在，取出用户信息等等；
# 包含变量{{ name }}的模板就是V：View，View负责显示逻辑，通过简单地替换一些变量，View最终输出的就是用户看到的HTML
# MVC中的Model在哪？Model是用来传给View的，这样View在替换变量的时候，就可以从Model中取出相应的数据。
#   只是因为Python支持关键字参数，很多Web框架允许传入关键字参数，然后，在框架内部组装出一个dict作为Model。

# 我们把上次直接输出字符串作为HTML的例子用高端大气上档次的MVC模式改写一下
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def signin_from():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    username = request.form['username']
    password = request.form['password']
    if username == 'cuihuan' and password == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


if __name__ == '__main__':
    app.run()

# Flask 通过render_template()函数实现模版渲染，
# 和Web框架类似，Python的模版也有多种，Flask默认支持的模版是jinja2:https://jinja.palletsprojects.com/en/3.0.x/
# 安装jinja2: pip install jinja2
# 然后编写 home.html 用来显示首页的模板：   ---见home.html
# form.html 用来展示登陆表单
# signin-ok.html 登陆成模版
# 把模板放到正确的templates目录下，templates和app.py在同级目录下

# 通过MVC，我们在Python代码中处理M：Model和C：Controller，而V：View是通过模板处理的，这样，我们就成功地把Python代码和HTML代码最大限度地分离了。
# 使用模板的另一大好处是，模板改起来很方便，而且，改完保存后，刷新浏览器就能看到最新的效果，这对于调试HTML、CSS和JavaScript的前端工程师来说实在是太重要了。

# 在Jinja2模板中
# 用{{ name }}表示一个需要替换的变量
# 需要循环、条件判断等指令语句，在Jinja2中，用{% ... %}表示指令。
# 循环输出页码：
# {% for i in page_list %}
#     <a href="/page/{{ i }}">{{ i }}</a>
# {% endfor %}
# 如果page_list是一个list：[1, 2, 3, 4, 5]，上面的模板将输出5个超链接。

# 除了Jinja2，常见的模板还有：
# Mako：用<% ... %>和${xxx}的一个模板；https://www.makotemplates.org/
# Cheetah：也是用<% ... %>和${xxx}的一个模板；https://cheetahtemplate.org/
# Django：Django是一站式框架，内置一个用{% ... %}和{{ xxx }}的模板。
