一句话：UniApp = Vue3 + 微信小程序 + 多端编译，一套代码发布 iOS、Android、H5、小程序

一、核心认知
1.1 UniApp 到底是什么？
// 正确理解
UniApp = 
    Vue3语法（你已会） + 
    微信小程序组件/API（新概念） + 
    多端编译引擎（黑盒）

// 错误理解
UniApp != 单纯的Vue
UniApp != 单纯的微信小程序
UniApp = 两者杂交 + 跨端魔法
1.2 开发前必须知道的三件事
// 1. 没有DOM！没有DOM！没有DOM！
document.getElementById('app')  // 报错！
window.addEventListener        // 报错！
localStorage                  // H5可用，App/小程序不可用！

// 2. CSS 是部分支持的
* {
    margin: 0;    // 支持
    padding: 0;   // 支持
}
:hover { }      // 移动端不支持
position: fixed // 注意兼容性

// 3. 标签是微信小程序的，不是HTML
<div>     // 报错！
<span>    // 报错！
<p>       // 报错！

<view>    // div 的替代品
<text>    // span 的替代品
<image>   // img 的替代品

二、环境搭建
2.1 安装 HBuilderX（官方IDE）
1. 官网下载 HBuilderX
2. 安装后打开
3. 工具 -> 插件安装 -> 安装 uni-app (Vue3) 编译器
2.2 创建项目
# 方式1：HBuilderX 可视化创建
文件 -> 新建 -> 项目 -> uni-app
选择：Vue3 + Vite + TypeScript（推荐）

# 方式2：命令行（如果你习惯）
npm create vue@latest
# 然后手动安装 uni-app 依赖（不推荐新手）
2.3 项目结构
my-project/
├── src/
│   ├── pages/          # 页面文件夹（重要！）
│   │   └── index/
│   │       ├── index.vue    # 首页
│   │       └── index.scss
│   ├── components/     # 公共组件
│   ├── uni_modules/    # 插件市场下载的插件
│   ├── static/         # 静态资源（图片等）
│   ├── store/          # Pinia/Vuex
│   ├── App.vue         # 根组件（全局配置）
│   └── main.js         # 入口文件
├── manifest.json       # 应用配置（应用名称、图标等）
├── pages.json          # 页面配置（路由、导航栏）
└── uni.scss           # 全局样式变量

三、页面与路由
3.1 pages.json - 页面配置（类似路由表）
{
    "pages": [
        {
            "path": "pages/index/index",     // 首页
            "style": {
                "navigationBarTitleText": "首页",
                "navigationBarBackgroundColor": "#007AFF",
                "enablePullDownRefresh": true  // 允许下拉刷新
            }
        },
        {
            "path": "pages/user/user",
            "style": {
                "navigationBarTitleText": "我的"
            }
        },
        {
            "path": "pages/detail/detail",
            "style": {
                "navigationBarTitleText": "详情"
            }
        }
    ],
    "globalStyle": {
        "navigationBarTextStyle": "white",
        "navigationBarTitleText": "UniApp",
        "navigationBarBackgroundColor": "#007AFF",
        "backgroundColor": "#F5F5F5"
    },
    "tabBar": {
        "color": "#999",
        "selectedColor": "#007AFF",
        "list": [
            {
                "pagePath": "pages/index/index",
                "text": "首页",
                "iconPath": "static/tab/home.png",
                "selectedIconPath": "static/tab/home-active.png"
            },
            {
                "pagePath": "pages/user/user",
                "text": "我的",
                "iconPath": "static/tab/user.png",
                "selectedIconPath": "static/tab/user-active.png"
            }
        ]
    }
}
3.2 页面跳转
// 1. 保留当前页面，跳转到新页面（最常用）
uni.navigateTo({
    url: '/pages/detail/detail?id=123'
})

// 2. 关闭当前页面，跳转到新页面
uni.redirectTo({
    url: '/pages/login/login'
})

// 3. 关闭所有页面，打开应用内某个页面
uni.reLaunch({
    url: '/pages/index/index'
})

// 4. 跳转到 tabBar 页面（底部导航）
uni.switchTab({
    url: '/pages/user/user'
})

// 5. 返回上一页
uni.navigateBack({
    delta: 1  // 返回层级，1=上一页
})

