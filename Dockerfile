# Dockerfile示例
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

