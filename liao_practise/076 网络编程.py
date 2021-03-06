# --*-- coding:utf-8 --*--
# 网络通信是两台计算机上的两个进程之间的通信
# 比如，浏览器进程和新浪服务器上的某个Web服务进程在通信，而QQ进程是和腾讯的某个服务器上的某个进程在通信
# 用Python进行网络编程，就是在Python程序本身这个进程内，连接别的服务器进程的通信端口进行通信。

# 为了把全世界的所有不同类型的计算机都连接起来，就必须规定一套全球通用的协议
# 互联网协议簇（Internet Protocol Suite）就是通用协议标准
# 互联网协议包含了上百种协议标准，但是最重要的两个协议是TCP和IP协议
# 互联网的协议简称TCP/IP协议。
# 通信的时候，双方必须知道对方的标识,互联网上每个计算机的唯一标识就是IP地址，类似123.123.123.123
# 一台计算机同时接入到两个或更多的网络，比如路由器，它就会有两个或多个IP地址，
# 所以，IP地址对应的实际上是计算机的网络接口，通常是网卡。

# IP协议负责把数据从一台计算机通过网络发送到另一台计算机。数据被分割成一小块一小块，然后通过IP包发送出去。
# 由于互联网链路复杂，两台计算机之间经常有多条线路，因此，路由器就负责决定如何把一个IP包转发出去。
# IP包的特点是按块发送，途径多个路由，但不保证能到达，也不保证顺序到达
# IP地址实际上是一个32位整数（称为IPv4
# 以字符串表示的IP地址如192.168.0.1实际上是把32位整数按8位分组后的数字表示，目的是便于阅读。
# IPv6地址实际上是一个128位整数，它是目前使用的IPv4的升级版，以字符串表示类似于2001:0db8:85a3:0042:1000:8a2e:0370:7334

# TCP协议则是建立在IP协议之上的。TCP协议负责在两台计算机之间建立可靠连接，保证数据包按顺序到达。
# TCP协议会通过握手建立连接，然后，对每个IP包编号，确保对方按顺序收到，如果包丢掉了，就自动重发。

# 许多常用的更高级的协议都是建立在TCP协议基础上的，比如用于浏览器的HTTP协议、发送邮件的SMTP协议等
# 一个TCP报文除了包含要传输的数据外，还包含源IP地址和目标IP地址，源端口和目标端口。
# 端口有什么作用, 因为同一台计算机上跑着多个网络程序。一个TCP报文来了之后，到底是交给浏览器还是QQ，就需要端口号来区分
# 一个进程也可能同时与多个计算机建立链接，因此它会申请很多端口。

# Socket是网络编程的一个抽象概念。通常我们用一个Socket表示“打开了一个网络链接”，
# 而打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可
# 大多数连接都是可靠的TCP连接。创建TCP连接时，主动发起连接的叫客户端，被动响应连接的叫服务器

# 创建一个基于TCP连接的Socket
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.sina.com.cn', 80))

# AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6
# SOCK_STREAM指定使用面向流的TCP协议
# 新浪网站的IP地址可以用域名www.sina.com.cn自动转换到IP地址
# 怎么知道新浪服务器的端口号,
# 作为服务器，提供什么样的服务，端口号就必须固定下来。由于我们想要访问网页，
# 因此新浪提供网页服务的服务器必须把端口号固定在80端口，因为80端口是Web服务的标准端口。
# 其他服务都有对应的标准端口号，例如SMTP服务是25端口，FTP服务是21端口，
# 端口号小于1024的是Internet标准服务的端口，端口号大于1024的，可以任意使用。

# 建立TCP连接后，我们就可以向新浪服务器发送请求，要求返回首页的内容
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# TCP连接创建的是双向通道，双方都可以同时给对方发数据
# 发送规则要根据具体的协议来决定。
# 例如，HTTP协议规定客户端必须先发请求给服务器，服务器收到后才发数据给客户端
# 发送的文本格式必须符合HTTP标准，如果格式没问题，接下来就可以接收新浪服务器返回的数据

buffer = []
while True:
    # 每次最多接收1K字节
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break

data = b''.join(buffer)

# 接收数据时，调用recv(max)方法，一次最多接收指定的字节数
# 在一个while循环中反复接收，直到recv()返回空数据，表示接收完毕，退出循环。
# 当我们接收完数据后，调用close()方法关闭Socket，这样，一次完整的网络通信就结束了
s.close()

# 接收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件：
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
with open('sina.html', 'wb') as f:
    f.write(html)

