HTTP协议基本方法:
get -> 明文发送数据/请求
post -> 密文发送数据/请求
put -> 请求全量更新数据
patch -> 请求部分更新数据
delete -> 请求删除资源

# get写法1
axios.get('/api/users?id=xx&&name=xx')
  .then(res => console.log(res.data, res.status))
  .catch(err => console.error(err))

# get写法2
axios.get('/api/users', {
  params: {
    id: xx,
    name: xx
  }
})
.then(res => console.log(res.data, res.status))
.catch(err => console.error(err))

# get写法3
async function getUsers() {
  try {
    const res = await axios.get('/api/users', {
      params: { id: xx, name: xx }
    })
    console.log(res.data, res.status)
  } catch (err) {
    console.error('请求失败', err)
  }
}


# post写法1
axios.post('/api/users', {
  name: xx,
  id: xx
})
.then(res => console.log(res.data, res.status))
.catch(err => console.error(err))

# post写法2
axios.post('/api/users', {
  try {
    const res = await axios.post('/api/users', {
      name: xx,
      id: xx
    })
    console.log(res.data, res.status)
  } catch (err) {
    console.error(err)
  }
})

# put -> 没设置传送的部分默认传undefined
axios.put('/api/users/1', {
  id: xx,
  name: xx
})

# patch
axios.patch('/api/users/1', {
  id: xx
})

# delete，无参
axios.delete('/api/users/1')

# delete，有参
axios.delete('/api/users', {
  params: {
    id: xx
  }
})

{
  服务器返回的数据（最常用）
  data: { },

  HTTP 状态码
  status: 200,

  状态文本
  statusText: 'OK',

  响应头
  headers: { },

  请求配置
  config: { },

  请求对象
  request: { } }

# 建议创建实例进行配置再使用 -> 某些数据可以使用.env环境变量管理传递
const request = axios.create({
  // 设置baseURL
  baseURL: xx,
  // 设置超时限制ms
  timeout: 10000,
  // 配置默认请求头
  headers: {
    'Content-Type': 'application/json'
  }
})

# Axios请求拦截器，在每个请求发送之前自动执行，用于统一处理请求的预处理工作 -> Bearer持有者 token令牌
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // showLoading() -> 自定义函数 -> 显示加载动画

    return config
  },
  // 配置发生错误触发
  err => {
    return Promise.reject(err) // 返回一个错误的Promise对象，并且传递给下一个catch处理
  }
)

# 响应拦截器，拦截所有从服务器返回的响应，在 then 或 catch 收到之前进行统一处理 -> code/message由后端定义
request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code == 200) {
      return res.data
    } else {
      // 弹出错误提示框
      // ElMessage是element-plus组件的某插件
      ElMessage.error(res.message || '请求失败')
      if (res.code === 401) {
        localStorage.removeItem('token')
        router.push('/login')
      }
      return Promise.reject(new Error(res.message))
    }
  },
  err => {
    let message = '请求失败'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          message = '未登录或登录已过期'
          // 跳转登录
          break
        case 403:
          message = '没有权限'
          break
        case 404:
          message = '请求资源不存在'
          break
        case 500:
          message = '服务器错误'
          break
        default:
          message = `连接失败(${error.response.status})`
      }
    } else if (error.code === 'ECONNABORTED') {           // ECONNABORTED = Connection Aborted（连接被中止/中断）
      message = '请求超时'
    } else if (!navigator.onLine) {
      message = '网络已断开'
    }

    ElMessage.error(message)

    return Promise.reject(error)
  }
)

# 必知状态码:
  200 OK
  401 Unauthorized
  403 Forbidden
  404 Not Found
  500 Internal Server Error

