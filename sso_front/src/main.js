import Vue from 'vue'
import App from './App.vue'
import './assets/css/main.css'
import ElementUI from 'element-ui'
import router from './router'
// import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
import './assets/theme/index.css' // 自定义主题
import VeLine from 'v-charts/lib/line.common' //折线图
import VeBar from 'v-charts/lib/bar.common' // 条形图
import VeHistogram from 'v-charts/lib/histogram.common' //柱状图
import VePie from 'v-charts/lib/pie.common' // 饼图
import auth from './utils/auth'
import http from './utils/http'
import message from './utils/message'
import messagebox from './utils/messagebox'
import myloading from './utils/loading'
// 自定义分页组件
import Pagination from '@/components/Pagination'
// 这个将项目中api分类管理，不同模块的api写在不同的.js文件
import api from './api/'




Vue.config.productionTip = false

Vue.prototype.$api=api
Vue.prototype.$auth=auth
Vue.prototype.$http=http
// 以后直接用this.$http就行
Vue.prototype.$message = message
Vue.prototype.$messagebox = messagebox
Vue.prototype.$myloading = myloading

Vue.use(ElementUI, {
  size: 'small'
})

// 全局组件挂载
Vue.component('Pagination', Pagination)
Vue.component(VeLine.name, VeLine)
Vue.component(VeBar.name, VeBar)
Vue.component(VeHistogram.name, VeHistogram)
Vue.component(VePie.name, VePie)

router.beforeEach((to, from, next) => {
  let token =sessionStorage.getItem('token')
  if (token){
    // next()
    if(to.fullPath == "/login" || to.fullPath == "/register"){
      next({path:from.fullPath})
    }else{
      next()
    }
  }else{
    if(to.path =="/login"|| to.path=="/register"){
      next()
    }else{
    next({path:"/login"})
  }
  }
});


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')





// 全局前置首位
// router.beforeEach((to, from, next) => {

  // if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
  //   if(sessionStorage.getItem('token')){ //判断本地是否存在access_token
  //     next();
  //   }else {
  //    if(to.path === '/login'|| to.path === '/register'){
  //       next();
  //     }else {
  //       next({
  //         path:'/login'
  //       })
  //     }
  //   }
  // }
  // else {
  //   next();
  // }
  /*如果本地 存在 token 则 不允许直接跳转到 登录页面*/
  // if(to.fullPath == "/login" || to.fullPath == "/register"){
  //   if(sessionStorage.getItem('token')){
  //     next({
  //       path:from.fullPath
  //     });
  //   }else {
  //     next();
  //   }
  // }else{
  //   next();
  // }
// });
