# --*-- coding:utf-8 --*--
# 连接建立后，服务器首先发一条欢迎消息，然后等待客户端数据，并加上Hello再发送给客户端。如果客户端发送了exit字符串，就直接关闭连接。
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()

# 运行服务
# 先运行起来服务端，再运行客户端
# 需要注意的是，客户端程序运行完毕就退出了，
# 而服务器程序会永远运行下去，必须按Ctrl+C退出程序。
# 对于客户端，要主动连接服务器的IP和指定端口，
# 对于服务器，要首先监听指定端口，然后，对每一个新的连接，创建一个线程或进程来处理。通常，服务器程序会无限运行下去。

# 同一个端口，被一个Socket绑定了以后，就不能被别的Socket绑定了


