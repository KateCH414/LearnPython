# --*-- cording:utf-8 --*--
from urllib import request, parse
import ssl

if __name__ == '__main__':
    # Get
    # urllib的request模块可以非常方便地抓取URL内容，也就是发送一个GET请求到指定的页面，然后返回HTTP的响应：
    # 对豆瓣的一个URL https://api.douban.com/v2/book/2129650 进行抓取，并返回响应
    context = ssl._create_unverified_context()  # 处理证书

    with request.urlopen('https://restapi.amap.com/v3/weather/weatherInfo', context=context) as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for key, value in f.getheaders():
            print('%s: %s' % (key, value))
        print('Data:', data.decode('utf-8'))

    print('----------------------------------')
    # 要想模拟浏览器发送GET请求，就需要使用Request对象，通过往Request对象添加HTTP头，我们就可以把请求伪装成浏览器。
    # 例如，模拟iPhone 6去请求豆瓣首页：
    # 这样豆瓣会返回适合iPhone的移动版网页：
    req = request.Request('http://www.douban.com/')
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req, context=context) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))
        # <html itemscope itemtype="http://schema.org/WebPage" class="ua-safari ua-mobile ">

    print('---------------------------------')
    # POST发送一个请求，只需要把参数data以bytes形式传入
    # 模拟一个微博登录，先读取登录的邮箱和口令，然后按照weibo.cn的登录页的格式以username=xxx&password=xxx的编码传入：
    print('Login to weibo.cn...')
    email = input('Email: ')
    passwd = input('Password: ')
    login_data = parse.urlencode([
        ('username', email),
        ('password', passwd),
        ('savestate', '1'),
        ('ec', ''),
        ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
    ])

    req = request.Request('https://passport.weibo.cn/sso/login')

    req.add_header('Origin', 'https://passport.weibo.cn')
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    req.add_header('Referer',
                   'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')
    with request.urlopen(req, context=context, data= login_data.encode('utf-8')) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))

    # Handler
    # 如果还需要更复杂的控制，比如通过一个Proxy去访问网站，我们需要利用ProxyHandler来处理，示例代码如下：
    proxy_handler =  request.ProxyHandler({'http': 'http://www.example.com:3128/'})
    proxy_auth_handler = request.ProxyBasicAuthHandler()
    proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
    opener =  request.build_opener(proxy_handler,proxy_auth_handler)
    with opener.open('http://www.example.com/login.html') as f:
        pass