// 获取页面参数（在详情页）
onLoad(options) {
    console.log(options.id)  // 123
}
3.3 页面生命周期
<script setup>
import { onLoad, onShow, onHide, onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'

// 页面加载（只一次，可获取参数）
onLoad((options) => {
    console.log('页面加载', options.id)
})

// 页面显示（每次进入）
onShow(() => {
    console.log('页面显示')
})

// 页面隐藏
onHide(() => {
    console.log('页面隐藏')
})

// 下拉刷新（需在pages.json开启）
onPullDownRefresh(() => {
    console.log('下拉刷新')
    setTimeout(() => {
        uni.stopPullDownRefresh()  // 停止刷新
    }, 1000)
})

// 上拉加载更多（触底）
onReachBottom(() => {
    console.log('触底了，加载更多')
})

// 页面滚动
onPageScroll((e) => {
    console.log('滚动距离：', e.scrollTop)
})
</script>


四、组件系统
4.1 基础组件
<template>
    <view class="container">
        <!-- view = div -->
        <view class="card">
            <!-- text = span/p -->
            <text class="title">标题</text>
            
            <!-- image = img -->
            <image 
                src="/static/logo.png"
                mode="aspectFit"
                @click="handleClick"
            />
            
            <!-- scroll-view 可滚动区域 -->
            <scroll-view scroll-y class="list">
                <view v-for="item in list" :key="item.id">
                    {{ item.name }}
                </view>
            </scroll-view>
            
            <!-- 按钮 -->
            <button 
                type="primary"
                size="default"
                :loading="loading"
                @click="submit"
            >
                提交
            </button>
            
            <!-- 输入框 -->
            <input 
                v-model="username"
                type="text"
                placeholder="请输入用户名"
                @input="handleInput"
            />
            
            <!-- 单选/复选框 -->
            <checkbox-group @change="checkboxChange">
                <label v-for="item in items" :key="item.value">
                    <checkbox :value="item.value" :checked="item.checked" />
                    {{ item.name }}
                </label>
            </checkbox-group>
            
            <!-- 开关 -->
            <switch :checked="checked" @change="switchChange" />
        </view>
    </view>
</template>

4.2 条件渲染（跨端适配）
<template>
    <!-- #ifdef = 仅在某个平台编译 -->
    <!-- #ifdef MP-WEIXIN -->
    <view>只在微信小程序显示</view>
    <!-- #endif -->
    
    <!-- #ifdef APP-PLUS -->
    <view>只在App显示</view>
    <!-- #endif -->
    
    <!-- #ifdef H5 -->
    <view>只在H5显示</view>
    <!-- #endif -->
    
    <!-- #ifndef = 除了某个平台都显示 -->
    <!-- #ifndef MP-WEIXIN -->
    <view>除了微信小程序都显示</view>
    <!-- #endif -->
</template>


五、API 调用（替代 Web API）
5.1 网络请求（封装 axios 风格）
// utils/request.js
export const request = (options) => {
    return new Promise((resolve, reject) => {
        uni.request({
            url: 'https://api.example.com' + options.url,
            method: options.method || 'GET',
            data: options.data,
            header: {
                'Content-Type': 'application/json',
                'Authorization': uni.getStorageSync('token')
            },
            success: (res) => {
                if (res.statusCode === 200) {
                    resolve(res.data)
                } else {
                    reject(res)
                }
            },
            fail: (err) => {
                reject(err)
            }
        })
    })
}

// 使用
async function getUser() {
    uni.showLoading({ title: '加载中' })
    try {
        const data = await request({
            url: '/user/info',
            method: 'GET'
        })
        userInfo.value = data
    } catch (error) {
        uni.showToast({
            title: '请求失败',
            icon: 'error'
        })
    } finally {
        uni.hideLoading()
    }
}
5.2 数据存储（替代 localStorage）
// 同步存储
uni.setStorageSync('token', 'abc123')
const token = uni.getStorageSync('token')
uni.removeStorageSync('token')
uni.clearStorageSync()

// 异步存储（推荐）
await uni.setStorage({ key: 'token', data: 'abc123' })
const { data } = await uni.getStorage({ key: 'token' })
await uni.removeStorage({ key: 'token' })
await uni.clearStorage()
5.3 路由跳转
// 已在第三部分详细说明
5.4 弹窗提示
// 轻提示（2秒消失）
uni.showToast({
    title: '操作成功',
    icon: 'success',  // success / error / none / loading
    duration: 2000
})

// 模态对话框
uni.showModal({
    title: '提示',
    content: '确定要删除吗？',
    success: (res) => {
        if (res.confirm) {
            console.log('用户点击确定')
        }
    }
})

// 加载中
uni.showLoading({
    title: '加载中...',
    mask: true  // 防止触摸穿透
})
uni.hideLoading()
5.5 设备信息
// 系统信息
const systemInfo = uni.getSystemInfoSync()
console.log(systemInfo.platform)      // 'ios' / 'android' / 'devtools'
console.log(systemInfo.windowWidth)   // 屏幕宽度
console.log(systemInfo.windowHeight)  // 屏幕高度

// 网络状态
uni.getNetworkType({
    success: (res) => {
        console.log(res.networkType)  // wifi / 4g / none
    }
})

六、实战：完整增删改查页面
6.1 列表页（pages/list/list.vue）
<template>
    <view class="list">
        <!-- 搜索框 -->
        <view class="search-box">
            <input 
                v-model="keyword"
                placeholder="搜索商品"
                @confirm="handleSearch"
            />
        </view>
        
        <!-- 商品列表 -->
        <scroll-view 
            scroll-y 
            class="list-content"
            @scrolltolower="loadMore"
            :lower-threshold="50"
        >
            <view 
                v-for="item in list" 
                :key="item.id"
                class="list-item"
                @click="goDetail(item.id)"
            >
                <image :src="item.image" mode="aspectFill" />
                <view class="info">
                    <text class="name">{{ item.name }}</text>
                    <text class="price">¥{{ item.price }}</text>
                </view>
                <button 
                    size="mini"
                    type="warn"
                    @click.stop="deleteItem(item)"
                >
                    删除
                </button>
            </view>
            
            <!-- 加载更多 -->
            <view class="loading-more">
                <text v-if="hasMore">加载更多...</text>
                <text v-else>没有更多了</text>
            </view>
        </scroll-view>
    </view>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { onPullDownRefresh, onReachBottom } from '@dcloudio/uni-app'

// 数据
const list = ref([])
const keyword = ref('')
const page = ref(1)
const hasMore = ref(true)

// 获取列表
async function fetchList() {
    uni.showLoading({ title: '加载中' })
    try {
        const res = await request({
            url: '/products',
            data: {
                page: page.value,
                keyword: keyword.value
            }
        })
        
        if (page.value === 1) {
            list.value = res.data
        } else {
            list.value = [...list.value, ...res.data]
        }
        
        hasMore.value = res.data.length === 10
    } catch (error) {
        uni.showToast({ title: '加载失败', icon: 'error' })
    } finally {
        uni.hideLoading()
    }
}

// 搜索
function handleSearch() {
    page.value = 1
    fetchList()
}

// 加载更多
function loadMore() {
    if (hasMore.value) {
        page.value++
        fetchList()
    }
}

// 下拉刷新
onPullDownRefresh(() => {
    page.value = 1
    fetchList().finally(() => {
        uni.stopPullDownRefresh()
    })
})

// 上拉加载
onReachBottom(() => {
    loadMore()
})

// 删除
function deleteItem(item) {
    uni.showModal({
        title: '提示',
        content: `确定要删除${item.name}吗？`,
        success: async (res) => {
            if (res.confirm) {
                try {
                    await request({
                        url: `/products/${item.id}`,
                        method: 'DELETE'
                    })
                    uni.showToast({ title: '删除成功' })
                    list.value = list.value.filter(i => i.id !== item.id)
                } catch (error) {
                    uni.showToast({ title: '删除失败', icon: 'error' })
                }
            }
        }
    })
}

// 跳转详情
function goDetail(id) {
    uni.navigateTo({
        url: `/pages/detail/detail?id=${id}`
    })
}

onMounted(() => {
    fetchList()
})
</script>
<style lang="scss">
.list {
    height: 100vh;
    background: #f5f5f5;
    
    .search-box {
        padding: 20rpx;
        background: #fff;
        
        input {
            height: 80rpx;
            background: #f5f5f5;
            border-radius: 40rpx;
            padding: 0 30rpx;
            font-size: 28rpx;
        }
    }
    
    .list-content {
        height: calc(100vh - 120rpx);
        
        .list-item {
            display: flex;
            align-items: center;
            padding: 20rpx;
            background: #fff;
            margin-bottom: 2rpx;
            
            image {
                width: 120rpx;
                height: 120rpx;
                border-radius: 12rpx;
                margin-right: 20rpx;
            }
            
            .info {
                flex: 1;
                display: flex;
                flex-direction: column;
                
                .name {
                    font-size: 28rpx;
                    margin-bottom: 16rpx;
                }
                
                .price {
                    font-size: 32rpx;
                    color: #ff5500;
                    font-weight: bold;
                }
            }
            
            button {
                margin-left: 20rpx;
            }
        }
    }
    
    .loading-more {
        text-align: center;
        padding: 30rpx;
        color: #999;
        font-size: 26rpx;
    }
}
</style>

6.2 详情页（pages/detail/detail.vue）
<template>
    <view class="detail">
        <!-- 商品图片 -->
        <swiper 
            class="banner"
            indicator-dots
            autoplay
            circular
        >
            <swiper-item v-for="img in detail.images" :key="img">
                <image :src="img" mode="aspectFill" />
            </swiper-item>
        </swiper>
        
        <!-- 商品信息 -->
        <view class="info">
            <text class="name">{{ detail.name }}</text>
            <text class="price">¥{{ detail.price }}</text>
            <text class="desc">{{ detail.description }}</text>
        </view>
        
        <!-- 底部操作栏 -->
        <view class="footer">
            <button 
                type="default"
                @click="addToCart"
            >
                加入购物车
            </button>
            <button 
                type="primary"
                @click="buyNow"
            >
                立即购买
            </button>
        </view>
    </view>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const id = ref('')
const detail = ref({})

// 获取页面参数
onLoad((options) => {
    id.value = options.id
    fetchDetail()
})

async function fetchDetail() {
    try {
        const data = await request({
            url: `/products/${id.value}`
        })
        detail.value = data
    } catch (error) {
        uni.showToast({
            title: '加载失败',
            icon: 'error'
        })
    }
}

function addToCart() {
    // 添加到购物车逻辑
    uni.showToast({
        title: '已加入购物车',
        icon: 'success'
    })
}

function buyNow() {
    // 立即购买
    uni.navigateTo({
        url: `/pages/order/confirm?id=${id.value}`
    })
}
</script>


七、发布与调试
7.1 运行到各种平台
# HBuilderX 顶部菜单
运行 -> 运行到浏览器 -> Chrome     # H5
运行 -> 运行到手机或模拟器          # App
运行 -> 运行到小程序模拟器          # 微信开发者工具

# 需要先安装对应环境
H5: 无需额外安装
App: 需要 Android Studio / Xcode
小程序: 需要微信开发者工具
7.2 发行打包
# H5
发行 -> 网站-H5手机版

# App
发行 -> 原生App-云打包

# 小程序
发行 -> 小程序-微信
7.3 常用调试技巧
// 1. console.log 依然可用
console.log('调试信息', data)

// 2. H5端打开控制台
// Chrome DevTools

// 3. 小程序调试
// 微信开发者工具

// 4. App调试
// 真机运行 + console.log

// 5. 条件编译调试
// #ifdef H5
debugger
// #endif

八、常见问题（避坑指南）
错误1：用了DOM API
// 报错！小程序没有window/document
window.localStorage.setItem('token', '123')  
document.querySelector('.box')

// 改
uni.setStorageSync('token', '123')
// 或者用 ref 操作视图
const box = ref(null)
错误2：用了HTML标签
<!-- 报错！不识别div/span/p -->
<div class="box"></div>
<!-- 改 -->
<view class="box"></view>

错误3：CSS 用了通配符
/* 性能极差，某些平台不支持 */
* {
    margin: 0;
    padding: 0;
}

/* 改 */
page, view, text {
    margin: 0;
    padding: 0;
}
错误4：图片路径写错
<!-- 可能加载失败 -->
<image src="./logo.png" />

<!-- 改：/static 开头 -->
<image src="/static/logo.png" />
错误5：忘了处理异步
// 没加 await，拿不到数据
onLoad(() => {
    fetchData()  // 异步没处理
})

// 改
onLoad(async () => {
    await fetchData()
})

九、总结
必会清单
1. pages.json 配置页面和tabBar
2. 5种跳转方法：navigateTo, redirectTo, reLaunch, switchTab, navigateBack
3. 3个生命周期：onLoad, onShow, onHide
4. 3个基础标签：view, text, image
5. 2个存储方法：setStorageSync, getStorageSync
6. 2个弹窗：showToast, showModal
7. 1个请求：uni.request


