"""
日志级别:
    1.DEBUG 程序调试时候使用
    2.INFO 程序正常运行时候使用
    3.WARNING 程序未按期运行时候使用，但是并不是错误
    4.ERROR 程序出错时候使用
    5.CRITICAL 特别严重的问题，导致程序不能继续运行时候使用
    默认是WARNING等级，当在WARNING或其之上等级时候才会记录日志信息
    上面的日志级别是由低到高的
logging模块记录日志的方式:
    1.输出到控制台
    2.保存到日志文件
"""

import logging

# 日志等级和输出格式配置
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s",
    filename="log.txt",
    filemode="w",
)
# level 设置日志的等级
# format 日志的输出格式
# 日志级别名称
# 当前执行的程序名
# 日志当前行号
# 日志时间
# 日志信息
# 保存到文件
# 文件读写模式设置
logging.debug("This is a debug message")  # 默认不输出
logging.info("This is an info message")  # 默认不输出
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")
