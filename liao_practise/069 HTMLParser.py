# --*-- coding:utf-8 --*--
# 如果我们要编写一个搜索引擎，第一步是用爬虫把目标网站的页面抓下来，
# 第二步就是解析该HTML页面，看看里面的内容到底是新闻、图片还是视频。

# HTML本质上是XML的子集，但是HTML的语法没有XML那么严格，所以不能用标准的DOM或SAX来解析HTML。
# HTMLParser采用的是一种事件驱动的模式，当HTMLParser找到一个特定的标记时，它会去调用一个用户定义的函数，以此来通知程序处理。
# 它主要的回调函数的命名都是以handler_开头的，都HTMLParser的成员函数。
# 当我们使用时，就从HTMLParser派生出新的类，然后重新定义这几个以handler_开头的函数即可
# 好在Python提供了HTMLParser来非常方便地解析HTML，只需简单几行代码：

import ssl
from urllib import request
from html.parser import HTMLParser
from html.entities import name2codepoint
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # 初始化信息保存变量information，其结构为['']
        self.information = []
        self.index = 0
        # 信息标志位
        self._date_name_flag = 0
        self._date_time_flag = 0
        self._date_place_flag = 0



    def handle_starttag(self, tag, attrs):

        # if len(attrs) != 0:
        #     print('attrs')
        #     print(attrs)
        #     # [('class', 'event-title')]

        def _attr(attrlist, attrname):  # 接受的参数都是 attrs，和‘class’
            for attr in attrlist:  # attrs 是[(),()]类的，那attr就是里面的list
                if attr[0] == attrname:  # 如果匹配，返回attr[1]
                    return attr[1]
            return None
        if tag == 'time':
            self._date_time_flag = 1
        if _attr(attrs, 'class') == 'event-title':
            self._date_name_flag = 1
        if _attr(attrs, 'class') == 'event-location':
            self._date_place_flag = 1

    def handle_endtag(self, tag):
        # 标志归位
        self._date_name_flag = 0
        self._date_time_flag = 0
        self._date_place_flag = 0

    # def handle_startendtag(self, tag, attrs):
    #     print('<%s/>' % tag)

    def handle_data(self, data):
        # 判断标志处理 data
        if self._date_time_flag == 1:
            self.information.append(str(data.encode('utf_8')))
        if self._date_name_flag == 1:
            self.information.append(str(data.encode('utf_8')))
        if self._date_place_flag == 1:
            self.information.append(str(data.encode('utf_8')))

    # def handle_comment(self, data):
    #     print('<!--', data, '-->')
    #
    # def handle_entityref(self, name):
    #     print('&%s;' % name)
    #
    # def handle_charref(self, name):
    #     print('&#%s;' % name)


if __name__ == '__main__':
    parser = MyHTMLParser()
    parser.feed('''<html>
    <head></head>
    <body>
    <!-- test html parser -->
        <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    </body></html>''')
    # feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去。
    # 特殊字符有两种，一种是英文表示的&nbsp;，一种是数字表示的&#1234;，这两种字符都可以通过Parser解析出来。

    # 练习 ：找一个网页，例如https://www.python.org/events/python-events/，
    #       用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
    print('---------------------------------------------')
    context = ssl._create_unverified_context()  # 处理证书
    with request.urlopen('https://www.python.org/events/python-events/', context=context) as f:
        data = f.read()
        # print('Data:', data.decode('utf-8'))
        parser.feed(str(data))
    for info in parser.information:
        print(info)




