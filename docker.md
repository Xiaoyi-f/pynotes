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




