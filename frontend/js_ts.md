# 1.JS基础:
基本数据类型:
Boolean
Number
String -> .length
Undefined
Null
// 实际使用都小写就好

高级数据类型:
Array -> .length -> 可读写,修改关联变容 (empty * n)
Object

特殊类型:
NaN -> isNaN()
Infinity

基本关联与组成:
渲染引擎 -> blink/webkit...
JS引擎 -> v8/node...
ECMAScript BOM DOM

/* JS是动态类型语言，只需要声明变量 -> let const */
视口交互:
prompt()
alert()
console.log()
console.error()

/* 外部js文件建议多写单引号，内部写双引号 */
基本语法:
async await
// 事件循环
// 宏任务 / 微任务

try catch finally
[] 元组
{} 对象

Object.keys()
Object.values()
Object.entries()

`${exp}`
typeof
?. 可选链
instanceof
+ - * / %
>> << ~ ^ & |
++
--
===
&& || ！
? :
<算术运算符>=


分支与循环:
if () {
} else if () {
} else {
}

switch () {
    case value: break;
    default:
}

for (初始变量; 条件; 操作) {}

while () {}
do {} while ()

函数:
function name() {}
arguments -> 函数内置伪数组，可遍历，存函数参数 .length
(args) => {} 箭头函数 -> 无this
...参数 -> 剩余参数
...还可以作为展开对象符

对象:
键只能是字符串，js可以自动省略识别字符串
[key] key是一个变量 -> 动态键

类 -> 创建对象:
class Demo extends Object {
    constructor(arg) {
        this.arg = arg
    }

    static var = 'var'

    static func() {
    // pass
}

    get info() {
    return xx
    }

    set info() {
    // 修改逻辑
    }
}

定时器
targetTimeout = setTimeout(() => {
}, time)

targetInterval = setInterval(() => {
}, time)

clearTimeout(targetTimeout)
clearInterval(targetInterval)

深克隆:
import cloneDeep from 'lodash/cloneDeep'
const cloned = cloneDeep(obj)

节点操作:
document.createElement(tag)
document.querySelector(tag) as HTMLXxxElement
document.querySelectorAll()
parent.appendChild()
parent.insertBefore(newElement, referenceElement)
element.remove()
obj.style.xxx -> 连字符全改写为小驼峰
obj.innerHTML
obj.textContent 性能好
obj.attr

事件回调:
obj.addEventListener(eventType, (event) => {})
event.target -> 触发这个事件的对象
event.key -> 按键
event.preventDefault()
event.stopPropagation()
event.button -> 0左键 1中键 2右键

localStorage和sessionStorage:
// 增/改
localStorage.setItem('key', 'value')
sessionStorage.setItem('key', 'value')

// 删
localStorage.removeItem('key')
localStorage.clear()      // 全删

// 查
localStorage.getItem('key')     // 没有则返回 null
sessionStorage.getItem('key')   // 没有则返回 null

// 遍历
Object.keys(localStorage)
Object.keys(sessionStorage)

// 存对象
const demo = { key: 'value' }
localStorage.setItem('demo', JSON.stringify(demo))

// 取
const demoStr = localStorage.getItem('demo')
const demoObj = JSON.parse(demoStr)

设置Cookie:
document.cookie = "key=value"
// 建议JS只设置非敏感简单Cookie -> 指定好URL

高级方法:
.map(args => {})
.forEach(args => {})
.filter(args => {})

# 2.高级概念:
防抖：在事件被触发后，等待一段时间再执行函数，如果在这段时间内再次触发，则重新计时
防抖生活类比
● 电梯例子：电梯门打开后，如果有人不断进来，电梯就一直等待。只有当最后一个人进来后，等待一段时间没人再进，电梯才关门运行
● 搜索框：用户打字时不要立即搜索，等用户停止输入后再搜索

节流：在一定时间间隔内，函数最多只执行一次，无论触发多少次，都保证在指定时间间隔内执行一次
节流生活类比
● 游戏技能：技能释放后有冷却时间，冷却期间不能再次释放
● 公交车：公交车每10分钟一班，无论站台有多少人，都按时发车
守卫：在快级代码运行前后进行系列操作，守护程序的良好运行

3.TS注解:
string
number
boolean
undefined
null
any 任意类型
void 一般用于函数，表示无返回值
[number, ...string]
<T extends string> 泛型占位 -> 在块头声明 -> 之后可使用T -> U也是泛型占位符
? 可选
type 定义注解类型
interface 定义接口类/对象 -> (args) 函数/方法接口
public
private
protected -> 类/子类可访问
readonly
abstract 定义抽象类/抽象方法
& 交叉类型
| 联合类型
declare 声明变量是存在的

# 4.基本事件
| 事件 | 触发时机 | 常用场景 |
|------|----------|----------|
| `click` | 鼠标点击完成 | 按钮、链接交互 |
| `input` | 输入框值实时变化 | 搜索框、表单验证 |
| `submit` | 表单提交 | 表单提交拦截 |
| `keydown` | 键盘按下 | 快捷键、回车提交 |
| `scroll` | 滚动 | 无限滚动、懒加载 |
| `load` | 所有资源加载完成 | 页面初始化 |
| `change` | 表单值改变+失焦 | 下拉框、复选框 |
| `resize` | 窗口大小改变 | 响应式适配 |
| `focus` | 获得焦点 | 输入框高亮 |
| `blur` | 失去焦点 | 输入框验证 |
| `mouseenter` | 鼠标进入元素 | 悬浮效果 |
| `mouseleave` | 鼠标离开元素 | 悬浮消失 |
| `error` | 资源加载失败 | 图片降级处理 |
| `contextmenu` | 右键菜单 | 自定义右键 |
| `dblclick` | 双击 | 编辑、放大 |
| `beforeunload` | 离开页面确认 | 草稿保存 |
| `online` | 网络连接 | 恢复联网提示 |
| `offline` | 网络断开 | 离线提示 |


