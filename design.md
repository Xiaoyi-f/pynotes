基本概念:
接口定义了一个契约，其中规定了软件组件（如类、模块）必须提供的操作（方法），但隐藏了这些操作的内部实现细节
基本设计模式:
1.抽象工厂模式
抽象工厂模式提供一个接口，用于创建一系列相关或相互依赖的对象，而无需指定它们具体的类，工厂即生产物件
由于python本身没有接口类型，一般使用继承的形式来实现接口

示例代码:
class Tool():
    def __init__(self):
        pass
class Chair():
    def __init__(self):
        pass

class ToolFactory():
    def create_tool():
        pass

class ChairFactory():
    def create_chair():
        pass

class ComponentFactory():
    def create_chair():
        pass

    def create_tool():
        pass


工厂方法模式(虚拟构造器)
工厂方法模式属于设计模式中的“虚拟构造器”，它的核心是定义一个创建对象的接口，但由子类决定要实例化的类是哪一个
class PoliceDrawer:
    def __init__(self, person):
        self.person = person 

    def draw(self):
        print("name:", self.person.name)

class Police:
    def __init__(self, name):
        self.name = name

def create_drawer(self):
    return PoliceDrawer(self)
原型模式
原型模式是一种创建型设计模式，它通过复制现有对象（称为原型）来创建新对象，而不是通过传统的__init__方法实例化
Tip: __copy__和__deepcopy__是Python中的特殊方法，用于自定义对象的拷贝行为，当调用copy.copy()和copy.deepcopy()时，Python会自动调用这些方法
import copy

class Prototype:
    def __init__(self, name):
        self.name = name
    
    def clone(self):
        return copy.copy(self)  # 浅拷贝

    def __copy__(self):
        print("浅拷贝成功啦！")
        return type(self)(name) # type(xx)(参数) = ClassDemo(args)


生成器模式
生成器模式（Builder Pattern）是一种创建型设计模式，它将一个复杂对象的构建与其表示分离，使得同样的构建过程可以创建不同的表示
class Builder:
    def __init__(self):
        self.product = Product()
    
    def set(self, attr, value):
        setattr(self.product, attr, value)
        return self
    
    def build(self):
        return self.product

# 使用
product = Builder().set("name", "test").set("price", 100).build()
单例模式
单例模式（Singleton Pattern）是一种创建型设计模式，确保一个类只有一个实例，并提供一个全局访问点
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logs = []

# 测试
log1 = Logger()
log2 = Logger()
print(log1 is log2)  # True

十大行为模式
1. 观察者模式（Observer）
概念：定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。
class Subject:
    def __init__(self):
        self.observers = []
        self.state = None
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def notify(self):
        for observer in self.observers:
            observer.update(self.state)

class Observer:
    def update(self, state):
        print(f"观察到状态变化: {state}")

# 使用
subject = Subject()
observer = Observer()
subject.attach(observer)
subject.state = "新状态"
subject.notify()  # 输出: 观察到状态变化: 新状态
2. 策略模式（Strategy）
概念：定义一系列算法，把它们一个个封装起来，并且使它们可以相互替换，让算法的变化独立于使用算法的客户。
class Strategy:
    def execute(self, a, b): pass

class AddStrategy(Strategy):
    def execute(self, a, b): return a + b

class MultiplyStrategy(Strategy):
    def execute(self, a, b): return a * b

class Context:
    def __init__(self, strategy):
        self.strategy = strategy
    def execute(self, a, b):
        return self.strategy.execute(a, b)

# 使用
context = Context(AddStrategy())
print(context.execute(3, 4))  # 输出: 7
context.strategy = MultiplyStrategy()
print(context.execute(3, 4))  # 输出: 12
3. 命令模式（Command）
概念：将一个请求封装为一个对象，从而可以用不同的请求对客户进行参数化，对请求排队或记录请求日志，以及支持可撤销的操作。
class Light:
    def on(self): return "灯亮了"
    def off(self): return "灯灭了"

class Command:
    def execute(self): pass

class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    def execute(self):
        return self.light.on()

class RemoteControl:
    def set_command(self, command):
        self.command = command
    def press_button(self):
        return self.command.execute()

