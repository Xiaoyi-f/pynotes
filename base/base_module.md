import copy 

copy.copy() # 潜拷贝
copy.deepcopy # 深拷贝
import doctest

"""
>>> python_code
... indent_python_code
"""
doctest.testmod()
import time

time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime(time.time())
time.sleep()

import sys

sys.argv: list
sys.exit()
sys.path.append("path")
import os

os.getcwd()
os.listdir()
os.chdir()
os.system()
os.path.abspath()
os.path.exists()
from pathlib import Path

content = Path("file.txt").read_text()
Path("file.txt").write_text("content")

import json

json.dumps(data, ensure_ascii=False)
json.loads(jsonstr)
json.dump(data, file, ensure_ascii=False, indent=4) 
json.load(file)
"""
日志级别:
1.DEBUG
2.INFO
3.WARNING 
4.ERROR
5.CRITICAL
默认: 3以即以上的级别才报告
输出方式:
1.控制台
2.文件
"""
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s",
    filename="log.txt",
    filemode="w" # w->覆盖 a->追加 
)

logging.debug("This is a debug message")  # 默认不输出
logging.info("This is an info message")  # 默认不输出
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")

# 同时输出到控制台和文件
def setup_logger():
    """配置同时输出到控制台和文件的日志器"""
    # 创建日志器
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台只输出INFO及以上

    # 创建文件处理器
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)    # 文件输出所有级别

    # 设置格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 使用自定义日志器
logger = setup_logger()
logger.debug("这是调试信息（只写入文件）")
logger.info("这是普通信息（控制台+文件）")
logger.error("这是错误信息（控制台+文件）")

# 异常追踪（必须掌握）
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("除数不能为0")  # 自动记录异常堆栈信息

import re 

"""
基本正则:
[^0-9a-zA-Z]{m,n}
^begin\s+
*
?
last$
\^转义
?? -> 非贪婪
"""
"忽略大小写"    "多行模式"   "点号匹配所有"
flag = re.IGNORECASE | re.MULTILINE | re.DOTALL
re.search(pattern, text, flag).group(n) # n->0全,1,2...
print(findall(pattern, text, flag))
split_advance = re.split(r"[,:;.]+", text, flag)
xxx_pattern = re.compile(pattern, flag)
xxx_pattern.search(text, flag).group(n) 
xxx_pattern.findall(text, flag)
import itertools

list1, list2 = [1, 2, 3], [4, 5, 6]
chain_obj = itertools.chain(list1, list2) # 返回chain对象
list(chain_obj) # 实现延迟合并
itertools.combinations(items, n) # 顺序无关->组合
itertools.permutations(items, n) # 顺序有关->排列
itertools.cycle(iterable) # 无限循环迭代器
import contextlib

@contextmanager
def timer():
    pass # __enter__
    try:
        yield # with代码块在这里执行
    finally:
        pass # __exit__
from enum import Enum, Flag, auto
from enum import IntEnum, IntFlag

# 严格类型
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED.name)
print(Color.RED.value)

