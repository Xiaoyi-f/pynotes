import hmac
import hashlib
import os

# ============ 1. HMAC本质 ============
# HMAC = 哈希 + 密钥（防篡改、防伪造）
# 场景：API签名、Webhook回调验证、JWT

# ============ 2. 基本用法（必会） ============
def basic_hmac():
    """API签名验证"""
    # 2.1 服务端和客户端约定好密钥（放环境变量）
    secret_key = b"my_api_secret_key_2024"  # 绝不上传git

    # 2.2 客户端：生成签名
    message = b"user_id=123&amount=100&timestamp=1700000000"
    signature = hmac.new(
        key=secret_key,      # 密钥（bytes）
        msg=message,        # 要签名的数据（bytes）
        digestmod=hashlib.sha256  # 哈希算法
    ).hexdigest()  # 输出十六进制字符串

    # 2.3 服务端：用相同密钥和算法验证
    # 收到请求后，用同样的参数重新计算签名，比对
    expected = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
    is_valid = hmac.compare_digest(signature, expected)  # ✅ 安全比对（防时序攻击）

    return signature, is_valid


# ============ 3. 实战：Webhook签名验证 ============
class WebhookVerifier:
    """验证第三方回调（GitHub、Stripe、微信支付）"""

    def __init__(self, secret: str):
        self.secret = secret.encode()

    def sign(self, payload: bytes) -> str:
        """生成签名（给第三方用的，通常不需要）"""
        return hmac.new(
            self.secret,
            payload,
            hashlib.sha256
        ).hexdigest()

    def verify(self, payload: bytes, signature: str) -> bool:
        """验证回调签名（必会！）"""
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)  # ✅ 必须用compare_digest


# ============ 4. 实战：API请求签名 ============
class APISigner:
    """防止请求被篡改"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret.encode()

    def sign_request(self, method: str, path: str, body: str = "", timestamp: str = None):
        """生成请求签名（客户端用）"""
        if timestamp is None:
            timestamp = str(int(time.time()))

        # 构建签名串
        message = f"{method}\n{path}\n{body}\n{timestamp}\n{self.api_key}".encode()

        signature = hmac.new(
            self.api_secret,
            message,
            hashlib.sha256
        ).hexdigest()

        return {
            'X-API-Key': self.api_key,
            'X-Timestamp': timestamp,
            'X-Signature': signature
        }

    def verify_request(self, headers: dict, method: str, path: str, body: str = ""):
        """验证请求签名（服务端用）"""
        signature = headers.get('X-Signature')
        timestamp = headers.get('X-Timestamp')
        api_key = headers.get('X-API-Key')

        # 1. 校验时间戳防重放（5分钟过期）
        if abs(int(time.time()) - int(timestamp)) > 300:
            return False

        # 2. 重新计算签名
        message = f"{method}\n{path}\n{body}\n{timestamp}\n{api_key}".encode()
        expected = hmac.new(
            self.api_secret,  # 根据api_key查出来
            message,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)


# ============ 5. 文件完整性校验（带密钥） ============
def sign_file(file_path: str, key: bytes) -> str:
    """给文件签名，防止被替换"""
    h = hmac.new(key, b"", hashlib.sha256)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()


# ============ 6. 重要：为什么用HMAC而不是普通哈希？ ============
def why_hmac():
    """攻击者不知道密钥，无法伪造签名"""

    # ❌ 错误：直接用哈希拼接密钥（长度扩展攻击风险）
    insecure = hashlib.sha256(b"secret" + b"message").hexdigest()

    # ✅ 正确：HMAC标准算法，无漏洞
    secure = hmac.new(b"secret", b"message", hashlib.sha256).hexdigest()

    # 更重要的是：HMAC.compare_digest() 防时序攻击
    # 普通 == 比较：发现第一个不同字节就返回False，时间差异可被攻击
    # compare_digest：固定时间比较，不泄露信息
    return secure


# ============ 一句话总结 ============
# - hmac.new(key, msg, algo).hexdigest()  # 生成签名
# - hmac.compare_digest(sig1, sig2)       # 安全验证（必用！）
#
# 场景：
# 1. API签名验证（防止篡改）⭐ 必会
# 2. Webhook回调验证（GitHub/支付宝）⭐ 必会
# 3. JWT/Token签名（实际用库，原理是HMAC）

if __name__ == '__main__':
    import time

    # 测试Webhook验证
    verifier = WebhookVerifier("whsec_abc123")
    payload = b'{"event":"user.created","id":123}'
    sig = verifier.sign(payload)
    assert verifier.verify(payload, sig)  # ✅
    assert not verifier.verify(payload, "fake")  # ❌
    print("Webhook验证通过")

    # 测试API签名
    signer = APISigner("ak_123", "sk_secret")
    headers = signer.sign_request("POST", "/api/order", '{"amount":100}')
    assert signer.verify_request(headers, "POST", "/api/order", '{"amount":100}')
    print("API签名验证通过")