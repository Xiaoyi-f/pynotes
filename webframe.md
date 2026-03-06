预备知识
Python Web 核心协议：WSGI 与 ASGI
在 Python Web 开发的学习路径中，理解服务器与应用之间的通信机制至关重要。WSGI 和 ASGI 正是定义这种通信标准的两大接口协议。前者是奠定基础的“经典”，后者则是支持实时交互的“未来”。

WSGI：同步通信的基石
WSGI（Web Server Gateway Interface）是 Python 为 Web 服务器与 Web 应用之间制定的标准接口。它使得开发者编写的代码可以兼容多种服务器（如 Gunicorn、uWSGI），而无需关心底层网络细节。
● 核心工作模式
WSGI 采用同步阻塞的模式。它就像一次传统的“点餐-上菜”流程：客户端发送请求（点餐），服务器调用应用处理（厨房做菜），应用处理完毕后返回响应（上菜），连接随即断开。这一过程是“一问一答”式的，服务器在处理一个请求时，无法响应其他请求。
● 代码结构特征
一个典型的 WSGI 应用是一个可调用对象（通常是函数），它接收 environ（包含请求信息的字典）和 start_response（用于设置响应状态和头部的回调函数）两个参数。
def application(environ, start_response):
    status = '200 OK'
    headers = 
    start_response(status, headers)
    return [b'Hello, WSGI!']
● 适用场景与局限
WSGI 非常适合传统的、以请求-响应为主的 Web 应用，如博客系统、内容管理后台等。其主要局限在于无法有效处理长连接和实时通信场景，且在面对大量 I/O 阻塞操作时，并发性能受限。

ASGI：异步与实时的未来
ASGI（Asynchronous Server Gateway Interface）是为了解决 WSGI 的局限性而诞生的，旨在支持异步处理和多种网络协议。它是现代 Python 异步框架（如 FastAPI、Starlette）的基石。
● 核心工作模式
ASGI 采用异步非阻塞的模式。它更像是一场“视频通话”：连接建立后可以长时间保持，服务器和客户端可以随时主动向对方发送数据。这种模式不仅支持传统的 HTTP，还原生支持 WebSocket、HTTP/2 以及服务器发送事件（SSE）。
● 代码结构特征
一个 ASGI 应用是一个异步可调用对象，它接收 scope、receive 和 send 三个参数。scope 包含连接的元数据，receive 和 send 则是用于收发消息的异步通道。
async def application(scope, receive, send):
    if scope['type'] == 'http':
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, ASGI!',
        })
● 核心优势
  ○ 高性能并发：基于 async/await 语法，应用在等待数据库查询或文件读写等 I/O 操作时，可以挂起并去处理其他请求，极大提升了单线程的并发处理能力。
  ○ 原生支持长连接：无需复杂的轮询或适配器，即可直接构建聊天室、实时通知、在线游戏等需要服务器主动推送数据的应用。