# 支持组合/严格类型
class Root(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    DELETE = auto()

user_root = root.read | root.write

# 由于Flag 和 Enum -> 严格类型
# 需要比较数值 -> 使用 IntEnum 和 IntFlag
import random

nums = [1, 3, 5, 7, 9]
demo = random.Random()
demo_int = demo.randrange(start, end) # 包前不包后
demo_float = demo.uniform(start, end) # 包前包后
demo_choice = demo.choice(nums)
demo_sample = demo.sample(nums, n)
demo.shuffle(nums)
import shutil

shutil.copyfile("source", "target")
shutil.copytree("source", "target")
shutil.move("old", "new")
shutil.rmtree("url")
usage = shutil.disk_usage("url_disk")
usage.total
usage.free
usage.used
import socket

"""TCP套接字"""
# 基础服务端
# fd一般指代文件描述符
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
# 响应
发送给浏览器基本数据格式 -> HTTP协议
状态行      : HTTP/1.1 404 NotFound\r\n
响应头1     : Content-Type: text/html\r\n
空行        : \r\n
响应体      : <h1>:-(<br>Sorry, the page you requested is lost.</h1>

HTTPS就是对传送的数据加上一个新协议SSL/TLS以即其他加密协议实现加密

# 请求
接收浏览器内容基本数据格式 -> HTTP协议
请求行      示例: GET / HTTP/1.1
请求头部 
示例: 
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
Accept: text/html...
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
# 提示: socket模块的UDP协议使用在此略
import unittest

class TestDemo(unittest.TestCase):
    def setUp(self):  # 每个测试前执行
        pass

    def tearDown(self):  # 每个测试后执行
        pass

    def test_add(self):  # 测试函数
        self.assertEqual(1 + 1, 2)
        self.assertTrue(True)
        self.assertIn(1, [1, 2])
        self.assertIsNone(None)

        # 异常测试
        with self.assertRaises(ValueError):
            int('abc') # 会报错 --> 匹配测试异常，相同则通过测试


if __name__ == '__main__':
    unittest.main()

# 命令行运行
# python -m unittest test.py
# python -m unittest discover  # 自动发现所有测试文件并进行测试
import threading
import time

# 1. 创建和启动线程
def task(name, seconds):
    print(f"线程{name}开始")
    time.sleep(seconds)
    print(f"线程{name}结束")

# 创建线程
t1 = threading.Thread(target=task, args=("A", 2))
t2 = threading.Thread(target=task, kwargs={"name": "B", "seconds": 1})

# 启动线程
t1.start()
t2.start()

# 等待线程结束
t1.join()
t2.join()
print("主线程结束")

# 2. 守护线程（主线程结束，子线程强制结束）
t = threading.Thread(target=task, args=("守护", 5), daemon=True)
t.start()
# 主线程不等待守护线程

# 3. 互斥锁（解决资源竞争）
lock = threading.Lock()
count = 0

def safe_increment():
    global count
    for _ in range(100000):
        lock.acquire()
        count += 1
        lock.release()

# 或使用with语法（推荐）
def safe_increment2():
    global count
    for _ in range(100000):
        with lock:
            count += 1

# 4. 线程局部数据（每个线程独立）
local_data = threading.local()

def set_data():
    local_data.value = threading.current_thread().name
    time.sleep(0.1)
    print(f"{threading.current_thread().name}: {local_data.value}")

# 5. 信号量（控制并发数量）
semaphore = threading.Semaphore(3)

def limited_task():
    with semaphore:
        print(f"{threading.current_thread().name} 执行")
        time.sleep(1)

# 6. 事件（线程间通信）
event = threading.Event()

def waiter():
    print("等待事件...")
    event.wait()
    print("收到事件，继续执行")

def setter():
    time.sleep(2)
    print("设置事件")
    event.set()

# 7. 线程池（工作中最常用）
from concurrent.futures import ThreadPoolExecutor

def work(x):
    return x * x

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(work, [1, 2, 3, 4, 5])
    print(list(results))
import multiprocessing
import os
import time

# 1. 创建和启动进程
def work(name, seconds):
    print(f"进程{name} ID: {os.getpid()}, 父进程: {os.getppid()}")
    time.sleep(seconds)
    print(f"进程{name}结束")

if __name__ == "__main__":
    # 创建进程
    p1 = multiprocessing.Process(target=work, args=("A", 2))
    p2 = multiprocessing.Process(target=work, kwargs={"name": "B", "seconds": 1})

    # 启动进程
    p1.start()
    p2.start()

    # 等待进程结束
    p1.join()
    p2.join()
    print("主进程结束")

# 2. 进程间不共享全局变量
my_list = []

def write_data():
    global my_list
    for i in range(3):
        my_list.append(i)
        print(f"写入: {i}")
    print(f"写入进程list: {my_list}")

def read_data():
    print(f"读取进程list: {my_list}")  # 输出 []，数据不共享

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=write_data)
    p2 = multiprocessing.Process(target=read_data)
    p1.start()
    p1.join()
    p2.start()
    p2.join()

# 3. 进程间通信 - Queue（最常用）
def producer(q):
    for i in range(5):
        q.put(f"数据{i}")
        print(f"生产: {i}")

def consumer(q):
    while True:
        data = q.get()
        if data is None:
            break
        print(f"消费: {data}")

if __name__ == "__main__":
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))

    p1.start()
    p2.start()
    p1.join()
    q.put(None)  # 结束信号
    p2.join()

# 4. 进程池（工作中最常用）
from multiprocessing import Pool

def task(n):
    print(f"进程{os.getpid()} 计算: {n}")
    return n * n

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # 方式1：map（同步）
        results = pool.map(task, [1, 2, 3, 4, 5])
        print(results)

        # 方式2：apply_async（异步）
        results = [pool.apply_async(task, args=(i,)) for i in range(5)]
        for r in results:
            print(r.get())

# 5. 守护进程
def daemon_task():
    while True:
        print("守护进程运行中...")
        time.sleep(1)

