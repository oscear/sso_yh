import axios from "axios"
import auth from "./auth"
// import  config from "../../public/config"



let backURL
backURL = window.VUE_APP_URL.backURL
// const BASE_URL = config.VUE_SERVER_URL_187
// const BASE_URL = backURLl


class Http {
  constructor() {
    this.http = axios.create({
      baseURL: backURL,
      timeout:100000
    })

    // 设置拦截器，用来添加JWT Token的
    this.http.interceptors.request.use(config => {
      const token = sessionStorage.getItem("token");
      if (token && token != 'undefined') {
        config.headers.common.Authorization = "Token " + token
      }
      return config
    },error =>{
      return Promise.reject(error)
    })

    // 设置拦截器，如果返回403，跳转到登陆页面
    // 403是没有权限访问这个接口
    this.http.interceptors.response.use(null, err => {
      if (err && err.response && err.response.status == 403) {
        auth.clearUserToken()
      }else if(err && err.response && err.response.status == 400){
        return Promise.reject(err.response);
      }
      return Promise.reject(err);
    })
  }
  getUser(uuid) {
    const url = "/api/v1/register/" + uuid + "/"
    return this.http.get(url)
  }

  editUser(user_id,params){
    const url = "api/v1/register/"+ user_id +"/"
    return this.http.put(url,params)
  }

  register(params) {
    const url = "/api/v1/register/"
    return this.http.post(url, params)
  }

  login(params) {
    const url = "/api/v1/login/"
    return this.http.post(url, params)
  }

  getHost(){
    const url = "/api/v1/host/"
    return this.http.get(url)
  }

  addHost(params){
    const url = "/api/v1/host/"
    return this.http.post(url,params)
  }

  editHost(host_id,params){
    const url = "api/v1/host/"+ host_id +"/"
    return this.http.put(url,params)
  }

  delHost(host_id){
    const url = "/api/v1/host/" + host_id + "/"
    return this.http.delete(url)
  }

  getModule(){
    const url = "/api/v1/module/"
    return this.http.get(url)
  }
  addModulet(params){
    const url = "/api/v1/module/"
    return this.http.post(url,params)
  }

  editModule(host_id,params){
    const url = "api/v1/module/"+ host_id +"/"
    return this.http.put(url,params)
  }

  delModule(host_id){
    const url = "/api/v1/module/" + host_id + "/"
    return this.http.delete(url)
  }

  getReport(version, testsuite){
    const url ="/api/v1/report/?version="+ version + "&testsuite=" + testsuite
    return this.http.get(url)
  }
  replaceExp(params){
    const url = "/api/v1/report/"
    return this.http.post(url,params)
  }

  SvnUpdate(params){
    const url = "api/v1/checkLocalSVN/"
    return this.http.post(url,params)
  }

  // 查询本地文件状态
  showDetail(version,testsuite){
    const url = "api/v1/checkLocalSVN/?version="+ version + "&testsuite=" + testsuite
    return this.http.get(url)
  }

  SvnCommit(params){
    const url = "api/v1/SvnCommit/"
    return this.http.post(url,params)
  }

  getXML(sheetname){
    const url = "/api/v1/AvatarUpload/?sheetname=" + sheetname
    return this.http.get(url)
  }

}



export default new Http()