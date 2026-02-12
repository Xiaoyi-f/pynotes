import sys

# 1. 获取命令行参数（写脚本必用）
if len(sys.argv) > 1:
    filename = sys.argv[1]

# 2. 退出程序
sys.exit(1)  # 出错退出
sys.exit(0)  # 正常退出

# 3. 添加模块搜索路径（解决导入问题）
sys.path.append("/my/module/path")