# 使用
light = Light()
cmd = LightOnCommand(light)
remote = RemoteControl()
remote.set_command(cmd)
print(remote.press_button())  # 输出: 灯亮了
4. 迭代器模式（Iterator）
概念：提供一种方法顺序访问一个聚合对象中的各个元素，而又不暴露该对象的内部表示。
class Iterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0
    
    def has_next(self):
        return self.index < len(self.collection)
    
    def next(self):
        if self.has_next():
            item = self.collection[self.index]
            self.index += 1
            return item
        return None

# 使用
items = [1, 2, 3]
iterator = Iterator(items)
while iterator.has_next():
    print(iterator.next())  # 输出: 1 2 3 每行一个
5. 模板方法模式（Template Method）
概念：定义一个操作中的算法骨架，而将一些步骤延迟到子类中，使得子类可以不改变算法结构即可重定义算法的某些特定步骤。
class DataProcessor:
    def process(self):
        self.load_data()
        self.analyze()
        self.save_results()
    
    def load_data(self):
        print("加载通用数据")
    
    def analyze(self):
        pass  # 子类实现
    
    def save_results(self):
        print("保存结果")

class CSVProcessor(DataProcessor):
    def analyze(self):
        print("分析CSV数据")

# 使用
processor = CSVProcessor()
processor.process()  # 加载通用数据 -> 分析CSV数据 -> 保存结果
6. 状态模式（State）
概念：允许一个对象在其内部状态改变时改变它的行为，对象看起来似乎修改了它的类。
class State:
    def handle(self): pass

class StartState(State):
    def handle(self):
        return "开始状态"

class StopState(State):
    def handle(self):
        return "停止状态"

class Context:
    def __init__(self):
        self.state = StartState()
    
    def request(self):
        return self.state.handle()

# 使用
context = Context()
print(context.request())  # 输出: 开始状态
7. 职责链模式（Chain of Responsibility）
概念：使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系，将这些对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。
class Handler:
    def __init__(self):
        self.next = None
    
    def set_next(self, handler):
        self.next = handler
        return handler
    
    def handle(self, request):
        if self.next:
            return self.next.handle(request)
        return None

class HandlerA(Handler):
    def handle(self, request):
        if request == "A":
            return f"HandlerA处理: {request}"
        return super().handle(request)

class HandlerB(Handler):
    def handle(self, request):
        if request == "B":
            return f"HandlerB处理: {request}"
        return super().handle(request)

# 使用
handler = HandlerA()
handler.set_next(HandlerB())
print(handler.handle("B"))  # 输出: HandlerB处理: B
8. 访问者模式（Visitor）
概念：表示一个作用于某对象结构中的各元素的操作，它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。
class Element:
    def accept(self, visitor): pass

class ElementA(Element):
    def accept(self, visitor):
        visitor.visit_a(self)

class ElementB(Element):
    def accept(self, visitor):
        visitor.visit_b(self)

class Visitor:
    def visit_a(self, element): print("访问A")
    def visit_b(self, element): print("访问B")

# 使用
elements = [ElementA(), ElementB()]
visitor = Visitor()
for element in elements:
    element.accept(visitor)  # 输出: 访问A \n 访问B
9. 备忘录模式（Memento）
概念：在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态，这样以后就可将该对象恢复到原先保存的状态。
class Memento:
    def __init__(self, state):
        self.state = state

class Originator:
    def __init__(self):
        self.state = ""
    
    def save(self):
        return Memento(self.state)
    
    def restore(self, memento):
        self.state = memento.state

# 使用
originator = Originator()
originator.state = "状态1"
saved = originator.save()  # 保存状态
originator.state = "状态2"
originator.restore(saved)  # 恢复状态
print(originator.state)  # 输出: 状态1
10. 解释器模式（Interpreter）
概念：给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。
class Expression:
    def interpret(self, context): pass

class Number(Expression):
    def __init__(self, value): self.value = value
    def interpret(self, context): return self.value

class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def interpret(self, context):
        return self.left.interpret(context) + self.right.interpret(context)

# 使用: 1 + 2
expr = Add(Number(1), Number(2))
print(expr.interpret({}))  # 输出: 3



