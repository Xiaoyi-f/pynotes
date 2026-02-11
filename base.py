"""
python基础语法模块.

基础配置：
    # Linux/Mac - 换源
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

    # Windows（PowerShell或CMD） - 换源
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

    pip config list

    pip install black
    pip -m venv .venv -> .venv/Scripts/activate # deactivate

    pip install ipython -> 下载高级 python shell

pycharm推荐基础插件:
    BlackConnect
    CMD Support
    CodeGlance Pro
    Indent Rainbow
    Inspection Lens
    Lingma -Alibaba
    Material Theme UI Lite
    Rainbow Brackets Lite - Free
    Translation
    -> 其他插件需要什么搜索对应名字找好用的官方的使用即可

统一规范:
    包/目录/变量/函数/方法名 -> 蛇形小写
    类名 -> 大驼峰
    私有构建包&测试包 -> _utils&tests -> _tools&test_demo
    文档包 -> docs
    工具包 -> utils
    依赖文件 -> requirements.txt
    许可证 -> LICENSE
    项目配置 -> pyproject.toml
    源码 -> src

注意事项:
    object构造函数创建的实例不能动态创建属性，因为object类早期为节省空间，并没有实现动态添加属性到__dict__，它的__dict__是只读的
    空或零值被判定为False
    _*标识为保护状态
    __*标识为私有状态，实际可以通过_类名__属性名来访问/修改
"""
import sys
import math
import time
import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass


int_num = int(12)  # python的int类型是大数字，会自行扩展
float_num = float(12.5)  # python的float类型是双精度的，占据8个字节
string = str("hello world")  # .find(sub_string) .lower() .upper() .title() .replace(old, new) .split(sep) .join(iterable)
complex_num = complex(1, 2)  # 1 + 2j
bytes_data = b"hello world"
byte_array = bytearray(b"hello world")
# result = functools.reduce(lambda: x + y, iterable)
# .append(val) .pop(idx) .insert(idx, val) .remove(val) .reverse .extend(list) .index(val) .count(val)
list_data = list([1, 3, 5, 7])
# [start: end: step] .count(val) .index(val)
tuple_data = tuple((1, 3, 5, 7))
# .add(val) .clear() .difference() .intersection() .pop() .remove() .discard() .union() .update(iterable)->批量添加
set_data = frozenset({1, 3, 5, 7})  # &set
# .get(key, default) .setdefault(key, default) .popitem() .update(dict)
dict_data = dict({"name": "xiaoyi", "hash_only": "hash_only"})
# sum() max() min() abs() round() len() all() any()
none_data = None
true_val = True
false_val = False
eval("(1+1) + (1-1) + (1*1) + (1/1) + (1//1) + (1%1) + (1**1)")  # *= :=
exec("比较运算符 = input('== != > < >= <= 这些是什么呢?')")

# math
# math.ceil() math.floor() math.sqrt() math.factorial() math.isnan() math.isinf()
inf = -math.inf
nan = math.nan

# & | ~ ^ << >> 位运算符
oct_num = 0o10  # oct()
hex_num = 0x10  # hex()
bin_num = 0b10  # bin()

if 1 and 1 or 1 and (not 1):
    print("test_success")
elif 0 and 1:
    print("短路特性")
elif 1 or 0:
    print("短路特性")
else:
    print("over_test")

# id() is not isinstance(var, type)
# not in

container = {"start": None, "end": None, "step": None}
for i in container.keys():  # .values() .items()
    container[i] = input(f"请输入{i}的值:")

start, end, step = int(container["start"]), int(container["end"]), int(container["step"])

for i in range(start, end, step):
    pass

# __bases__ __class__ __dict__->dir(obj) __mro__ __name__
# __new__(本类) __init__(本类实例) __call__(本类实例) __bool__(本类实例)
# __getattribute__(本类实例，属性名)->return super().__getattribute__(属性名)
# __getattr__(本类实例, 属性名)->return name __setattr__(本类实例, 属性名, 属性值)->super().__setattr__(属性名, 属性值) __delattr__(本类实例, 属性名)->super().__delattr__(属性名)
# __hash__(本类实例)->return __str__(本类实例)->return __repr__(本类实例)->return
# __add__(本类实例, 参数)->return __sub__(本类实例, 参数)->return __mul__(本类实例, 参数)->return __truediv__(本类实例, 参数)->return __floordiv__(本类实例, 参数)->return __mod__(本类实例, 参数)->return __pow__(本类)
# __eq__(本类实例, 参数)->return __ne__(本类实例, 参数)->return __lt__(本类实例, 参数)->return __gt__(本类实例, 参数)->return __le__(本类实例, 参数)->return __ge__(本类实例, 参数)->return
# __format__(self, format_spec)->format_spec = xxx->return

print(type(type), sep='', end='\n', file=sys.stderr)  # 元类
help(object)  # 基类

"""
装饰器:
    @property
    @attr.setter
    @attr.deleter
    @classmethod -> 本类
    @staticmethod -> 无特参
    @functools.lru_cache
    @abstractmethod
"""


class MyMeta(type):
    __slots__ = "slots"  # 限制实例变量

    # 实现iter协议便可当迭代器对象
    def __iter__(cls):
        pass

    # 实现next协议才可以使用next()函数
    def __next__(cls):
        pass


def MyClass(metaclass=MyMeta):
    pass


class ExceptionNew(Exception):
    pass


def argv_decorator(*argv):
    def decorator(func):
        @functools.wraps(func)  # 保持元信息
        def wrapper(*args, **kwargs):
            print(f"启动装饰器{argv}")
            print(func(*args, **kwargs))
            print(f"关闭装饰器{argv}")

        return wrapper

    return decorator


@argv_decorator("argv_decorator")
def add(a, b):
    return a + b


# 闭包
def person(name, age):
    def get_info():
        return f"Name: {name}, Age: {age}"

    def set_age(new_age):
        nonlocal age
        age = new_age

    return get_info, set_age


class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        print("汪汪汪")


def power(base, exp):
    return base ** exp

square = functools.partial(power, exp=2)

@dataclass # -> 自动生成对应__init__, __repr__, __eq__
class data():
    name: str
    age: int
    height: float

with open("test.txt", "w") as file:
    """
    file.read(字节数)
    file.readlines()
    file.write(data)
    file.writelines(iterable)
    file.seek(+/-字节数, 0/1/2)
    file.tell()
    file.readable()
    file.writable()
    """
    pass

class Timer:
    def __enter__(self):
        self.start_time = time.time()
        time.sleep(1)
        return self

    # exc_type -> 异常类型 exc_value -> 异常值 exc_trace -> 异常回溯信息
    def __exit__(self, exc_type, exc_value, exc_trace):
        end_time = time.time()
        print(f"Elpased time: {end_time - self.start_time:.4f} seconds")
        print(f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}")
        return False


if __name__ == "__main__":
    try:
        pass
    except ExceptionNew as e:
        print(e)
    else:
        print("没有异常")
    finally:
        print("无论是否有异常都会执行")

