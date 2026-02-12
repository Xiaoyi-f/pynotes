from PIL import Image, ImageFilter, ImageDraw, ImageFont

# pip install pillow
import os

# ============ Pillow = 图片处理（缩略图/水印/格式转换）============

# ------------ 1. 打开/保存/格式转换 ------------
# 打开图片
img = Image.open("input.jpg")

# 格式转换（保存时自动转）
img.save("output.png")  # JPG转PNG
img.save("output.webp")  # 转WebP（网页用）


# ------------ 2. 缩略图（最常用）------------
def make_thumbnail():
    """生成缩略图，等比例缩放"""
    img = Image.open("photo.jpg")

    # 方法1：thumbnail（直接改原图，等比例）
    img.thumbnail((300, 300))  # 宽高不超过300，比例不变
    img.save("thumb.jpg")

    # 方法2：resize（强制尺寸，会变形）
    resized = img.resize((300, 300))  # 不推荐，除非你就是要变形
    resized.save("resized.jpg")


# ------------ 3. 调整大小/裁剪 ------------
img = Image.open("input.jpg")

# 裁剪 (左, 上, 右, 下)
cropped = img.crop((100, 100, 400, 400))
cropped.save("cropped.jpg")

# 调整大小（指定宽高）
resized = img.resize((800, 600))
resized.save("resized.jpg")


# ------------ 4. 添加水印（文字/图片）------------
def add_watermark():
    """给图片添加文字水印"""
    img = Image.open("photo.jpg").convert("RGBA")

    # 创建透明层
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)

    # 写文字
    text = "© 2024"
    # 字体（系统字体路径，Linux/Mac/Windows不同）
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()  # 无字体时用默认

    # 计算文字位置（右下角）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = img.width - text_width - 20
    y = img.height - text_height - 20

    # 绘制文字（白色，半透明）
    draw.text((x, y), text, fill=(255, 255, 255, 128), font=font)

    # 合并
    watermarked = Image.alpha_composite(img, txt)
    watermarked.save("watermarked.png")


# ------------ 5. 滤镜效果 ------------
img = Image.open("photo.jpg")

# 模糊
blurred = img.filter(ImageFilter.BLUR)
blurred = img.filter(ImageFilter.GaussianBlur(radius=2))  # 高斯模糊

# 轮廓
outline = img.filter(ImageFilter.CONTOUR)

# 边缘增强
enhanced = img.filter(ImageFilter.EDGE_ENHANCE)

# 黑白
bw = img.convert("L")  # L = 灰度


# ------------ 6. 批量处理（实战）------------
def batch_resize(input_dir, output_dir, size=(800, 600)):
    """批量调整图片大小"""
    from pathlib import Path

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for img_file in input_path.glob("*.jpg"):
        with Image.open(img_file) as img:
            # 等比例缩放宽高不超过size
            img.thumbnail(size)
            # 保存到输出目录，保持原名
            img.save(output_path / img_file.name)
            print(f"处理: {img_file.name}")


def batch_convert(input_dir, output_format="png"):
    """批量格式转换"""
    from pathlib import Path

    for img_file in Path(input_dir).glob("*.*"):
        if img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            out_file = img_file.with_suffix(f".{output_format}")
            with Image.open(img_file) as img:
                img.save(out_file)
                print(f"转换: {img_file.name} -> {out_file.name}")


# ------------ 7. 验证码生成 ------------
def generate_captcha(text=None, width=200, height=80):
    """简单的验证码图片"""
    import random

    if text is None:
        import string

        text = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # 创建空白图片
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # 绘制文字（随机位置、颜色）
    for i, char in enumerate(text):
        x = 20 + i * 40 + random.randint(-5, 5)
        y = 20 + random.randint(-5, 5)
        color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        draw.text((x, y), char, fill=color, font=font)

    # 添加干扰线
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill="gray", width=1)

    return img, text


# ------------ 8. 获取图片信息 ------------
def get_image_info(path):
    """获取图片元数据"""
    with Image.open(path) as img:
        info = {
            "格式": img.format,
            "尺寸": f"{img.width}x{img.height}",
            "模式": img.mode,
            "大小": f"{os.path.getsize(path) / 1024:.1f}KB",
            "调色板": img.palette is not None,
        }
        return info


# ------------ 9. 压缩图片（降低质量）------------
def compress_image(input_path, output_path=None, quality=85):
    """压缩JPG图片，减小文件大小"""
    if output_path is None:
        output_path = input_path

    with Image.open(input_path) as img:
        # 转换为RGB（去掉透明通道）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        # quality 1-100，越小文件越小，画质越差
        img.save(output_path, "JPEG", quality=quality, optimize=True)


# ------------ 10. 简单示意图（纯色+文字）------------
def create_placeholder(width=800, height=600, color="gray", text=None):
    """生成占位图"""
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)

    if text is None:
        text = f"{width}x{height}"

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # 文字居中
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, fill="white", font=font)
    return img


# ============ 完整示例 ============
if __name__ == "__main__":
    # 1. 生成验证码
    captcha_img, code = generate_captcha()
    captcha_img.save("captcha.png")
    print(f"验证码: {code}")

    # 2. 创建占位图
    placeholder = create_placeholder(400, 300, "blue", "Hello PIL")
    placeholder.save("placeholder.jpg")

    # 3. 获取图片信息
    info = get_image_info("placeholder.jpg")
    for k, v in info.items():
        print(f"{k}: {v}")

    # 4. 批量处理（先创建测试图片）
    Path("test_imgs").mkdir(exist_ok=True)
    for i in range(3):
        img = Image.new("RGB", (100, 100), color="red")
        img.save(f"test_imgs/test_{i}.jpg")

    # 批量缩略图
    batch_resize("test_imgs", "test_imgs/thumbs", (50, 50))