协议对比与选型指南
维度	WSGI	ASGI
通信模式	同步阻塞	异步非阻塞
核心语法	def 函数	async def 协程
协议支持	仅 HTTP/1.x	HTTP/1.x, HTTP/2, WebSocket 等
典型框架	Django (< 3.0), Flask(原生不支持ASGI -> 混合架构/中间件处理...)	FastAPI,  Django (>= 3.0)
适用场景	传统网站、同步业务逻辑	实时应用、高并发 I/O 密集型服务
总结：
● WSGI 是 Python Web 的“基石”，生态成熟稳定，适合绝大多数传统的同步 Web 开发。
● ASGI 是面向未来的“引擎”，它解决了实时通信和高并发的痛点，是构建现代交互式 Web 应用的首选。随着异步生态的成熟，ASGI 正在逐步成为新的标准。
原生 Python 手写 Web 框架思路
项目核心：五大模块拆解
为了便于理解，可将框架构建过程比作经营一家餐厅，通过这一类比理解各模块的作用及必要性。
1. 地基：WSGI 协议（标准点菜单）
● 小白讲解：想象 Web 框架是一家餐厅，浏览器是顾客，Web 服务器是送餐员，Python 代码是厨师。WSGI 协议就是那张标准的“点菜单”。
● 要用的东西：一个符合 WSGI 规范的函数 def application(environ, start_response):。
● 为什么要有它：它是 Python Web 开发的生命线。没有它，Python 代码无法接收浏览器的请求，也无法将处理结果返回给服务器，导致“厨师”不知道“顾客”点了什么。
2. 指挥中心：框架主类（大堂经理）
● 小白讲解：这是餐厅的“大堂经理”，负责统一管理所有业务。
● 要用的东西：一个类 class SimpleFramework: 和一个存储路由的列表 self.routes = []。
● 为什么要有它：需要一个中心化的地方来记录所有网址（路由）与处理函数（视图）的对应关系。例如，当用户访问 / 时，大堂经理负责指派对应的处理逻辑。
3. 导航系统：路由系统（指示牌）
● 小白讲解：这是餐厅的“指示牌”，负责引导顾客去往正确的包厢。
● 要用的东西：装饰器 @app.route() 和正则表达式 import re。
● 为什么要有它：互联网应用不仅有静态路径（如 /about），还有动态路径（如 /user/123）。路由系统能智能解析 URL，提取动态参数（如用户 ID），并将请求精准分发，避免为每个用户写死一个路径。
● 路由注册：将特定的 URL 路径模式（URL Pattern）与具体的处理逻辑（Handler/Controller/View Function）进行绑定的过程
4. 点单处理：请求封装（备忘录）
● 小白讲解：顾客递来的原始“点菜单”（请求）格式混乱，大堂经理需要将其整理成一张清晰的“备忘录”交给厨师。
● 要用的东西：urllib.parse（拆解 URL 参数）和 json 模块（处理 JSON 数据）。
● 为什么要有它：原生的 environ 对象数据结构复杂且难以阅读。通过封装 Request 类，开发者可以使用 request.args['name'] 这样简洁的方式获取数据，极大提升开发效率和代码可读性。
5. 上菜环节：响应处理（装盘）
● 小白讲解：菜做好后不能把锅扔给顾客，需要“装盘”并贴上状态标签（如“200 好菜”或“404 找不到”）。
● 要用的东西：字节码转换 .encode('utf-8')。
● 为什么要有它：网络传输只认字节流。正确的响应处理能确保浏览器正确显示中文、识别文件类型或执行跳转，是保证用户体验的基础。
️ 动手实操：项目清单
在开始编码前，请准备好以下“积木原料”：
模块分类	具体组件	用途说明
导入库	from typing import Callable	用于代码注释，标明变量类型为函数
from urllib.parse import urlparse, parse_qs	解析 URL 中的查询参数	
import re	处理动态路由的正则匹配	
import json	处理 JSON 格式的数据	
核心类	class SimpleFramework:	框架主类，充当大堂经理角色
def __init__(self):	初始化路由存储列表	
def route(self, path):	装饰器，用于注册路由	
def __call__(self, environ, start_response):	WSGI 入口，启动请求分发	
请求类	class Request:	封装请求数据，提供便捷访问属性
服务器	from wsgiref.simple_server import make_server	启动本地开发服务器，用于测试
设计哲学：为什么这样写？
● 高内聚低耦合(软件设计的黄金法则)：将请求封装成 Request 类，是为了让处理逻辑与业务逻辑分离。这就像大堂经理负责接单，厨师负责做菜，职责分明，便于后期维护和修改。
● 正则的力量：计算机思维是死板的。利用正则表达式将 /user/<id> 转换为通用规则，能以不变应万变，高效处理海量动态请求。
● WSGI 的标准性：使用 wsgiref 是为了在开发阶段提供一个简易的测试服务器。这种设计遵循标准，意味着将来项目上线时，可以无缝切换到 Gunicorn 等专业服务器，而无需修改核心业务代码。
TIP：
耦合是指不同模块之间相互依赖程度的度量
内聚是指单个模块内部各个元素（函数、数据、逻辑）彼此结合的紧密程度的度量
建议
不要试图一口吃成胖子。建议按照以下迭代步骤进行：
1. 先跑通：先不写类，直接写一个最简单的 WSGI 函数，确保能在浏览器中显示 "Hello World"。
2. 加路由：引入类和路由列表，尝试实现一个简单的路径匹配。
3. 做封装：逐步加入 Request 封装和动态路由解析。

