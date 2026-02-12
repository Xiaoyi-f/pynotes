# 1. 加密配置/Token（简单粗暴）
from cryptography.fernet import Fernet

# ❌ 错误：写死在代码里
key = b"1a2b3c4d5e6f7g8h9i0j..."  # 提交git就泄露

# ✅ 正确：放环境变量
import os

key = os.environ.get("FERNET_KEY").encode()  # .env文件里

# ✅ 或存配置文件（别提交）
with open("secret.key", "rb") as f:
    key = f.read()
cipher = Fernet(key)
enc = cipher.encrypt(b"data")
dec = cipher.decrypt(enc)

# 2. 存用户密码（别自己写MD5）
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
hash = kdf.derive(b"password")
