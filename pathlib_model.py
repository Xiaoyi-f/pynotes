from pathlib import Path

# 1. 读文件
content = Path("file.txt").read_text()

# 2. 写文件
Path("out.txt").write_text("hello")

# 3. 拼接路径
config = Path.home() / ".config" / "app.ini"

# 4. 遍历文件
for py in Path(".").rglob("*.py"):
    print(py.name)

# 5. 创建目录
Path("a/b/c").mkdir(parents=True, exist_ok=True)
