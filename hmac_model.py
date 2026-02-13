import hmac
import hashlib

# 1️⃣ 第一步：约定密钥（就像暗号）
密钥 = b"our_secret_key"  # 客户端和服务器都知道

# 2️⃣ 第二步：要保护的消息
消息 = b"transfer 100 yuan"

# 3️⃣ 第三步：生成签名（贴防伪标签）
签名 = hmac.new(
    key=密钥, msg=消息, digestmod=hashlib.sha256  # 暗号  # 内容  # 算法
).hexdigest()  # 转成16进制字符串

print(f"签名: {签名}")


# 4️⃣ 第四步：验证签名（检查是否被篡改）
def 验证(原始消息, 收到的签名):
    """验证消息是否真实"""
    # 重新计算应该的签名
    应该的签名 = hmac.new(key=密钥, msg=原始消息, digestmod=hashlib.sha256).hexdigest()

    # 安全比较（必须用这个！）
    return hmac.compare_digest(收到的签名, 应该的签名)


# 测试
print(验证(b"transfer 100 yuan", 签名))  # True（没被改过）
print(验证(b"transfer 10000 yuan", 签名))  # False（被篡改了）
