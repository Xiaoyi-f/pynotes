# Python HTTP 服务器项目

## 项目简介

这是一个基于 Python socket 实现的简单 HTTP 服务器项目，用于处理静态资源和动态资源的请求。服务器支持多线程并发处理客户端连接，提供基本的 Web 服务功能。

## 功能特点

- **静态资源处理**：支持 CSS、JavaScript、图片等静态文件的访问
- **动态资源处理**：支持 HTML 文件的动态生成，通过 `dynamic.frame.application()` 函数处理
- **多线程并发**：使用线程池处理多个客户端请求，提高并发性能
- **HTTP 协议支持**：实现了基本的 HTTP/1.1 协议响应
- **错误处理**：对于不存在的资源返回 404 错误

## 项目结构

```
webframe/
├── webserver.py         # 主服务器文件，包含 HTTP 服务器实现
├── dynamic/             # 动态资源处理目录
│   └── frame.py         # 动态资源处理模块，实现 WSGI 接口
├── static/              # 静态资源目录
│   ├── css/             # CSS 文件
│   ├── js/              # JavaScript 文件
│   ├── images/          # 图片文件
│   ├── fonts/           # 字体文件
│   └── index.html       # 默认首页
├── template/            # 模板文件目录
│   ├── index.html       # 模板文件
│   └── center.html      # 模板文件
└── .venv/               # 虚拟环境目录（可选）
```

## 安装与运行

### 前提条件

- Python 3.7+ 环境

### 运行步骤

1. **进入项目目录**

   ```powershell
   cd e:\webframe
   ```

2. **（可选）激活虚拟环境**

   如果项目使用了虚拟环境：

   ```powershell
   .venv\Scripts\activate
   ```

3. **启动服务器**

   ```powershell
   python webserver.py
   ```

4. **访问服务器**

   在浏览器中输入以下地址：

   ```
   http://localhost:8080
   ```

   服务器默认监听 8080 端口，可在 `webserver.py` 文件中修改端口号。

## 技术栈

- **Python 3.7+**：主要开发语言
- **socket 模块**：实现 TCP 服务器功能
- **threading 模块**：实现多线程并发处理
- **WSGI 接口**：用于处理动态资源请求

## 核心模块说明

### webserver.py

主服务器文件，包含 `HttpWebServer` 类，实现了以下功能：

- 创建 TCP 服务器套接字并监听端口
- 接受客户端连接并创建子线程处理请求
- 解析 HTTP 请求报文，获取请求路径
- 根据请求路径分发静态资源或动态资源处理
- 组装 HTTP 响应报文并发送给客户端

### dynamic/frame.py

动态资源处理模块，实现了 `application` 函数，用于处理 HTML 文件的动态生成。该函数遵循 WSGI 接口规范，接收环境变量 `env` 并返回响应体。

## 示例请求

### 访问静态资源

```
http://localhost:8080/css/main.css      # 访问 CSS 文件
http://localhost:8080/js/jquery.min.js   # 访问 JavaScript 文件
http://localhost:8080/images/001.jpg     # 访问图片文件
```

### 访问动态资源

```
http://localhost:8080/index.html         # 访问动态生成的首页
http://localhost:8080/                   # 默认为 index.html
```

## 注意事项

1. 确保 8080 端口未被其他程序占用，否则可能导致启动失败
2. 服务器仅用于开发和学习目的，不建议在生产环境中使用
3. 静态资源目录为 `static/`，所有静态文件需放置在此目录下
4. 动态资源处理逻辑在 `dynamic/frame.py` 中，可根据需要修改

## 扩展建议

- 添加路由系统，支持更多动态资源路径
- 实现模板引擎，简化 HTML 生成
- 添加日志系统，记录请求和错误信息
- 支持 HTTPS 协议
- 优化并发处理，使用线程池或异步 IO

## 许可证

本项目为学习用例，无特定许可证限制。
