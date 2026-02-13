import hashlib
import os


# 字符串哈希
def normal_hash():
    # 字符串哈希
    data = "hello world"
    hash_data = hashlib.sha256(data.encode()).hexdigest()
    # b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    # 转成16进制字符串返回
    return hash_data.hexdigest()


# 密码哈希
def password_hash():
    password = "user123456"

    # 生成随机盐（每个用户不同）
    salt = os.urandom(16)  # 16字节盐

    # 计算哈希
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

    # 验证密码 -> python允许函数嵌套，函数是对象
    def verify(input_pwd, stored_salt_hex, stored_hash_hex):
        salt = bytes.fromhex(stored_salt_hex)
        test_hash = hashlib.pbkdf2_hmac(
            "sha256", input_pwd.encode(), salt, 100000
        ).hex()
        return test_hash == stored_hash_hex

    return salt_hex, hash_hex, verify
