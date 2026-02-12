import hashlib
import os


# ============ 1. 普通哈希（文件/缓存去重） ============
def normal_hash():
    """SHA-256：文件完整性、重复数据判断"""
    # 字符串哈希
    data = "hello world"
    hash1 = hashlib.sha256(data.encode()).hexdigest()
    # b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9

    # 文件哈希（大文件分块读）
    hash2 = hashlib.sha256()
    with open("file.txt", "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash2.update(chunk)
    return hash2.hexdigest()


# ============ 2. 用户密码（必用PBKDF2！） ============
def password_hash():
    """PBKDF2：加盐+慢哈希，防彩虹表防暴力破解"""
    password = "user123456"

    # 2.1 生成随机盐（每个用户不同）
    salt = os.urandom(16)  # 16字节盐

    # 2.2 计算哈希
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256",  # 哈希算法
        password.encode(),  # 密码转bytes
        salt,  # 盐
        100000,  # 迭代次数（越大越安全，越慢）
        dklen=32,  # 输出长度
    )

    # 转十六进制存数据库
    salt_hex = salt.hex()
    hash_hex = hash_bytes.hex()

    # 2.3 验证密码
    def verify(input_pwd, stored_salt_hex, stored_hash_hex):
        salt = bytes.fromhex(stored_salt_hex)
        test_hash = hashlib.pbkdf2_hmac(
            "sha256", input_pwd.encode(), salt, 100000
        ).hex()
        return test_hash == stored_hash_hex

    return salt_hex, hash_hex, verify


# ============ 实战：用户系统 ============
class UserPassword:
    """密码处理完整实现"""

    @staticmethod
    def make(password: str, iterations: int = 100000) -> dict:
        """注册：生成密码哈希"""
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
        return {
            "salt": salt.hex(),
            "hash": key.hex(),
            "iterations": iterations,  # 留个字段，以后可以升级
        }

    @staticmethod
    def check(
        password: str, salt_hex: str, hash_hex: str, iterations: int = 100000
    ) -> bool:
        """登录：验证密码"""
        salt = bytes.fromhex(salt_hex)
        test_key = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, iterations
        ).hex()
        return test_key == hash_hex


# ============ 一句话总结 ============
# 普通去重用 hashlib.sha256()
# 存用户密码用 hashlib.pbkdf2_hmac()  ⚠️ 千万别用md5/sha256直接存！

if __name__ == "__main__":
    # 测试
    pwd = UserPassword()
    result = pwd.make("admin123")
    print(f"盐: {result['salt'][:20]}...")
    print(f"哈希: {result['hash'][:20]}...")

    # 验证
    ok = pwd.check("admin123", result["salt"], result["hash"])
    print(f"验证正确: {ok}")  # True
    ok = pwd.check("admin456", result["salt"], result["hash"])
    print(f"验证错误: {ok}")  # False
