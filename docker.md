📚 第一部分：Docker 到底是个啥？
1.1 Docker 是什么？（一句话说清）
Docker = 轻量级虚拟机 + 软件打包工具 + 一键部署神器

传统部署：安装环境 → 配置环境 → 安装软件 → 调试 → 运行
Docker部署：下载镜像 → 运行容器 → 完成！
1.2 为什么要用 Docker？（三大好处）
# 1. 解决"在我机器上好好的"问题
# 你的机器：Ubuntu + Python 3.8 + Node.js 14
# 别人机器：Windows + Python 3.6 + Node.js 12
# Docker：大家环境完全一致

# 2. 快速部署
传统：安装需要2小时
Docker：5分钟搞定

# 3. 节省资源
虚拟机：每个要分配完整系统资源（几GB内存）
Docker容器：共享主机系统，只需几十MB内存
1.3 三大核心概念（必须理解）
1. 镜像 (Image)     - 软件安装包
   📦 类比：Windows系统的.iso安装文件

2. 容器 (Container) - 运行中的软件
   🖥️ 类比：安装好的Windows系统（正在运行）

3. 仓库 (Registry) - 软件商店
   🛒 类比：应用商店（Docker Hub）

🎯 第二部分：零基础安装和验证
2.1 安装 Docker（各平台）
# 1. Windows/Mac：下载 Docker Desktop
# 访问：https://www.docker.com/products/docker-desktop
# 双击安装，一直下一步就行

# 2. Linux（Ubuntu为例）
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker && sudo systemctl enable docker
# enable设置开机自启
2.2 验证安装（必做的三件事）
# 1. 检查版本
docker --version
# ✅ 看到类似：Docker version 20.10.17 就成功了

# 2. 运行测试容器（最重要的测试！）
docker run hello-world
# ✅ 看到 "Hello from Docker!" 就是成功
# 📝 解释：这个命令会自动下载hello-world镜像并运行

# 3. 查看系统信息
docker info
# ✅ 显示Docker详细信息，证明安装正常

📦 第三部分：镜像（Image）操作 - 软件包管理
3.1 镜像是什么？
镜像 = 只读模板（包含应用+环境）
类比：.exe安装程序 + 运行需要的所有库
3.2 镜像基础操作（掌握这5个就够了）
# 🔥 1. 搜索镜像（找软件）
docker search nginx
# 📊 结果：会列出所有nginx相关的镜像
# ⭐ 带OFFICIAL的是官方镜像，最可靠

# 🔥 2. 下载镜像（下软件）
docker pull nginx
# 💡 技巧：不写版本默认下载最新版
# 🎯 生产环境一定要指定版本！
docker pull nginx:1.23-alpine  # 下载指定版本

# 🔥 3. 查看本地镜像（看你下了哪些）
docker images
# 📊 输出：镜像名、标签、ID、创建时间、大小
# 💡 常用参数：
docker images -a      # 显示所有（包括中间层）
docker images | grep nginx  # 只显示nginx相关

# 🔥 4. 删除镜像（删软件）
docker rmi nginx
# ⚠️ 注意：如果镜像正在被容器使用，需要先删容器
# ✅ 安全删除：先停止容器，再删镜像

# 🔥 5. 镜像打标签（重命名/标记）
docker tag nginx mynginx:v1
# 📝 解释：给nginx镜像起个别名叫mynginx:v1
# 🎯 用途：推送到自己仓库时用
3.3 镜像标签是什么？
nginx:latest      ← 默认标签，最新版（不推荐用）
nginx:1.23        ← 指定版本（推荐）
nginx:1.23-alpine ← 版本+变体（alpine是精简版）
myapp:v1.0        ← 自定义标签

🐳 第四部分：容器（Container）操作 - 运行软件
4.1 容器是什么？
容器 = 镜像的运行实例
类比：安装好的软件（正在运行）

关键特性：
1. 轻量级：启动只要几秒
2. 隔离性：每个容器相互独立
3. 可移植：在哪都能运行
4.2 容器生命周期（掌握这8个命令）
# 🔥 1. 创建并运行容器（最常用！）
docker run nginx
# ⚠️ 问题：这样会占用终端，按Ctrl+C停止

# 🔥 正确用法（加-d参数后台运行）
docker run -d nginx
# ✅ 容器在后台运行，返回容器ID

# 🔥 带名字运行（方便管理）
docker run -d --name mynginx nginx

# 🔥 2. 查看运行中的容器
docker ps
# 📊 显示：容器ID、镜像、命令、状态、端口等

docker ps -a
# 📊 查看所有容器（包括已停止的）

