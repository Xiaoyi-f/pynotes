我们写代码通常由三大环境:
    1.开发环境 -> 开发
    2.测试环境 -> 测试
    3.生产环境 -> 运维
为了避免在不同环境中代码冲突问题，我们可以把项目需要的环境
放到一个容器中，实现软件跨环境迁移 
Docker是一个开源的应用容器引擎->基于Go语言实现
容器是完全使用沙箱机制，相互隔离的
容器性能开销极低
# Docker安装 -> Ubuntu -> 自行搜索就好
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list && sudo apt-get update && sudo apt-get install -y docker-ce && sudo systemctl start docker && sudo systemctl enable docker
docker --version 检查 
# Docker架构 
Docker安装成功启动守护进程
容器和镜像的关系 -> 镜像相当于类，容器相当于实例
通过客户端发送命令给守护进程执行Docker命令
仓库是用来保存镜像文件的,代码仓库
# 国内镜像源:
    1.阿里云
    2.中科大
    3.清华源 
    4.腾讯云 
    5....
# 镜像加速器配置
阿里云控制台中找到容器镜像服务...
# Docker命令 
systemctl start docker 启动
systemctl stop docker 停止
systemctl restart docker 重启
systemctl status docker 查看状态
systemctl enable docker 使开机自启

docker images 查看镜像
docker search <name> 搜索仓库镜像 -> 国内常被限制 
docker pull <name>:<version> 拉取镜像
docker rmi <id> 删除镜像 
docker images -q 查看所有镜像id

# -i让容器一直运行着 -t给容器分配一个伪终端 /bin/bash 进入容器的初始化指令
# -d 后台运行
docker run -i -t -d --name=<name> <name>:<version> 创建/运行容器
docker exec -it <containername> /bin/bash 进入容器
exit 退出容器
docker ps -a 查看所有的容器
docker stop <containername> 停止容器 
docker start <containername> 启动容器
docker rm <containername> 删除容器
docker inspect <containername> 查看容器信息

# Docker数据卷 -> 数据交换/本地保存 
数据卷是宿主机中的一个目录 
当容器目录和数据卷绑定后，对方的修改会立即同步 
一个数据卷可以被多个容器同时挂载 
一个容器也可以被挂载多个数据卷 
docker run ... -v 宿主机目录/文件:容器目录/文件 
注意: 
    目录必须是绝对路径
    如果目录不存在，会自动创建 
    可以挂载多个数据卷
~ 表示/root目录 
容器本身是一个虚拟机，容器目录指的是容器系统的某个目录
建议在root中
    创建一个data目录再创建对应的数据卷存放数据 

# 网络 
容器内容的网络和外部机器不能直接通信 
外部机器和宿主机可以直接通信 
宿主机和容器可以直接通信

# 网络连接
将宿主机的某个端口和容器的某个端口映射 
映射端口可以一样，因为他们不是同一个系统
-p 宿主机端口:容器端口 
使用$PWD占位路径 

# 注意: 提前创建好需要的目录/进入到对应目录操作 

# 部署示例
mysql部署 
    mkdir mysql
    cd mysql 
    docker run -i -d \
        -p 3306:3306 \
        --name=mysql8 \
        -v $PWD/conf:/etc/mysql/conf.d \
        -v $PWD/logs:/logs \
        -v $PWD/data:/var/lib/mysql \
        -e MYSQL_ROOT_PASSWORD=<PASSWORD> \
        mysql:8.0 # 版本声明 
-e是配置环境变量 
conf.d是linux约定熟成的配置文件目录名 
外界访问docker要访问宿主机ip和映射的端口 

nginx部署 
    mkdir nginx
    cd nginx
    docker run -i -d \
        -p 80:80 \ 
        -v $PWD/website:/usr/share/nginx/html \
        -v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf \
        -v $PWD/logs:/var/log/nginx \
        nginx:latest

# Docker镜像原理 
Docker镜像是由特殊的文件系统叠加而成的 
最底端是bootfs，并使用宿主机的bootfs
第二层是root文件系统rootfs，称为 base image 
然后可往上再叠加其他镜像文件，形成依赖链 

# 镜像制作 
1.容器转镜像 
    docker commit 容器id 镜像名称:版本号 
    docker save -o 压缩文件名称 镜像名称:版本号
    docker load -i 压缩文件名称 
    目录挂载的会失连，需要重新挂载
2.dockerfile
    docker build -f DockerfileURL -t 镜像名称:版本号 

# Docker Compose
服务编排: 按照一定规则管理多个容器
1.利用Dockerfile定义环境镜像
2.使用docker-compose.yml定义组成应用的各种服务
3.运行docker-compose up 启动应用
4.运行docker-compose down 停止应用
下载:
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker compose version 检验安装
# docker-compose.yml
# 最简单的模板，只包含最常用的配置
version: '3.8'        # 版本号

services:
  # 后端服务
  backend:
    build: .                    # 用当前目录的 Dockerfile 构建
    container_name: backend     # 容器名称
    ports:
      - "5000:5000"            # 宿主机端口:容器端口
    environment:
      - KEY=VALUE               # 环境变量
    depends_on:
      - database                # 依赖数据库服务
    volumes:
      - ./app:/app              # 挂载代码，方便开发
    restart: always              # 重启策略

  # 数据库
  database:
    image: postgres:13          # 直接用官方镜像
    container_name: database
    environment:
      - POSTGRES_PASSWORD=123456  # 数据库密码
    volumes:
      - db_data:/var/lib/postgresql/data  # 数据持久化
    restart: always

  # 反向代理
  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"    # 对外暴露80端口
    depends_on:
      - backend
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf  # 配置文件
    restart: always

# 数据卷 
volumes:
  db_data:         # 声明数据卷

常用命令:
    # 启动服务（前台）
    docker-compose up
    
    # 后台启动
    docker-compose up -d
    
    # 停止服务
    docker-compose down
    
    # 查看日志
    docker-compose logs -f
    
    # 进入容器
    docker-compose exec backend sh
    
    # 重启服务
    docker-compose restart
    
    # 查看状态
    docker-compose ps

# 私有仓库
# FROM python:<version>
# LABEL maintainer="author" <15779544219@163.com> \
#       version="1.0" \
#       description="desc"

# ENV
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=utf-8
ENV PYTHONFAULTHANDLER=1
ENV PYTHONHASHSEED=1
ENV PYTHONPATH=/project
ENV PYTHONOPTIMIZE=1
ENV PYTHONOPTIMIZE=2
# 1 -> 去掉assert语句和__debug__条件
# 2 -> 在1的基础上，还去掉文档字符串
# WORKDIR /project

# RUN command -> 每行RUN会创建一层级，尽量&&合并命令

# COPY url url
# ADD url url 若是tar会自动解包

# EXPOSE <端口号> 声明会打开的端口

# CMD ["cmd1", "cmd2" ...] 一个Dockerfile只能用一次


