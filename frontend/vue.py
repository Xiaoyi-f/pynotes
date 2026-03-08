"""
一、基础使用
1. 创建应用
// main.js
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
2. 模板语法
<template>
    <!-- 插值 -->
    <p>{{ message }}</p>
    <!-- 原始HTML -->
    <div v-html="rawHtml"></div>
    <!-- 属性绑定 -->
    <div :id="dynamicId"></div>
    <button :disabled="isDisabled">按钮</button>
    <!-- 简写 -->
    <div :class="{ active: isActive }"></div>
    <div :style="{ color: activeColor }"></div>
    <!-- 事件绑定 -->
    <button @click="handleClick">点击</button>
    <input @keyup.enter="submit">

    <!-- 双向绑定 -->
    <input v-model="text">
    <input v-model.number="age" type="number">
    <input v-model.trim="text">

    <!-- 条件渲染 -->
    <div v-if="type === 'A'">A</div>
    <div v-else-if="type === 'B'">B</div>
    <div v-else>C</div>
    <!-- 显示/隐藏 -->
    <div v-show="isVisible">显示/隐藏</div>
    <!-- 列表渲染 -->
    <li v-for="(item, index) in items" :key="item.id">
        {{ index }} - {{ item.name }}
    </li>
    <!-- 遍历对象 -->
    <div v-for="(value, key) in object" :key="key">
        {{ key }}: {{ value }}
    </div>
</template>

3. 组件定义
<script setup>
// Composition API (推荐)
import { ref, reactive, computed, watch } from 'vue'

// 响应式数据
const count = ref(0)
const state = reactive({
    name: 'Vue 3',
    version: '3.0'
})

// 计算属性
const fullName = computed({
    // getter
    get() {
        return `${state.name} ${state.version}`
    },
    // setter
    set(newValue) {
        const names = newValue.split(' ')
        state.name = names[0]
        state.version = names[1] || ''
    }
})

// 方法
const increment = () => {
    count.value++
}

// 侦听器
watch(count, (newValue, oldValue) => {
    console.log(`count变化: ${oldValue} -> ${newValue}`)
})

// 立即执行的侦听器
watch(
    () => state.name,
    (newValue) => {
        console.log(`name变化: ${newValue}`)
    },
    { immediate: true }
)

// 侦听多个数据源
watch([count, () => state.name], ([newCount, newName]) => {
    console.log(newCount, newName)
})

// 生命周期
import { onMounted, onUpdated, onUnmounted } from 'vue'

onMounted(() => {
    console.log('组件已挂载')
})

onUnmounted(() => {
    console.log('组件已卸载')
})
</script>
<template>
    <button @click="increment">{{ count }}</button>
    <p>{{ fullName }}</p>
</template>

二、组件通信
1. Props 和 Emits 配置接收，事件传递
<!-- 子组件 Child.vue -->
<script setup>
// 定义props
const props = defineProps({
    title: String,
    count: {
        type: Number,
        default: 0,
        required: true
    }
})

// 定义emits
const emit = defineEmits(['update:count', 'customEvent'])

const handleClick = () => {
    emit('update:count', props.count + 1)
    emit('customEvent', 'data')
}
</script>
<template>
    <h2>{{ title }}</h2>
    <p>Count: {{ count }}</p>
    <button @click="handleClick">增加</button>
</template>
<!-- 父组件 Parent.vue -->
<script setup>
import { ref } from 'vue'
import Child from './Child.vue'

const count = ref(0)

const handleCustomEvent = (data) => {
    console.log('收到数据:', data)
}
</script>
<template>
    <Child
        title="子组件"
        :count="count"
        @update:count="count = $event"
        @custom-event="handleCustomEvent"
    />
</template>

2. Provide/Inject 响应式数据可以修改
<!-- 祖先组件 -->
<script setup>
import { provide, ref } from 'vue'

const theme = ref('dark')

provide('theme', theme)
provide('changeTheme', (newTheme) => {
    theme.value = newTheme // 工厂函数
})
</script>
<!-- 后代组件 -->
<script setup>
import { inject } from 'vue'

const theme = inject('theme')
const changeTheme = inject('changeTheme')
</script>

三、响应式系统
1. ref 和 reactive
import { ref, reactive, toRefs } from 'vue'

// ref: 用于基本类型
const count = ref(0)
console.log(count.value) // 访问值

// reactive: 用于对象
const state = reactive({
    count: 0,
    name: 'Vue'
})

// 解构响应式对象
const { count, name } = toRefs(state)
// 现在 count 和 name 都是 ref

// 浅层响应式
import { shallowRef, shallowReactive } from 'vue'
const shallow = shallowReactive({ nested: { count: 0 } })
// 替换整个对象才会导致响应变化
2. 响应式工具
import { isRef, unref, toRef, markRaw } from 'vue'

// 检查是否是 ref
isRef(count) // true

// 将响应式对象属性转为 ref
const countRef = toRef(state, 'count')

// 标记为不可响应式
const rawObject = markRaw({ nested: {} })
四、计算属性和侦听器
1. 计算属性
import { computed } from 'vue'

// 只读计算属性
const fullName = computed(() => {
    return `${firstName.value} ${lastName.value}`
})

// 可写计算属性
const writableFullName = computed({
    get() {
        return `${firstName.value} ${lastName.value}`
    },
    set(newValue) {
        const [first, last] = newValue.split(' ')
        firstName.value = first
        lastName.value = last
    }
})
2. 侦听器
import { watch, watchEffect } from 'vue'

// 基础侦听
watch(count, (newValue, oldValue) => {
    // 当count变化时执行
})

// 侦听多个源
watch([count, name], ([newCount, newName], [oldCount, oldName]) => {
    // 当任意一个变化时执行
})

// 深度侦听对象
watch(
    () => state.user,
    (newUser) => {
        console.log(newUser)
    },
    { deep: true }
)
五、生命周期
import {
    onBeforeMount,
    onMounted,
    onBeforeUpdate,
    onUpdated,
    onBeforeUnmount,
    onUnmounted,
    onErrorCaptured,
    onActivated,
    onDeactivated
} from 'vue'

onBeforeMount(() => {
    // 挂载前
})

onMounted(() => {
    // 挂载后 - 可以访问DOM
})

onBeforeUpdate(() => {
    // 更新前
})

onUpdated(() => {
    // 更新后
})

onBeforeUnmount(() => {
    // 卸载前
})

onUnmounted(() => {
    // 卸载后 - 清理工作
})

onErrorCaptured((err, instance, info) => {
    // 捕获子组件错误
    return false // 阻止错误继续向上传播
})

// KeepAlive组件特有
onActivated(() => {
    // 激活时
})

onDeactivated(() => {
    // 停用时
})
六、自定义指令
// 全局指令
app.directive('focus', {
    mounted(el) {
        el.focus()
    }
})

// 局部指令
<script setup>
const vMyDirective = {
    mounted(el, binding) {
        // binding.value - 指令的值
        // binding.oldValue - 之前的值（仅在beforeUpdate和updated中可用）
        // binding.arg - 传给指令的参数 指令:参数
        // binding.modifiers - 修饰符对象
    },
    updated(el, binding) {
        // 更新时调用
    },
    beforeUnmount(el) {
        // 卸载前清理
    }
}
</script>
<template>
    <input v-my-directive:arg.modifier="value">
</template>

七、内置组件
1. Transition
<template>
    <button @click="show = !show">切换</button>
    <Transition name="fade">
        <p v-if="show">Hello</p>
    </Transition>
    <!-- 使用CSS -->
    <style>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.5s;
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
    </style>
</template>

2. TransitionGroup
<template>
    <TransitionGroup name="list" tag="ul">
        <li v-for="item in items" :key="item.id">
            {{ item.text }}
        </li>
    </TransitionGroup>
</template>

3. KeepAlive
<template>
    <!-- :include明确缓存对象, exclude排除缓存对象 -->
    <KeepAlive :include="['ComponentA']" :exclude="['ComponentB']" :max="10">
        <component :is="currentComponent" />
    </KeepAlive>
</template>

4. Teleport
<template>
    <button @click="modalOpen = true">打开模态框</button>
    <Teleport to="body">
        <div v-if="modalOpen" class="modal">
            <p>模态框内容</p>
            <button @click="modalOpen = false">关闭</button>
        </div>
    </Teleport>
</template>

5. Suspense
<!-- 父组件 -->
<template>
    <Suspense>
        <template #default>
            <AsyncComponent />
        </template>
        <template #fallback>
            <div>加载中...</div>
        </template>
    </Suspense>
</template>
<!-- 异步组件 -->
<script setup>
const { data } = await fetch('/api/data').then(r => r.json())
</script>

八、组合式函数
// useMouse.js
import { ref, onMounted, onUnmounted } from 'vue'

export function useMouse() {
    const x = ref(0)
    const y = ref(0)

    function update(event) {
        x.value = event.pageX
        y.value = event.pageY
    }

    onMounted(() => window.addEventListener('mousemove', update))
    onUnmounted(() => window.removeEventListener('mousemove', update))

    return { x, y }
}

// 在组件中使用
<script setup>
import { useMouse } from './useMouse'

const { x, y } = useMouse()
</script>
<template>
    <p>鼠标位置: {{ x }}, {{ y }}</p>
</template>

九、TypeScript支持
<script setup lang="ts">
// 类型定义
interface User {
    id: number
    name: string
    age?: number
}

// 带类型的ref
import { ref } from 'vue'
const user = ref<User>({
    id: 1,
    name: '张三'
})

// 带类型的props
const props = defineProps<{
    title: string
    count?: number
    users: User[]
}>()

// 带类型的emits
const emit = defineEmits<{
    (e: 'update:count', value: number): void
    (e: 'select', user: User): void
}>()

// 带类型的computed
import { computed } from 'vue'
const userName = computed<string>(() => user.value.name)

// 带类型的provide/inject
import { provide, inject, InjectionKey } from 'vue'
const key = Symbol() as InjectionKey<string>

provide(key, 'value')
const value = inject(key)
</script>

十、状态管理（Pinia）
// store/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        name: '张三',
        age: 25,
        token: null
    }),

    getters: {
        // 类似计算属性
        isAdult: (state) => state.age >= 18,
        // 使用其他getter
        greeting: (state) => {
            return `Hello, ${state.name}`
        }
    },

    actions: {
        // 同步操作
        updateName(newName) {
            this.name = newName
        },

        // 异步操作
        async login(credentials) {
            const response = await api.login(credentials)
            this.token = response.token
        }
    }
})

// 在组件中使用
<script setup>
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()

// 直接修改状态
userStore.name = '李四'

// 使用action
userStore.updateName('王五')

// 使用getter
console.log(userStore.isAdult)

// 解构并保持响应式
const { name, age } = storeToRefs(userStore)
</script>

十一、路由（Vue Router 4）
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/user/:id',
        name: 'User',
        component: () => import('../views/User.vue'),
        props: true, // 将params作为props传递
        meta: { requiresAuth: true }
    },
    {
        path: '/about',
        component: () => import('../views/About.vue'),
        children: [
            {
                path: 'info',
                component: () => import('../views/AboutInfo.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})
<!-- 在组件中使用 -->
<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 获取路由参数
console.log(route.params.id)
console.log(route.query.search)

// 导航
router.push('/home')
router.push({ name: 'User', params: { id: 1 } })
router.replace('/login')
router.go(-1)

// 编程式导航
const navigate = () => {
    router.push({
        path: '/user',
        query: { search: 'vue' }
    })
}
</script>
<template>
    <!-- 路由链接 -->
    <router-link to="/">首页</router-link>
    <router-link :to="{ name: 'User', params: { id: 1 } }">
        用户
    </router-link>
    <!-- 路由出口 -->
    <router-view />
    <router-view name="sidebar" /> <!-- 命名视图 -->
</template>

十二、实用技巧
1. 动态组件
<script setup>
import { shallowRef } from 'vue'
import Home from './Home.vue'
import About from './About.vue'

const components = {
    Home,
    About
}
const currentComponent = shallowRef(Home)
</script>
<template>
    <component :is="currentComponent" />
    <component :is="components['Home']" />
</template>

2. 自定义 v-model
<!-- 子组件 -->
<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const updateValue = (event) => {
    emit('update:modelValue', event.target.value)
}
</script>
<template>
    <input :value="modelValue" @input="updateValue">
</template>
<!-- 父组件 -->
<template>
    <CustomInput v-model="text" />
    <!-- 相当于 -->
    <CustomInput
        :modelValue="text"
        @update:modelValue="text = $event"
    />
</template>

3. 属性透传
<!-- 父组件 -->
<template>
    <MyButton class="large" @click="handleClick">
        按钮
    </MyButton>
</template>
<!-- 子组件 MyButton.vue -->
<template>
    <button v-bind="$attrs" class="btn">
        <slot />
    </button>
</template>
<script>
// 禁用属性继承
export default {
    inheritAttrs: false
}
</script>

4. 性能优化
// 1. 使用shallowRef/shallowReactive
import { shallowRef } from 'vue'
const largeObject = shallowRef({ /* 大数据 */ })

// 2. 使用v-once
<template>
    <div v-once>{{ staticContent }}</div>
</template>
// 3. 使用v-memo (Vue 3.2+)
<div v-memo="[valueA, valueB]">
    <!-- 仅当valueA或valueB变化时更新 -->
</div>
// 4. 使用异步组件
import { defineAsyncComponent } from 'vue'
const AsyncComp = defineAsyncComponent(() =>
    import('./components/AsyncComponent.vue')
)
5. 防抖与节流
<script setup>
import { ref } from 'vue'
// -es 表示 ES Module 版本
import { debounce, throttle } from 'lodash-es'
import { onBeforeUnmount } from 'vue'

const searchResult = ref([])

// 防抖：输入结束后500ms执行
const handleSearch = debounce((keyword) => {
    console.log('搜索:', keyword)
    // 调用API...
}, 500)

// 节流：滚动时每200ms执行一次
const handleScroll = throttle(() => {
    console.log('滚动位置:', window.scrollY)
}, 200)

// 组件卸载时取消防抖/节流
onBeforeUnmount(() => {
    handleSearch.cancel() // 取消防抖
    handleScroll.cancel() // 取消节流
})
</script>
<template>
    <input @input="handleSearch($event.target.value)" placeholder="搜索" />
    <div @scroll="handleScroll">滚动区域</div>
</template>

6. 完整Props/Emits示例
<!-- 子组件 -->
<template>
    <div class="counter">
        <button @click="handleDecrease">-</button>
        <span>{{ count }}</span>
        <button @click="handleIncrease">+</button>
    </div>
</template>
<script setup>
// 1. 定义 props
const props = defineProps({
    count: {
        type: Number,
        required: true
    },
    min: {
        type: Number,
        default: 0
    },
    max: {
        type: Number,
        default: 100
    }
})

// 2. 定义 emits
const emit = defineEmits(['update:count', 'over-limit'])

// 3. 内部方法只负责发通知
const handleIncrease = () => {
    if (props.count < props.max) {
        // 正常情况：请求父组件增加
        emit('update:count', props.count + 1)
    } else {
        // 超出限制：发送特殊通知
        emit('over-limit', '已达到最大值')
    }
}

const handleDecrease = () => {
    if (props.count > props.min) {
        emit('update:count', props.count - 1)
    } else {
        emit('over-limit', '已达到最小值')
    }
}
</script>
<!-- 父组件 -->
<template>
    <Counter
        :count="pageCount"
        :min="5"
        :max="20"
        @update:count="pageCount = $event"
        @over-limit="handleShowWarning"
    />
</template>
<script setup>
import { ref } from 'vue'

const pageCount = ref(10)

const handleShowWarning = (msg) => {
    alert(msg) // 或使用 UI 组件显示提示
}
</script>

十三、插槽（Slots）
1. 基础插槽
<!-- 子组件 -->
<template>
    <div class="card">
        <slot></slot>  <!-- 父组件内容渲染在这里 -->
    </div>
</template>
<!-- 父组件 -->
<Child>
    <p>这是内容</p>
</Child>

2. 具名插槽
<!-- 子组件 Layout.vue -->
<template>
    <header><slot name="header"></slot></header>
    <main><slot></slot></main>  <!-- 默认插槽 -->
    <footer><slot name="footer"></slot></footer>
</template>
<!-- 父组件 -->
<Layout>
    <template #header>标题</template>
    <p>主要内容</p>
    <template #footer>版权</template>
</Layout>

3. 作用域插槽
<!-- 子组件：向父组件传递数据 -->
<template>
    <div v-for="user in users" :key="user.id">
        <slot :user="user" :index="index">{{ user.name }}</slot>
    </div>
</template>
<!-- 父组件：接收数据自定义渲染 -->
<Child>
    <template #default="{ user, index }">
        <span>{{ index }} - {{ user.name }} ({{ user.age }}岁)</span>
    </template>
</Child>

4. 动态插槽名
<template>
    <BaseLayout>
        <template #[dynamicSlotName]>动态内容</template>
    </BaseLayout>
</template>
<script setup>
const dynamicSlotName = ref('header')
</script>

十四、渲染函数 & JSX
1. h函数（渲染函数）
import { h, ref } from 'vue'

export default {
    setup() {
        const count = ref(0)

        // 返回渲染函数
        return () => h('div', { class: 'container' }, [
            h('p', `计数: ${count.value}`),
            h('button', {
                onClick: () => count.value++
            }, '增加')
        ])
    }
}
2. h函数参数详解
h(标签, 属性, 子节点)

// 示例
h('div', { id: 'app', class: 'box' }, '文本')
h('div', { style: { color: 'red' } }, [h('span'), '文本'])

// 组件
import Child from './Child.vue'
h(Child, { title: '标题', @click: handleClick })
3. JSX语法（需插件）
// Counter.jsx
import { ref } from 'vue'

export default {
    setup() {
        const count = ref(0)

        return () => (
            <div>
                <p>计数: {count.value}</p>
                <button onClick={() => count.value++}>增加</button>
            </div>
        )
    }
}
4. 渲染函数 vs 模板
// 模板写法
<template>
    <div v-if="show" @click="handleClick">内容</div>
</template>
// 渲染函数写法
() => show.value && h('div', { onClick: handleClick }, '内容')
快速记忆要点
● 组合式API是核心 - ref(), reactive(), computed(), watch()
● <script setup> 简化代码 - 自动导出，无需return
● TypeScript友好 - 完整的类型支持
● 响应式系统改进 - 更精确的依赖追踪
● 更小的包体积 - Tree-shaking支持更好
● 更好的性能 - 更快的渲染速度和内存使用
● 新的内置组件 - Teleport, Suspense
● 多个根节点 - Fragment支持
"""