# 🔥 3. 停止容器
docker stop mynginx
# 或者用容器ID
docker stop 容器ID前几位

# 🔥 4. 启动已停止的容器
docker start mynginx

# 🔥 5. 重启容器
docker restart mynginx

# 🔥 6. 删除容器
docker rm mynginx
# ⚠️ 注意：只能删除已停止的容器
docker rm -f mynginx  # 强制删除运行中的容器

# 🔥 7. 进入容器内部（调试用）
docker exec -it mynginx bash
# 📝 解释：
# -it：交互式终端
# bash：进入后使用bash shell

# 🔥 8. 查看容器日志
docker logs mynginx
docker logs -f mynginx    # 实时查看（跟踪日志）
docker logs --tail 100 mynginx  # 只看最后100行
4.3 容器常用参数详解
# 端口映射（最重要！）
docker run -d -p 8080:80 --name web nginx
# 📝 解释：
# -p 8080:80 = 主机8080端口 → 容器80端口
# 访问：http://localhost:8080

# 挂载目录（数据持久化）
docker run -d -v /宿主机路径:/容器路径 nginx
# 📝 例子：
docker run -d -v /home/html:/usr/share/nginx/html nginx
# 🎯 效果：修改主机/home/html，容器里立即生效

# 环境变量
docker run -d -e MYSQL_ROOT_PASSWORD=123456 mysql
# 📝 解释：设置容器的环境变量

# 资源限制
docker run -d --memory=512m --cpus=1 nginx
# 📝 解释：限制容器最多用512MB内存，1个CPU核心

🌐 第五部分：网络和存储 - 让容器真正可用
5.1 端口映射（让外部能访问）
# 基础映射
docker run -d -p 80:80 nginx
# 访问：http://localhost

# 指定IP映射
docker run -d -p 127.0.0.1:8080:80 nginx
# 只能本机访问

# 随机端口
docker run -d -P nginx
# 系统自动分配端口，用 docker ps 查看
5.2 数据卷（保存重要数据）
# 为什么需要数据卷？
# 容器删除 → 数据丢失 ❌
# 使用数据卷 → 数据持久化 ✅

# 1. 创建数据卷
docker volume create mydata

# 2. 使用数据卷
docker run -d -v mydata:/app/data nginx

# 3. 查看数据卷
docker volume ls

# 4. 删除数据卷
docker volume rm mydata
5.3 目录挂载（更常用的方式）
# 挂载主机目录到容器
docker run -d -v /宿主机/绝对路径:/容器路径 nginx

# 例子：挂载网站目录
docker run -d \
  -p 80:80 \
  -v /home/www:/usr/share/nginx/html \
  --name mywebsite \
  nginx
  
# 现在，在/home/www放index.html就能访问了！

🚀 第六部分：Dockerfile - 制作自己的镜像
6.1 Dockerfile 是什么？
Dockerfile = 镜像制作说明书
记录了：用什么基础镜像 + 安装什么 + 配置什么 + 运行什么
6.2 最简单的 Dockerfile
# 1. 基于哪个镜像（必须）
FROM nginx:alpine

# 2. 复制文件到镜像
COPY index.html /usr/share/nginx/html/

# 3. 暴露端口（文档作用）
EXPOSE 80

# 4. 启动命令
CMD ["nginx", "-g", "daemon off;"]
6.3 构建自己的镜像
# 1. 创建目录和文件
mkdir myapp && cd myapp
echo "<h1>Hello Docker!</h1>" > index.html

# 2. 创建 Dockerfile（内容如上）

# 3. 构建镜像
docker build -t mynginx:v1 .
# 📝 解释：
# -t mynginx:v1 = 给镜像起名字
# . = 在当前目录找Dockerfile

# 4. 运行自己的镜像
docker run -d -p 8080:80 mynginx:v1
# 访问：http://localhost:8080
6.4 Dockerfile 常用指令
FROM ubuntu:20.04           # 基础镜像
WORKDIR /app               # 设置工作目录
COPY . /app                # 复制文件
RUN apt-get update && apt-get install -y python3  # 执行命令
ENV PORT=8080              # 设置环境变量
EXPOSE 8080                # 声明端口
CMD ["python3", "app.py"]  # 容器启动命令

