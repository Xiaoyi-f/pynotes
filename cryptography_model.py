from cryptography.fernet import Fernet
from dotenv import load_dotenv

# 一定放环境变量
import os

# 加载.env文件（项目启动时执行一次）
load_dotenv()

# 然后统一从这里取配置
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),  # 第二个参数是默认值
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),  # 从.env读取
}
# 加密配置/Token（简单粗暴）
# .gitignore 里要加 .env
# os.environ 只管系统变量，.env 需要 python-dotenv 手动加载
key = os.environ.get("FERNET_KEY").encode()  # .env文件里


# 生成密钥（钥匙）
key = Fernet.generate_key()  # 生成一把钥匙
print(key)  # b'一串随机字符'（要保存好！）

# 把钥匙保存到文件（第一次运行时做）
with open("secret.key", "wb") as f:
    f.write(key)

# 从文件读取钥匙
with open("secret.key", "rb") as f:
    key = f.read()  # 拿到之前保存的钥匙

# 创建密码器
cipher = Fernet(key)

# 加密数据
data = b"银行卡号: 6222 1234 5678 9012"  # 要保护的数据
encrypted = cipher.encrypt(data)  # 加密！
print(f"加密后: {encrypted}")  # 乱码，看不懂

# 解密数据
decrypted = cipher.decrypt(encrypted)  # 解密！
print(f"解密后: {decrypted}")  # 变回原数据
