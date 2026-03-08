__author__ = "XiaoYi --NieJianbing"
__description__ = "快速掌握python基础"
__email__ = "15779544219@163.com"
__copyright__ = "作者小翊保留所有权"
__all__ = []
YI_TEAM = [
    "YiTeam是作者组织的一个工作室",
    "专注python全栈开发",
    "专注AI开发",
    "专注逆向爬虫开发",
    "专注数据分析",
    "申请加入请联系wechat: CodingAlgorithmYT",
]
print(__description__)
print(f"作者:{__author__}")
for i in range(len(YI_TEAM)):
    print(YI_TEAM[i])
print()

"""
1.下载安装与基本使用 
浏览器搜索python官网下载对应系统的security安全版本python --> 3.10.xxx
配置系统环境变量 -> 为了使得我们可以随时打开系统的终端使用python的命令解释器 -> 系统设置搜索"环境变量" -> 配置Path环境变量，将需要全局搜寻的路径添加进去即可
使用包管理工具pip 
pip --version
pip install package[==版本号](pip默认不区分包名大小写，但是建议统一使用对应官方说明的名字) -> 安装包
pip uninstall package -> 卸载包
pip list -> 查看已经安装过的所有包
pip config list -> 查看配置好的源
pip config set (按照 pip config list 给出的形式把那个'='替换为空格 换行则重新再执行一次对应的pip config set ...命令)
pip freeze > requirements.txt -> 将当前环境的包列表冻结版本信息并保存到requirements.txt文件中
pip install -r requirements.txt -> 启动请求安装模式并且从版本列表文件requirements.txt安装
pip show package -> 查看某个包的详细信息
推荐官方高级命令行解释器: pip install ipython 

推荐IDE -> Pycharm 
Pycharm推荐插件:
    BlackConnect
    CMD Support
    CodeGlance Pro
    Indent Rainbow
    Inspection Lens
    Lingma -Alibaba
    Material Theme UI Lite
    Rainbow Brackets Lite - Free
    Translation
    AceJump --> ctrl ; 启动模式 esc 退出模式
    
Pycharm基本使用:
    配置按键映射 -> ctrl d 删除当前行
    ctrl z 撤销操作 
    ctrl shift z 反撤销操作 
    F11 给当前行贴标签
    ctrl shift F10 运行对应文件
    alt F12 打开终端 
    shift enter 直接下开一行
    顶部tab文件栏通过鼠标上下滚轮可以滚动
    
开发辅助工具:
    AI --> 辅助开发必会
    Xshell --> 远程终端连接软件
    Xftp --> 本地机与虚拟/远程机资源交互软件
    Navicat --> 图形化数据库操作软件
    Postman/Apipost --> 接口测试软件
    WattToolkit/Clash --> VPN
    typora --> MarkDown笔记软件

python简介:
    python是一个动态强类型的通用脚本语言，python解释器有很多种，官方解释器为Cpython(由C语言实现，部分实现自举)
    python代码通过python编译器首先编译成为PVM字节码，然后PVM执行字节码运行代码，但是由于python的动态特性以即它的编译依赖PVM版本
    python给人的编译感很弱，大多数人都直呼python是解释性语言
    python语法简洁灵活，适用于软件/网站开发、数据科学与人工智能、自动化脚本以即运维、网络安全、物联网与嵌入式
    
python编码统一规范:
    1.除了类名使用大驼峰命名，其他所有标识符都以蛇形命名 --> 有些人并不以这个为规范，这里是我们的规范建议
    2.测试包统一命名为test -> 测试文件/函数统一命名为test_demo
    3.文档包统一命名为docs
    4.工具包统一命名为utils
    5.包版本列表文件统一命名为requirements.txt
    6.许可证统一命名为LICENSE 或 LICENSE.txt
    7.项目配置文件统一命名为pyproject.toml
    8.源码文件夹统一命名为src
    9.数据库文件夹统一命名为db
    10.静态资源文件夹统一命名为static
    
__init__.py出口文件介绍:
    __init__.py是python软件包的出口文件，当用户导入对应的包时会自动触发执行这个文件
"""

# python基础
import this
import keyword

print()
print("python内置关键字列表\n")
print(keyword.kwlist)

