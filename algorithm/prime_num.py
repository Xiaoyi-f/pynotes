# 实现质数判断
import math


def resolve():
    num = int(input("请输入判断数值:"))

    # 2 偶数 小数倍数
    def handler(num):
        if num <= 1:
            return False
        elif num == 2:
            return True
        elif num % 2 == 0:
            return False

        # sqrt 返回float range只接受int类型
        for i in range(3, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    print(f'{num} {"is" if handler(num) else "is not"} prime.')


if __name__ == "__main__":
    while True:
        resolve()
