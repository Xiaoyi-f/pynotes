from enum import Enum, Flag, auto


class color(Enum):
    RED = 1  # 红
    GREEN = 2  # 绿
    BLUE = 3  # 蓝


# 使用
print(color.RED)  # 颜色.RED
print(color.RED.name)  # 'RED'（名称）
print(color.RED.value)  # 1（值）
print(type(color.RED))  # <enum '颜色'>


# Flag支持位运算
class root(Flag):
    read = auto()  # 1 (0b0001)
    write = auto()  # 2 (0b0010)
    execute = auto()  # 4 (0b0100)
    delete = auto()  # 8 (0b1000)


# 组合root
user_root = root.read | root.write  # 3 (0b0011)

print(user_root)  # root.read|write
print(root.read in user_root)  # True
print(root.execute in user_root)  # False

# 更多操作
print(user_root & root.read)  # root.read
print(user_root ^ root.read)  # root.write（去掉read）
print(user_root | root.execute)  # root.read|write|execute