builtins = [
    "Exception",
    "AttributeError",
    "TypeError",
    "ValueError",
    "KeyError",
    "IndexError",
    "NameError",
    "ImportError",
    "ModuleNotFoundError",
    "FileNotFoundError",
    "IOError",
    "ZeroDivisionError",
    "StopIteration",
    "KeyboardInterrupt",
    "MemoryError",
    "TimeoutError",
    "int -> -5 ~ 256 缓存",
    "float",
    "str -> 驻留机制",
    "bool",
    "complex",
    "bytes",
    "bytearray -> 可变",
    "list",
    "tuple",
    "set",
    "frozenset",
    "dict",
    "range",
    "sum",
    "max",
    "min",
    "abs",
    "round",
    "len",
    "all",
    "any",
    "append",
    "pop",
    "insert",
    "remove",
    "reverse",
    "extend",
    "clear",
    "slice",
    "add",
    "difference",
    "intersection",
    "union",
    "discard",
    "issubset" "get",
    "setdefault",
    "popitem",
    "update",
    "values",
    "keys",
    "items",
    "fromkeys",
    "type",
    "isinstance",
    "+ - * / % // **",
    "== != > < >= <=",
    "& | ~ >> << ^",
    "<算术运算符>=",
    ":=",
    "and or not",
    "not in",
    "is not",
    "A if ... else B",
    "0b bin",
    "0x hex",
    "0o oct",
    "print",
    "input",
    "if elif else",
    "for else",
    "while else",
    "match case _ :",
    "global",
    "nonlocal",
    "with",
    "assert",
    "del",
    "exec",
    "help",
    "dir",
    "eval",
    "hasattr",
    "getattr",
    "setattr",
    "delattr",
    "metaclass",
    "*args **kwargs",
    "/",
    "*",
    "{[(... for ... if ...)]}",
    "super",
    "repr",
    "iter",
    "next",
    "send",
    "close",
    "f-string{x:m.n}",
    "r-string",
    "zip",
    "enumerate(iterable, start=idx)",
    "map",
    "filter",
    "chr -> unicode",
    "ord -> unicode",
    "ascii",
    "divmod(num, n)",
    "issubclass(test, class_model)",
    "aiter",
    "anext",
    "compile(source, string, mode='exec/eval')",
    "locals",
    "sorted(iterable, key=func)",
    "@property",
    "@attr.setter",
    "@attr.deleter",
    "@classmethod",
    "@staticmethod",
    "try except else finally",
    "w r a b + ",
    "open (file) -> read readline(s) write writelines seek tell readable writable",
    "Descriptor -> __get__ __set__ __delete__",
    "__dict__ __mro__ __name__ __package__",
    "__new__(cls) return super().__new__(cls, *args, *kwargs)",
    "__init__(self)",
    "__call__(self)",
    "__bool__(self)",
    "__getattribute__(self, attr) return super().__getattribute__(attr)",
    "__getattr__(self, attr)",
    "__setattr__(self, attr, value) super().__setattr__(attr, value)",
    "__delattr__(self, attr) super().__delattr__(attr)",
    "__str__(self)",
    "__repr__(self)",
    "__hash__(self) <-> '=='",
    "__eq__(self, other)",
    "__slots__",
    "__iter__(self)",
    "__aiter__(self)",
    "__next__(self)",
    "__anext__(self)",
    "__contains__(self) -> in触发",
    "__add__(self)",
    "__sub__(self)",
    "__mul__(self)",
    "__truediv__(self)",
    "__floordiv__(self)",
    "__mod__(self)",
    "__pow__(self)",
    "__ne__(self)",
    "__lt__(self)",
    "__gt__(self)",
    "__le__(self)",
    "__ge__(self)",
    "__format__(self, spec)",
]

annotations = [
    "int",
    "float",
    "str",
    "bool",
    "complex",
    "bytes",
    "bytearray",
    "list[T, ...]",
    "tuple[T, ...] (变长)",
    "tuple[X, Y, ...] (定长)",
    "set[T]",
    "frozenset[T]",
    "dict[K, V]",
    "X | Y | Z | None",
    "None",
    "...",
    "object 普通对象",
    "type 类对象",
    "TypeAlias = list[int] | str 类型别名自定义",
    "-> U 函数注解, U为占位符",
    "var: T",
]

n, m = 0, 0

print("\n内置基础语法\n")
for i in builtins:
    print(i)
    n += 1

print("\n内置注解\n")
for i in annotations:
    print(i)
    m += 1

sum = n + m

print(f"总共{sum}个必会语法")
print(f"综合keywords，大约需要学习{(sum // 10 + 2) * 10}+种语法就可以掌握python基础")
