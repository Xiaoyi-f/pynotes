import itertools
from itertools import permutations, combinations

list1, list2, list3 = [1, 2, 3], [4, 5, 6], [7, 8, 9]
merged = list(itertools.chain(list1, list2, list3))  # [1,2,3,4,5,6,7,8,9]


colors, sizes = ["红", "蓝"], ["S", "M"]

result = [
    f"{c}{s}" for c, s in itertools.product(colors, sizes)
]  # ['红S','红M','蓝S','蓝M']


items = ["A", "B", "C"]
list(combinations(items, 2))  # 组合 [('A','B'),('A','C'),('B','C')] 顺序无关
list(permutations(items, 2))  # 排列 [('A','B'),('A','C'),('B','A'),...] 顺序有关


workers = ["张三", "李四", "王五"]
tasks = ["任务1", "任务2", "任务3", "任务4", "任务5", "任务6", "任务7"]

# 创建无限循环的工人列表
worker_cycle = itertools.cycle(workers)

# 给每个任务分配一个工人（轮流）
for task in tasks:
    worker = next(worker_cycle)  # 依次取：张三、李四、王五、张三、李四...
    print(f"{task} -> {worker}")