if __name__ == "__main__":
    p = multiprocessing.Process(target=daemon_task)
    p.daemon = True  # 设置为守护进程
    p.start()

    time.sleep(3)
    print("主进程结束，守护进程被强制结束")
    # 主进程结束，守护进程自动结束

# 6. 进程锁（解决资源竞争）
lock = multiprocessing.Lock()

def safe_work(lock, num):
    with lock:
        print(f"进程{os.getpid()} 获得锁，执行: {num}")
        time.sleep(1)

if __name__ == "__main__":
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=safe_work, args=(lock, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
import hashlib
import hmac
import os


# 字符串哈希
def normal_hash():
    # 字符串哈希
    data = "hello world"
    hash_data = hashlib.sha256(data.encode()).hexdigest()
    # b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    # 转成16进制字符串返回
    return hash_data.hexdigest()


# 密码哈希
def password_hash():
    password = "user123456"

    # 生成随机盐（每个用户不同）
    salt = os.urandom(16)  # 16字节盐

    # 计算哈希
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",  # 哈希算法
        password.encode(),  # 密码转bytes
        salt,  # 盐
        100000,  # 迭代次数（越大越安全，越慢）
        dklen=32,  # 输出长度
    )
    # 转十六进制存数据库
    salt_hex = salt.hex()
    hash_hex = hash_bytes.hex()

    # 验证密码 -> python允许函数嵌套，函数是对象
    def verify(input_pwd, stored_salt_hex, stored_hash_hex):
        salt = bytes.fromhex(stored_salt_hex)
        test_hash = hashlib.pbkdf2_hmac(
            "sha256", input_pwd.encode(), salt, 100000
        ).hex()
        return test_hash == stored_hash_hex

    return salt_hex, hash_hex, verify


# 约定密钥（就像暗号）
密钥 = b"our_secret_key"  # 客户端和服务器都知道

# 要保护的消息
消息 = b"transfer 100 yuan"

# 生成签名（贴防伪标签）
签名 = hmac.new(
    key=密钥, msg=消息, digestmod=hashlib.sha256  # 暗号  # 内容  # 算法
).hexdigest()  # 转成16进制字符串

print(f"签名: {签名}")


# 验证签名（检查是否被篡改）
def 验证(原始消息, 收到的签名):
    """验证消息是否真实"""
    # 重新计算应该的签名
    应该的签名 = hmac.new(key=密钥, msg=原始消息, digestmod=hashlib.sha256).hexdigest()

    # 安全比较（必须用这个！）
    return hmac.compare_digest(收到的签名, 应该的签名)


# 测试
print(验证(b"transfer 100 yuan", 签名))  # True（没被改过）
print(验证(b"transfer 10000 yuan", 签名))  # False（被篡改了）
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.header import Header

class EmailSender:
    def __init__(self, smtp_server, port, username, password, use_ssl=True):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
    
    def send(self, to_addrs, subject, content, content_type='plain', cc_addrs=None, attachments=None, sender_name=''):
        try:
            msg = EmailMessage()
            msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), self.username)) if sender_name else self.username
            msg['To'] = ', '.join(to_addrs)
            if cc_addrs:
                msg['Cc'] = ', '.join(cc_addrs)
            msg['Subject'] = Header(subject, 'utf-8')
            
            if content_type == 'html':
                msg.add_alternative(content, subtype='html')
            else:
                msg.set_content(content)
            
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=file_path.split('/')[-1])
            
            all_recipients = to_addrs + (cc_addrs or [])
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg, self.username, all_recipients)
            else:
                with smtplib.SMTP(self.smtp_server, self.port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg, self.username, all_recipients)
            
            return True
        except Exception as e:
            print(f"发送失败: {e}")
            return False

# 使用
sender = EmailSender('smtp.qq.com', 邮箱端口, 'your_email@qq.com', 'your_code')
sender.send(['receiver@example.com'], '测试', '正文')
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import os

# pip install pillow


