import axios from 'axios';
import router from '../router';
import { Loading } from 'element-ui';
// 全局axios请求loading加载
let options = {
	lock: true,
	text: '',
	spinner: 'el-icon-loading',
	background: 'rgba(0, 0, 0, 0.7)'
},
	loadingPage

// const BASE_URL = "http://175.24.95.198:8099/"
const BASE_URL = "http://192.168.0.254:7081/"
let headers = {
	Accept: 'application/json;charset=utf-8',
	'Content-Type': 'application/json;charset=utf-8'
}
// axios配置参数-使用axios不要设置defaults参数配置，默认配置不要改，不方便后续使用
const instance = axios.create({
  baseURL:BASE_URL,
  timeout:10000,
  headers,
})
// axios.defaults.baseUrl = BASE_URL
// axios.defaults.headers = headers
// axios.defaults.timeout = 5000

// 请求拦截器
axios.interceptors.request.use(config => {
	config.withCredentials = true
	let token = sessionStorage.getItem("token")

	if (token) {
		config.headers.common.Authorization = "Token " + token
	} else {
		router.push("/login")
	}
	if (config.method === 'get') {
		config.params = {
			t: Date.parse(new Date()) / 1000,
			...config.params
		}
	}
	loadingPage = Loading.service(options);
	return config
},
	error => {
		loadingPage.close()
		return Promise.reject(error)
	}
)

//  响应拦截器
axios.interceptors.response.use(response => {
	loadingPage.close()
	if (response.data.code === 200) {
		return response.data
	}
	return response.data
},
	error => {
		loadingPage.close()
		if (error && error.response && error.response.status == 403) {
      sessionStorage.removeItem("token")
			router.push('/login')
		}
    return Promise.reject(error);
	}
)

export default instance