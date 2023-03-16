import request from '../utils/httpUtil'

/**
 * 登录
 */
export default{
  fetchLogin(params){
    return request.post('.api/v1/login/',params)
  }
}