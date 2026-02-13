"""
py -m http.server 端口号
"""

from http.client import HTTPConnection
from http.server import HTTPServer, BaseHTTPRequestHandler

# 客户端常用：
"""
HTTPConnection(host)        # 创建连接
conn.request(method, url)    # 发送请求
conn.getresponse()           # 获取响应
response.read()              # 读取数据
response.status              # 状态码
"""

# 服务器常用：
"""
HTTPServer((host, port), Handler)  # 创建服务器
server.serve_forever()              # 启动服务

# Handler中要重写的方法：
do_GET()     # 处理GET
do_POST()    # 处理POST
send_response()  # 发送状态码
send_header()    # 发送头信息
end_headers()    # 结束头信息
wfile.write()    # 写入响应内容
"""
