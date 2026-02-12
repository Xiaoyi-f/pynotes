"""
网络编程对所有开发语言都是一样的，Python也不例外。用Python进行网络编程，就是在Python程序本身这个进程内，
连接别的服务器进程的通信端口进行通信
网络编程就是两个进程间的通信
为了把全世界的所有不同类型的计算机都连接起来，
就必须规定一套全球通用的协议，为了实现互联网这个目标，互联网协议簇（Internet Protocol Suite）就是通用协议标准。
Internet是由inter和net两个单词组合起来的，原意就是连接“网络”的网络，有了Internet，
任何私有网络，只要支持这个协议，就可以联入互联网
最重要的两个协议是TCP和IP协议，所以，大家把互联网的协议简称TCP/IP协议
互联网上每个计算机的唯一标识就是IP地址，类似123.123.123.123。如果一台计算机同时接入到两个或更多的网络，比如路由器，它就会有两个或多个IP地址，所以，
IP地址对应的实际上是计算机的网络接口，通常是网卡
IP协议负责把数据从一台计算机通过网络发送到另一台计算机。数据被分割成一小块一小块，然后通过IP包发送出去。由于互联网链路复杂，两台计算机之间经常有多条线路，因此，
路由器就负责决定如何把一个IP包转发出去。IP包的特点是按块发送，途径多个路由，但不保证能到达，也不保证顺序到达
TCP协议则是建立在IP协议之上的。TCP协议负责在两台计算机之间建立可靠连接，保证数据包按顺序到达。TCP协议会通过握手建立连接，然后，对每个IP包编号，确保对方按顺序收到，如果包丢掉了，就自动重发。
许多常用的更高级的协议都是建立在TCP协议基础上的，比如用于浏览器的HTTP协议、发送邮件的SMTP协议等。
一个TCP报文除了包含要传输的数据外，还包含源IP地址和目标IP地址，源端口和目标端口
每个网络程序都向操作系统申请唯一的端口号，这样，两个进程在两台计算机之间建立网络连接就需要各自的IP地址和各自的端口号
一个进程也可能同时与多个计算机建立链接，因此它会申请很多端口
每个网络程序都向操作系统申请唯一的端口号，这样，两个进程在两台计算机之间建立网络连接就需要各自的IP地址和各自的端口号
"""

import socket

"""TCP套接字"""
# 基础服务端
socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_fd.bind(("127.0.0.1", 2888))
socket_fd.listen(8)

while True:
    print("正在等待客户端的连接…")
    try:
        conn_fd, addr = socket_fd.accept()
        print(f"客户端 {addr[0]}:{addr[1]} 已连接。")
    except KeyboardInterrupt:
        break
    while True:
        data_recv = conn_fd.recv(1024)
        if not data_recv:
            break
        print(f"客户端：{data_recv.decode()}")
        size = conn_fd.send("通信正常".encode())
        print(f"发送了 {size} byte 的数据。")
    conn_fd.close()
socket_fd.close()

# 基础客户端
import socket

socket_fd = socket.socket()
socket_fd.connect(("127.0.0.1", 2888))
while True:
    data_send = input("客户端：")
    if not data_send:
        print("客户端已退出。")
        break
    socket_fd.send(data_send.encode())
    data_recv = socket_fd.recv(1024)
    print(f"服务端：{data_recv.decode()}")
socket_fd.close()

# 连接浏览器
"""
发送给浏览器基本数据格式 -> HTTP协议
状态行      : HTTP/1.1 404 NotFound\r\n
响应头1     : Content-Type: text/html\r\n
空行        : \r\n
响应体      : <h1>:-(<br>Sorry, the page you requested is lost.</h1>

HTTPS就是对传送的数据加上一个新协议SSL/TLS以即其他加密协议实现加密

接收浏览器内容基本数据格式 -> HTTP协议
请求行      :
请求头部(使用上的量可自选 -》身份识别 -》不同公司识别方式可能不同) : 
空行        :\r\n
请求体       : (发送过来的实际数据)
"""


IP = "0.0.0.0"
PORT = 80


def handle(client_sock):
    print(f"已连接至{client_sock.getpeername()}")
    data_recv = client_sock.recv(4096)
    if not data_recv:  # 防止客户端因断开连接而接收到空数据导致索引越界异常
        return
    request_line = data_recv.splitlines()[0].decode()  # 将请求按行分割取第一行：请求行
    info = request_line.split(" ")[1]  # 获取请求内容
    if info == "/":
        fd_html = open("index.html", "r", encoding="UTF-8")
        data_send = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/html\r\n"
            f"\r\n"
            f"{fd_html.read()}"
        )
        fd_html.close()
    else:
        data_send = (
            "HTTP/1.1 404 NotFound\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<h1>:-(<br>Sorry, the page you requested is lost.</h1>"
        )
    client_sock.send(data_send.encode())  # 响应浏览器


def main():
    socket_fd = socket.socket()
    socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    socket_fd.bind((IP, PORT))
    socket_fd.listen(8)
    print(f"正在监听 {PORT} 端口以等待来自客户端的连接…")
    while True:
        connfd, addr = socket_fd.accept()
        handle(connfd)  # 处理来自浏览器的请求
        connfd.close()
    # socket_fd.close()


"""UDP套接字"""
# 服务端
import socket

socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建数据报套接字
socket_fd.bind(("0.0.0.0", 65088))  # 绑定地址
while True:
    print("正在等待客户端的连接…")
    try:
        data, addr = socket_fd.recvfrom(1024)  # 收消息
    except KeyboardInterrupt:
        break
    if not data:  # 断开服务端的链接。但这不是必须的，毕竟 UDP 协议是无连接的
        break
    print(f"客户端 ({addr[0]}:{addr[1]})：{data.decode()}")
    socket_fd.sendto("通信正常".encode(), addr)  # 发消息
socket_fd.close()  # 关闭套接字

# 客户端
import socket

socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建数据报套接字

HOST, PORT = "127.0.0.1", 65088
ADDR = (HOST, PORT)
while True:
    data_send = input("客户端：")
    socket_fd.sendto(data_send.encode(), ADDR)  # 发消息
    if not data_send:
        print("客户端已退出。")
        break
    data_recv, _ = socket_fd.recvfrom(1024)  # 收消息
    print(f"服务端：{data_recv.decode()}")
socket_fd.close()  # 关闭套接字

"""实现广播"""
# 发送端
import socket
from time import sleep
from datetime import datetime

DEST = ("192.168.0.255", 25533)
socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 UDP 套接字
socket_fd.setsockopt(
    socket.SOL_SOCKET, socket.SO_BROADCAST, True
)  # 使 UDP 套接字可以接收广播
print("广播服务正在运行…")
while True:
    socket_fd.sendto(f"授时广播@{datetime.now()}".encode(), DEST)  # 开始广播
    sleep(2.0)

# 接收端
import socket

socket_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 UDP 套接字
socket_fd.setsockopt(
    socket.SOL_SOCKET, socket.SO_BROADCAST, True
)  # 使 UDP 套接字可以接收广播
socket_fd.bind(("0.0.0.0", 25533))  # 选择接收端口（自动获取地址）
while True:
    try:
        msg, addr = socket_fd.recvfrom(1024)
    except KeyboardInterrupt:
        break
    else:
        print(f"来自 {addr[0]}:{addr[1]} 的消息：{msg.decode()}")
socket_fd.close()
