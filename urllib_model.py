import urllib.request
import urllib.parse
import json
from urllib.error import URLError, HTTPError

# 1. GET请求（最简单）
response = urllib.request.urlopen("http://httpbin.org/get")
print(response.read().decode())  # 读取返回内容

# 2. GET带参数（自动拼URL）
params = {"name": "张三", "age": 25}
url = "http://httpbin.org/get?" + urllib.parse.urlencode(params)
response = urllib.request.urlopen(url)
data = json.loads(response.read())  # JSON转字典
print(data["args"])  # 打印参数

# 3. POST表单数据
post_data = urllib.parse.urlencode({"user": "admin", "pass": "123"}).encode()
response = urllib.request.urlopen("http://httpbin.org/post", data=post_data)
print(json.loads(response.read()))

# 4. POST JSON数据
json_data = json.dumps({"name": "张三"}).encode()
req = urllib.request.Request(
    "http://httpbin.org/post",
    data=json_data,
    headers={"Content-Type": "application/json"},
    method="POST",
)
response = urllib.request.urlopen(req)
print(json.loads(response.read()))

# 5. 添加请求头（模拟浏览器）
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request("http://httpbin.org/headers", headers=headers)
response = urllib.request.urlopen(req)
print(json.loads(response.read()))

# 6. 异常处理（必加）
try:
    response = urllib.request.urlopen("http://httpbin.org/status/404", timeout=3)
    print(response.read())
except HTTPError as e:
    print(f"HTTP错误: {e.code}")
except URLError as e:
    print(f"连接失败: {e.reason}")


# 7. 下载文件（分块读省内存）
def download(url, save_path):
    response = urllib.request.urlopen(url)
    with open(save_path, "wb") as f:
        while True:
            chunk = response.read(8192)  # 一次8KB
            if not chunk:
                break
            f.write(chunk)
    print(f"下载完成: {save_path}")


# 8. 实战：封装成简单客户端
class HttpClient:
    def __init__(self, base_url=""):
        self.base_url = base_url.rstrip("/")

    def get(self, path, params=None):
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(url)
        return json.loads(response.read())

    def post(self, path, data=None, json_data=None):
        url = f"{self.base_url}{path}"
        if json_data:
            post_data = json.dumps(json_data).encode()
            headers = {"Content-Type": "application/json"}
        else:
            post_data = urllib.parse.urlencode(data or {}).encode()
            headers = {}

        req = urllib.request.Request(
            url, data=post_data, headers=headers, method="POST"
        )
        response = urllib.request.urlopen(req)
        return json.loads(response.read())


# 使用
client = HttpClient("https://httpbin.org")
result = client.get("/get", {"name": "张三"})
print(result["args"])

"""
记住：
urlopen() 发请求
urlencode() 拼参数
Request() 加headers
read().decode() 拿结果
"""
