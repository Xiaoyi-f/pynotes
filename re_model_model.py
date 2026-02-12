import re

# 正则基础
pattern = r"""
^BEGIN\s+          # ^ 字符串开始
([A-Za-z]+)\s+     # | 捕获组1 - 名字
has\s+             # \s 空白字符
(\d+)\s+           # {n} 正好n次 - 这里匹配数字
apples?            # ? 0次或1次 - 's'可选
[.,\s]+           # [] 字符集合 - 匹配点、逗号、空白
([a-z]{5,})\s+     # {n,} 至少n次 - 至少5个小写字母
and\s+            
(\d{1,2})\s+       # {n,m} n到m次 - 1-2位数字
cherries\.
.*?               # . 任意字符 + 懒惰模式 *? -》加?即开启懒惰模式
total\s+
[^^]*             # [^] 非字符集合 - 不匹配^字符
\^Special\^       # 转义特殊字符
\s+
line\s+
with\s+
([0-9]+)\s+       # + 1次或多次 - 匹配一个或多个数字
items\.
\s+
.*               # * 任意次 - 匹配任意字符任意次
END$              # $ 字符串结束
"""


def func(match):
    num = match.group()
    return "*" * len(num)


flag = re.IGNORECASE | re.MULTILINE | re.DOTALL
# 常用方法
text = "123-456-7890"
re.search(pattern, text, flag).group()
print(re.findall(pattern, text, flag))
re.match(pattern, text, flag)
result = re.sub(pattern, func, text, flag)
res = re.split(r"[,:;.]+", text, flag)
phone_pattern = re.compile(pattern, flag)
phone_pattern.match(text, flag)  # ...
resu = re.finditer(pattern, text, flag)
for match in resu:
    print(match.group())