# 图形验证码
def generate_captcha(text=None, width=120, height=40):
    """生成验证码图片

    Args:
        text: 验证码文字（默认随机4位）
        width: 图片宽
        height: 图片高
    Returns:
        (图片对象, 验证码文字)
    """
    # 1. 生成随机验证码（默认4位：数字+大写字母）
    if text is None:
        text = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    # 2. 创建空白图片（RGB模式，背景色随机浅色）
    bg_color = (
        random.randint(200, 255),
        random.randint(200, 255),
        random.randint(200, 255),
    )
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    # 3. 字体设置（工作用绝对路径或系统字体）
    try:
        # Windows常用字体路径
        font_paths = [
            "C:/Windows/Fonts/Arial.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Arial.ttf",  # Mac
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 30)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    # 4. 绘制文字（每个字符随机位置、颜色）
    x = 10
    for i, char in enumerate(text):
        y = random.randint(5, 10)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        draw.text((x, y), char, fill=color, font=font)
        x += 25  # 字符间距
    # 5. 添加干扰线（2-3条）
    for _ in range(random.randint(2, 3)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(150, 150, 150), width=1)
    # 6. 添加噪点
    for _ in range(100):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        img.putpixel((x, y), (0, 0, 0))

    return img, text


def save_captcha(img, text, save_dir="captchas"):
    """保存验证码（文件名用验证码文字，方便调试）"""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{text}.png")
    img.save(path)
    print(f"验证码已保存: {path}")
    return path


def verify_captcha(user_input, correct_text):
    """验证用户输入（忽略大小写）"""
    return user_input.upper() == correct_text.upper()


def batch_generate_captcha(count=10):
    """批量生成验证码（用于测试/训练）"""
    captchas = []
    for i in range(count):
        img, text = generate_captcha()
        captchas.append((img, text))
        img.save(f"captcha_{i}_{text}.png")
    return captchas

from PIL import Image, ImageDraw
import qrcode

# 配置参数（请修改这些值）
二维码内容 = "https://example.com"  # 要生成二维码的网址或文本
Logo宽度 = 50                         # Logo图片宽度（像素）
Logo高度 = 50                         # Logo图片高度（像素）
Logo背景色 = "#FF6B6B"                # Logo背景颜色（十六进制）
Logo前景色 = "#4ECDC4"                # Logo前景颜色（十六进制）
椭圆左上角X = 10                       # 椭圆左上角X坐标
椭圆左上角Y = 10                       # 椭圆左上角Y坐标
椭圆右下角X = 40                       # 椭圆右下角X坐标
椭圆右下角Y = 40                       # 椭圆右下角Y坐标
粘贴X坐标 = 二维码图片宽度 // 2 - 25     # 粘贴位置的X坐标
粘贴Y坐标 = 二维码图片高度 // 2 - 25     # 粘贴位置的Y坐标
输出文件名 = "qr.png"                   # 输出的图片文件名

# 生成二维码
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data(二维码内容)
qr.make(fit=True)
img = qr.make_image().convert("RGB")
二维码图片宽度, 二维码图片高度 = img.size

# 生成Logo
logo = Image.new("RGB", (Logo宽度, Logo高度), Logo背景色)
draw = ImageDraw.Draw(logo)
draw.ellipse((椭圆左上角X, 椭圆左上角Y, 椭圆右下角X, 椭圆右下角Y), fill=Logo前景色)

# 粘贴Logo
粘贴X坐标 = 二维码图片宽度 // 2 - Logo宽度 // 2
粘贴Y坐标 = 二维码图片高度 // 2 - Logo高度 // 2
img.paste(logo, (粘贴X坐标, 粘贴Y坐标))

# 保存图片
img.save(输出文件名)
print(f"生成成功:{输出文件名}")
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(name, template_folder=resource_path('web'))

pyinstaller --windowed --add-data "web;web" app.py
参数解释：
● web;web：前面的 web 是你电脑里原来的文件夹名，后面的 web 是打包后 对应本地系统软件 里对应的文件夹名（Mac/Linux 用户把分号 ; 改成冒号 :）
● --windowed：不显示黑框（适合桌面软件）

对于无前端，纯python命令行工具，可以使用-F打包成单文件
import io

# 1. 创建
sio = StringIO('初始内容')      # 文本模式
bio = BytesIO(b'initial')       # 二进制模式

# 2. 写入
sio.write('文本')               # 写入字符串
bio.write(b'bytes')             # 写入字节

# 3. 读取
sio.seek(0)                     # 指针移到开头
content = sio.read()            # 读取全部
line = sio.readline()           # 读取一行
lines = sio.readlines()         # 读取所有行

# 4. 指针操作
pos = sio.tell()                # 查看当前指针位置
sio.seek(5)                     # 将指针移动到第5个位置
sio.seek(0, 2)                  # 将指针移动到末尾（用于追加）

# 5. 获取内容（不移动指针）
value = sio.getvalue()          # 直接获取当前所有内容

# 6. 关闭
sio.close()                     # 释放内存
import poplib

