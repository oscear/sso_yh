import axios from 'axios'
// import  config from "../../public/config"


import {
  Message,
  Loading
} from 'element-ui'
import router from '../router/index.js'  //注意路径与文件名


let backURL
backURL = window.VUE_APP_URL.backURL  //取自pubilc/conf.js


const service = axios.create({
  baseURL: backURL, // api 的 base_url
  timeout: 50000 // request timeout
})

let loading // 定义loading变量

function startLoading () { // 使用Element loading-start 方法
  loading = Loading.service({
    lock: true,
    text: '加载中...',
    background: 'rgba(0, 0, 0, 0.7)'
  })
}

function endLoading () { // 使用Element loading-close 方法
  loading.close()
}

// 请求拦截  设置统一header
service.interceptors.request.use(
  config => {
    // 加载
    startLoading()
    if (sessionStorage.eleToken) {
      config.headers.Authorization = sessionStorage.eleToken
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截  401 token过期处理
service.interceptors.response.use(
  response => {
    endLoading()
    return response
  },
  error => {
    // 错误提醒
    endLoading()
    Message.error(error.response.data)

    const { status } = error.response
    if (status === 401) {
      Message.error('token值无效，请重新登录')
      // 清除token
      sessionStorage.removeItem('eleToken')

      // 页面跳转
      router.push('/login')
    }

    return Promise.reject(error)
  }
)

export default service
