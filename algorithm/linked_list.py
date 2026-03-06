# 链表判环 -> 快慢指针
def get_next(x):
    sum = 0
    digit = x % 10
    sum += digit * digit
    x //= 10

    return sum


def resolve(n):
    slow, fast = n, n
    while fast != 1:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

        if slow == fast and slow != 1:
            return False
    return True


if __name__ == "__main__":
    n = int(input("请输入一个数值，我将判断它是否为快乐数:"))
    print(resolve(n))