# 输入邮件地址, 口令和POP3服务器地址:
email = input('Email: ')
password = input('Password: ')
pop3_server = input('POP3 server: ')

# 连接到POP3服务器:
server = poplib.POP3(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))

# 身份认证:
server.user(email)
server.pass_(password)

# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)

# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = server.retr(index)

# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)

# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
    
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
import argparse

def main():
    # 定义一个ArgumentParser实例:
    parser = argparse.ArgumentParser(
        prog='backup', # 程序名
        description='Backup MySQL database.', # 描述
        epilog='Copyright(r), 2023' # 说明信息
    )
    # 定义位置参数:
    parser.add_argument('outfile')
    # 定义关键字参数:
    parser.add_argument('--host', default='localhost')
    # 此参数必须为int类型:
    parser.add_argument('--port', default='3306', type=int)
    # 允许用户输入简写的-u:
    parser.add_argument('-u', '--user', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('--database', required=True)
    # gz参数不跟参数值，因此指定action='store_true'，意思是出现-gz表示True:
    parser.add_argument('-gz', '--gzcompress', action='store_true', required=False, help='Compress backup files by gz.')


    # 解析参数:
    args = parser.parse_args()

    # 打印参数:
    print('parsed args:')
    print(f'outfile = {args.outfile}')
    print(f'host = {args.host}')
    print(f'port = {args.port}')
    print(f'user = {args.user}')
    print(f'password = {args.password}')
    print(f'database = {args.database}')
    print(f'gzcompress = {args.gzcompress}')

if __name__ == '__main__':
    main()

import pickle

# 保存对象
# 假设有一个复杂的对象（比如一个包含嵌套字典和自定义类的实例）
data = {
    'name': 'Alice',
    'scores': [90, 85, 88],
    'info': {'age': 25, 'active': True}
}

# 1. 打开文件，注意必须是 'wb' (write binary) 模式！
with open('data.pkl', 'wb') as f:
    # 2. .dump(要保存的对象, 文件句柄)
    pickle.dump(data, f)

print("保存成功！现在硬盘里有个 data.pkl 文件")

# 读取对象
# 1. 打开文件，注意必须是 'rb' (read binary) 模式！
with open('data.pkl', 'rb') as f:
    # 2. .load(文件句柄) -> 返回原来的对象
    loaded_data = pickle.load(f)

print(loaded_data)
# 输出: {'name': 'Alice', 'scores': [90, 85, 88], 'info': {'age': 25, 'active': True}}
print(type(loaded_data)) 
# 输出: <class 'dict'> (完美还原类型)

# 进阶使用
data = {'key': 'value'}

# 序列化到内存 (返回 bytes 字节串)
binary_string = pickle.dumps(data) 
print(f"二进制长度: {len(binary_string)}")

# 反序列化回对象
restored = pickle.loads(binary_string)
print(restored)
import numpy as np

# 1. 从列表创建
arr = np.array([1, 2, 3, 4, 5]) 

# 2. 生成连续数字 (类似 range，但返回数组)
# np.arange( start, stop, step )
a = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# 3. 生成全 0 或 全 1 数组 (常用于初始化权重或掩码)
zeros = np.zeros((3, 3)) # 3行3列的 0
ones = np.ones((2, 4))   # 2行4列的 1

# 4. 生成随机数 (模拟数据必用)
rand_arr = np.random.rand(3, 3)       # 0~1 之间的均匀分布
rand_norm = np.random.randn(3, 3)     # 标准正态分布 (均值0, 方差1)
rand_int = np.random.randint(0, 10, size=5) # 0~9 之间的5个随机整数

# 5. 特殊矩阵
eye = np.eye(3) # 3x3 单位矩阵 (对角线为1)

arr = np.arange(12) # [0, 1, ..., 11]

# 查看属性
print(arr.shape)    # (12,) -> 一维，长度12
print(arr.ndim)     # 1 -> 维度数
print(arr.dtype)    # int64 -> 数据类型

# 改变形状 (元素总数必须一致！)
# 把 12 个元素变成 3行4列
matrix = arr.reshape(3, 4) 
print(matrix)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 自动计算维度 (用 -1)
# 不知道行数是多少，但确定要4列，NumPy 会自动算出行数是3
auto_matrix = arr.reshape(-1, 4) 

data = np.arange(20).reshape(4, 5)
# [[ 0,  1,  2,  3,  4],
#  [ 5,  6,  7,  8,  9],
#  [10, 11, 12, 13, 14],
#  [15, 16, 17, 18, 19]]

# 1. 基础切片 [行, 列]
print(data[1, 2])    # 取第2行第3列的元素 -> 7
print(data[0:2, 1:3])# 取前2行，第2-3列 -> [[1, 2], [6, 7]]
print(data[:, 0])    # 取所有行的第1列 -> [0, 5, 10, 15]

# 2. 布尔索引 (筛选神器！)
# 找出所有大于 10 的元素
mask = data > 10     
print(data[mask])    # [11, 12, 13, 14, 15, 16, 17, 18, 19]

# 3. 花式索引 (按指定顺序取)
print(data[[0, 2], [1, 3]]) # 取 (0,1) 和 (2,3) 两个点 -> [1, 13]

arr = np.array([[1, 2, 3], 
                [4, 5, 6]]) # shape (2, 3)

# 场景：给每行都加上 10
result = arr + 10 
# 10 会被“广播”成 (2, 3) 的全 10 矩阵
# [[11, 12, 13], 
#  [14, 15, 16]]

# 场景：每行乘以不同的系数
multiplier = np.array([1, 2]) # shape (2,)
# multiplier 会被广播成 [[1, 1, 1], [2, 2, 2]]
result2 = arr * multiplier
# [[ 1*1, 2*1, 3*1], 
#  [4*2, 5*2, 6*2]] 
# -> [[1, 2, 3], [8, 10, 12]]

data = np.array([[1, 2, 3], 
                 [4, 5, 6]])

print(np.sum(data))        # 总和: 21
print(np.mean(data))       # 平均值: 3.5
print(np.max(data))        # 最大值: 6
print(np.min(data))        # 最小值: 1
print(np.std(data))        # 标准差

# axis 参数是关键！
# axis=0 -> 跨行计算 (按列统计)
print(np.sum(data, axis=0)) # [5, 7, 9] (1+4, 2+5, 3+6)

# axis=1 -> 跨列计算 (按行统计)
print(np.sum(data, axis=1)) # [6, 15] (1+2+3, 4+5+6)

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法 (注意不是 A * B，那是元素对应相乘)
dot_product = np.dot(A, B) 
# 或者使用 @ 符号 (推荐)
result = A @ B 

# 转置
T = A.T 

# 逆矩阵
inv_A = np.linalg.inv(A)
import asyncio
import time

# 1. 定义协程
async def say_hello(delay, name):
    print(f"开始: {name}")
    # 2. 模拟 IO 操作 (不能用 time.sleep，必须用 asyncio.sleep)
    await asyncio.sleep(delay) 
    print(f"结束: {name}")

# 3. 入口点
async def main():
    # 顺序执行 (耗时 1+1=2秒)
    # await say_hello(1, "A")
    # await say_hello(1, "B")
    
    # 并发执行 (耗时 1秒) -> 见下文 create_task
    pass

# 启动
asyncio.run(main())


async def work(id, delay):
    await asyncio.sleep(delay)
    return f"任务 {id} 完成"

async def main():
    # 创建任务 (立即开始运行，但不等待结果)
    task1 = asyncio.create_task(work(1, 2))
    task2 = asyncio.create_task(work(2, 1))
    task3 = asyncio.create_task(work(3, 1.5))

    # 等待所有任务完成
    # gather 可以一次性等待多个任务，并返回结果列表
    results = await asyncio.gather(task1, task2, task3)
    
    print(results) 
    # 输出: ['任务 1 完成', '任务 2 完成', '任务 3 完成']
    # 总耗时约 2 秒 (取决于最慢的那个)，而不是 2+1+1.5=4.5 秒

asyncio.run(main())


async def slow_operation():
    await asyncio.sleep(5)
    return "完成了"

async def main():
    try:
        # 最多等 2 秒，超过就报错
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时了！")

asyncio.run(main())


balance = 0
lock = asyncio.Lock() # 异步锁

async def deposit(amount):
    global balance
    # 获取锁
    async with lock: 
        temp = balance
        await asyncio.sleep(0.1) # 模拟 IO，此时如果没有锁，其他任务会介入修改 temp
        balance = temp + amount
        print(f"存入 {amount}, 余额: {balance}")
    # 自动释放锁

async def main():
    tasks = [deposit(100) for _ in range(5)]
    await asyncio.gather(*tasks)
    print(f"最终余额: {balance}") # 应该是 500，没有锁可能是错误的

asyncio.run(main())
# 设置具体时间点（2024-12-31 23:59:59）
expires_time = datetime(2024, 12, 31, 23, 59, 59)


