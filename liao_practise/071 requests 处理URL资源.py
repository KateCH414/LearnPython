# --*-- coding: utf-8 --*--
# Python内置的urllib模块，用于访问网络资源。但是，它用起来比较麻烦，而且，缺少很多实用的高级功能。
# 更好的方案是使用requests。它是一个Python第三方库，处理URL资源特别方便。

# 安装requests
# pip install requests

import requests

if __name__ == '__main__':
    # 使用requests
    #  GET
    # r = requests.get('https://www.duban.com', verify=False)
    # print(r.status_code)
    # print(r.text)

    # 对于带参数的URL，传入一个dict作为params参数：
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    r1 = requests.get('https://www.douban.com/search', headers=header, params={'q': 'python'})
    print(r1.url)  # https://www.douban.com/search?q=python
    print(r1.status_code)
    print(r1.text)

    # requests自动检测编码，可以使用encoding属性查看：
    print(r1.encoding)  # 'utf-8'

    # 无论响应是文本还是二进制内容，我们都可以用content属性获得bytes对象：
    print(r1.content)

    # requests的方便之处还在于，对于特定类型的响应，例如JSON，可以直接获取：
    header['Connection'] = 'close'
    r3 = requests.get(
        'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json', headers=header, verify=False)
    print(r3.json())

    # 要发送POST请求，只需要把get()方法变成post()，然后传入data参数作为POST请求的数据：
    r4 = requests.post('https://accounts.douban.com/login',
                      data={'form_email': 'abc@example.com', 'form_password': '123456'})

    # # requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数：
    # url = 'www.baidu.com'
    # params = {'key': 'value'}
    # r5 = requests.post(url, json=params)  # 内部自动序列化为JSON
    #
    #
    # # 上传文件需要更复杂的编码格式，但是requests把它简化成files参数
    # upload_files = {'file': open('report.xls', 'rb')}  # 在读取文件时，注意务必使用'rb'即二进制模式读取，这样获取的bytes长度才是文件的长度
    # r6 = requests.post(url, files=upload_files)
    # # 把post()方法替换为put()，delete()等，就可以以PUT或DELETE方式请求资源。
    #
    # # requests对获取HTTP响应的其他信息也非常简单
    # # 获取响应头
    # print(r6.headers)
    # print(r6.headers['Content-Type'])
    #
    # # requests对Cookie做了特殊处理，使得我们不必解析Cookie就可以轻松获取指定的Cookie：
    # # r.cookies['ts']
    #
    # # 要在请求中传入Cookie，只需准备一个dict传入cookies参数
    # cs = {'token': '12345', 'status': 'working'}
    # r7 = requests.get(url, cookies=cs)
    #
    # # 指定超时，传入以秒为单位的timeout参数
    # r8 = requests.get(url, timeout=2.5)
    #
    #




