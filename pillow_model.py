from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import os

# pip install pillow

# 图形验证码
def generate_captcha(text=None, width=120, height=40):
    """生成验证码图片

    Args:
        text: 验证码文字（默认随机4位）
        width: 图片宽
        height: 图片高
    Returns:
        (图片对象, 验证码文字)
    """
    # 1. 生成随机验证码（默认4位：数字+大写字母）
    if text is None:
        text = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    # 2. 创建空白图片（RGB模式，背景色随机浅色）
    bg_color = (
        random.randint(200, 255),
        random.randint(200, 255),
        random.randint(200, 255),
    )
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    # 3. 字体设置（工作用绝对路径或系统字体）
    try:
        # Windows常用字体路径
        font_paths = [
            "C:/Windows/Fonts/Arial.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Arial.ttf",  # Mac
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 30)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    # 4. 绘制文字（每个字符随机位置、颜色）
    x = 10
    for i, char in enumerate(text):
        y = random.randint(5, 10)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        draw.text((x, y), char, fill=color, font=font)
        x += 25  # 字符间距
    # 5. 添加干扰线（2-3条）
    for _ in range(random.randint(2, 3)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(150, 150, 150), width=1)
    # 6. 添加噪点
    for _ in range(100):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        img.putpixel((x, y), (0, 0, 0))

    return img, text


def save_captcha(img, text, save_dir="captchas"):
    """保存验证码（文件名用验证码文字，方便调试）"""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{text}.png")
    img.save(path)
    print(f"验证码已保存: {path}")
    return path


def verify_captcha(user_input, correct_text):
    """验证用户输入（忽略大小写）"""
    return user_input.upper() == correct_text.upper()


def batch_generate_captcha(count=10):
    """批量生成验证码（用于测试/训练）"""
    captchas = []
    for i in range(count):
        img, text = generate_captcha()
        captchas.append((img, text))
        img.save(f"captcha_{i}_{text}.png")
    return captchas