🛠️ 第七部分：Docker Compose - 管理多个容器
7.1 为什么需要 Compose？
# 一个应用需要：Web服务器 + 数据库 + 缓存
# 传统方式：分别启动3个容器，麻烦！
# Compose方式：一个命令启动所有！
7.2 docker-compose.yml 文件
version: '3.8'
services:
  web:                    # 服务1：Web服务
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:                     # 服务2：数据库
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: 123456
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:                # 定义数据卷
7.3 Compose 常用命令
# 安装（Linux）
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 核心命令
docker-compose up -d      # 启动所有服务（后台）
docker-compose down       # 停止并删除所有
docker-compose ps         # 查看服务状态
docker-compose logs       # 查看所有日志
docker-compose logs web   # 只看web服务日志
docker-compose exec db bash  # 进入db容器
docker-compose restart web   # 重启web服务

📝 第八部分：实战项目 - 从零搭建网站
项目：WordPress 博客系统
# 1. 创建项目目录
mkdir wordpress && cd wordpress

# 2. 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress123

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - "8000:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress123
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_data:/var/www/html

volumes:
  db_data:
  wp_data:
EOF

# 3. 一键启动
docker-compose up -d

# 4. 访问网站
# 浏览器打开：http://localhost:8000
# 按照WordPress引导完成安装

# 5. 停止服务
docker-compose down
# 加-v参数会删除数据卷（数据会丢失！）
docker-compose down -v

🎯 第九部分：命令速查表（打印贴在墙上）
镜像操作
docker pull 镜像名         # 下载镜像
docker images            # 查看镜像
docker rmi 镜像名         # 删除镜像
docker search 关键词      # 搜索镜像
docker tag 旧名 新名      # 重命名镜像
容器操作
docker run -d -p 主机:容器 镜像名   # 运行容器
docker ps                    # 查看运行中容器
docker ps -a                 # 查看所有容器
docker stop 容器名           # 停止容器
docker start 容器名          # 启动容器
docker restart 容器名        # 重启容器
docker rm 容器名             # 删除容器
docker exec -it 容器名 bash  # 进入容器
docker logs 容器名           # 查看日志
网络和存储
docker network ls           # 查看网络
docker volume ls           # 查看数据卷
docker volume create 卷名   # 创建数据卷
docker volume rm 卷名       # 删除数据卷
Docker Compose
docker-compose up -d       # 启动所有服务
docker-compose down        # 停止所有服务
docker-compose ps          # 查看服务状态
docker-compose logs        # 查看日志
docker-compose exec 服务名 bash  # 进入服务容器
系统管理
docker info               # 系统信息
docker system df          # 磁盘使用
docker system prune -a    # 清理所有无用资源（慎用！）

🚨 第十部分：常见问题解决
问题1：端口被占用
# 错误：Bind for 0.0.0.0:80 failed: port is already allocated

# 解决方法1：换端口
docker run -d -p 8080:80 nginx

# 解决方法2：停止占用端口的进程
netstat -tlnp | grep :80   # 查看谁在用80端口
kill -9 进程ID              # 停止该进程
问题2：容器无法启动
# 查看错误日志
docker logs 容器名

# 常见原因：
# 1. 端口冲突
# 2. 目录挂载错误
# 3. 环境变量缺失
问题3：磁盘空间不足
# 查看Docker磁盘使用
docker system df

# 清理无用资源
docker system prune      # 安全清理
docker system prune -a   # 彻底清理（会删未用镜像）
问题4：镜像下载慢
# 修改为国内镜像源
# 创建或编辑 /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}

# 重启Docker
sudo systemctl restart docker

🏁 学习路线建议
第1周：新手阶段
✅ 安装Docker
✅ 运行 hello-world
✅ 学会：docker pull, docker run, docker ps
✅ 部署一个nginx网站
第2周：进阶阶段
✅ 学会目录挂载 (-v)
✅ 学会端口映射 (-p)
✅ 制作简单Dockerfile
✅ 使用docker-compose管理多容器
第3周：实战阶段
✅ 部署WordPress/Mysql
✅ 部署自己的Web应用
✅ 理解数据持久化
✅ 学会排查常见问题
第4周：生产环境
✅ 镜像版本管理
✅ 资源限制配置
✅ 日志管理
✅ 备份和恢复

💡 一句话技巧
1. 镜像是模板，容器是实例
2. -d 参数让容器后台运行
3. -p 参数映射端口才能访问
4. -v 参数挂载目录持久化数据
5. docker-compose 是管理多容器的神器
6. 生产环境一定要指定镜像版本
7. 定期清理无用资源防止磁盘满

🎓 毕业项目
自己动手完成这个项目，你就从Docker小白毕业了：
项目：搭建个人博客系统
要求：
1. 使用WordPress + MySQL
2. 网站数据要持久化（容器删除数据不丢）
3. 通过80端口访问
4. 能进入MySQL容器备份数据
5. 能通过docker-compose一键启动/关闭
