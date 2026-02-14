from PIL import Image, ImageDraw
import qrcode

# 生成二维码
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr.add_data("https://baidu.com")
qr.make(fit=True)
img = qr.make_image().convert("RGB")

# 生成简单Logo(50x50的彩色方块)
logo = Image.new("RGB", (50, 50), "#FF6B6B")
draw = ImageDraw.Draw(logo)
draw.ellipse((10, 10, 40, 40), fill="#4ECDC4")

# 粘贴Logo
img.paste(logo, (img.size[0] // 2 - 25, img.size[1] // 2 - 25))
img.save("qr.png")
print("生成成功:qr.png")
