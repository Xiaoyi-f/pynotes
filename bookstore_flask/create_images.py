from PIL import Image, ImageDraw, ImageFont
import os
import platform

# 创建图片的函数
def create_image(filename, width, height, text, bg_color=(102, 126, 234), text_color=(255, 255, 255)):
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 根据操作系统选择合适的字体
    system = platform.system()
    font_size = 24 if len(text) <= 4 else 18
    
    try:
        if system == 'Windows':
            # Windows系统使用微软雅黑或宋体
            try:
                font = ImageFont.truetype("msyh.ttc", font_size)
            except:
                try:
                    font = ImageFont.truetype("simsun.ttc", font_size)
                except:
                    font = ImageFont.truetype("arial.ttf", font_size)
        else:
            # 其他系统尝试使用常见字体
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # 计算文本位置使其居中
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # 如果textbbox不可用，使用textsize
        text_width, text_height = draw.textsize(text, font=font)
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    # 绘制文字阴影效果
    draw.text((x + 1, y + 1), text, fill=(0, 0, 0), font=font)
    draw.text((x, y), text, fill=text_color, font=font)
    
    img.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

# 创建images目录下的图片
images_dir = "static/images"
os.makedirs(images_dir, exist_ok=True)

# 登录按钮
create_image(os.path.join(images_dir, "login_button.jpg"), 100, 40, "登录", (102, 126, 234))

# 注册按钮
create_image(os.path.join(images_dir, "reg_button.jpg"), 100, 40, "注册", (40, 167, 69))

# 提交按钮
create_image(os.path.join(images_dir, "submit_button.jpg"), 100, 40, "提交", (255, 102, 0))

# 提交订单按钮
create_image(os.path.join(images_dir, "submit_order.jpg"), 120, 40, "提交订单", (255, 102, 0))

# 用户图标
create_image(os.path.join(images_dir, "2.jpg"), 40, 40, "用户", (102, 126, 234))

# 密码图标
create_image(os.path.join(images_dir, "3.jpg"), 40, 40, "密码", (40, 167, 69))

# 书籍图标
create_image(os.path.join(images_dir, "4.jpg"), 40, 40, "书籍", (255, 102, 0))

# 购物车图标1
create_image(os.path.join(images_dir, "mycar1.jpg"), 40, 40, "购物车", (102, 126, 234))

# 购物车图标2
create_image(os.path.join(images_dir, "mycar.jpg"), 40, 40, "购物车", (255, 102, 0))

# 注册图标
create_image(os.path.join(images_dir, "reg.jpg"), 40, 40, "注册", (40, 167, 69))

# 列表图标
create_image(os.path.join(images_dir, "list.jpg"), 40, 40, "列表", (102, 126, 234))

# 信息图标
create_image(os.path.join(images_dir, "info.jpg"), 40, 40, "信息", (255, 102, 0))

# 按钮图标
create_image(os.path.join(images_dir, "button.jpg"), 100, 40, "加入购物车", (255, 102, 0))

# 用户图标
create_image(os.path.join(images_dir, "user.jpg"), 40, 40, "用户", (102, 126, 234))

# 创建goods_images目录下的图片
goods_images_dir = "static/goods_images"
os.makedirs(goods_images_dir, exist_ok=True)

# 创建商品图片
book_colors = [
    (102, 126, 234),  # 蓝色
    (40, 167, 69),    # 绿色
    (255, 102, 0),    # 橙色
    (220, 53, 69),    # 红色
    (108, 117, 125)   # 灰色
]

book_titles = [
    "Python全栈开发",
    "Flask Web开发",
    "数据库原理",
    "算法导论",
    "机器学习实战"
]

for i, (color, title) in enumerate(zip(book_colors, book_titles), 1):
    img = Image.new('RGB', (360, 360), (245, 245, 245))
    draw = ImageDraw.Draw(img)
    
    # 绘制书本封面
    draw.rectangle([30, 30, 330, 330], fill=color, outline=(0, 0, 0), width=3)
    
    # 绘制书脊
    draw.rectangle([30, 30, 55, 330], fill=tuple(max(0, c - 40) for c in color))
    
    # 添加文字
    try:
        if system == 'Windows':
            try:
                font_large = ImageFont.truetype("msyh.ttc", 28)
                font_small = ImageFont.truetype("msyh.ttc", 18)
            except:
                try:
                    font_large = ImageFont.truetype("simsun.ttc", 28)
                    font_small = ImageFont.truetype("simsun.ttc", 18)
                except:
                    font_large = ImageFont.truetype("arial.ttf", 28)
                    font_small = ImageFont.truetype("arial.ttf", 18)
        else:
            font_large = ImageFont.truetype("DejaVuSans.ttf", 28)
            font_small = ImageFont.truetype("DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 绘制标题
    try:
        bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = bbox[2] - bbox[0]
        title_height = bbox[3] - bbox[1]
    except:
        title_width, title_height = draw.textsize(title, font=font_large)
    
    title_x = (360 - title_width) / 2
    title_y = 140
    
    # 文字阴影
    draw.text((title_x + 2, title_y + 2), title, fill=(0, 0, 0), font=font_large)
    draw.text((title_x, title_y), title, fill=(255, 255, 255), font=font_large)
    
    # 绘制副标题
    subtitle = f"Book {i}"
    try:
        bbox = draw.textbbox((0, 0), subtitle, font=font_small)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_height = bbox[3] - bbox[1]
    except:
        subtitle_width, subtitle_height = draw.textsize(subtitle, font=font_small)
    
    subtitle_x = (360 - subtitle_width) / 2
    subtitle_y = title_y + title_height + 20
    
    draw.text((subtitle_x + 1, subtitle_y + 1), subtitle, fill=(0, 0, 0), font=font_small)
    draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 255, 255), font=font_small)
    
    filename = os.path.join(goods_images_dir, f"book{i}.jpg")
    img.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

# 创建默认商品图片
create_image(os.path.join(goods_images_dir, "default.jpg"), 360, 360, "暂无图片", (245, 245, 245), (108, 117, 125))

print("\n所有图片创建完成！")