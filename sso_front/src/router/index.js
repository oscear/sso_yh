import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/',
			redirect: '/login'
		},
		{
			path: '/',
			component: () => import('../components/Home.vue'),
			meta: { title: 'home' },
			children: [
				{
					path: 'dashboard',
					component: () => import('../pages/dashboard'),
					meta: { title: '系统首页' }
				},
				{
					path: 'table',
					component: () => import('../pages/table'),
					meta: { title: '基本表格' }
				},
        {
					path: 'userDetail',
					component: () => import('../pages/userDetail'),
					meta: { title: '用户信息' }
				},
        {
					path: 'Host',
					component: () => import('../pages/Host'),
					meta: { title: '主机配置' }
				},
        {
					path: 'DbManage',
					component: () => import('../pages/DbManage'),
					meta: { title: '报告配置' }
				},
        {
					path: 'testlink',
					component: () => import('../pages/testlink'),
					meta: { title: 'testlink' }
				},
        {
					path: 'JunitReplace',
					component: () => import('../pages/JunitReplace'),
					meta: { title: 'junit' }
				},
				{
					path: 'form',
					component: () => import('../pages/form'),
					meta: { title: '复杂表单',requireAuth:true  }
				},
				{
					path: 'jsjicehng',
					component: () => import('../pages/sso/jsjicheng'),
					meta: { title: 'js集成方式' }
				},
				{
					path: 'editor',
					component: () => import('../pages/sso/editor'),
					meta: { title: '制作报告',requireAuth:true }
				},
				{
					path: 'viewerManager',
					component: () => import('../pages/sso/viewerManager'),
					meta: { title: '查看报告',requireAuth:true }
				},
				{
					path: 'workflow',
					component: () => import('../pages/sso/workflow'),
					meta: { title: '流程审批',requireAuth:true }
				},
				{
					path: 'custom',
					component: () => import('../pages/sso/Custom'),
					meta: { title: '自定义模块',requireAuth:true }
				},
				{
					path: 'YHDB',
					component: () => import('../pages/sso/YHDB'),
					meta: { title: '报告嵌套',requireAuth:true },
          // 是说这个title吧 更新我写了beforeupdateroute  和这个没关系  key是指vue的diff机制导致的  知识所开发者开发时循环这种多个同样的dom需要开发者手动设置唯一key，优化vue区分

          beforeEnter (to,from,next){
            to.meta.title = to.query.title
            next()
          }
				},
				{
					path: 'upload',
					component: () => import('../pages/upload'),
					meta: { title: '文件上传' }
				},
				{
					path: 'charts',
					component: () => import('../pages/charts'),
					meta: { title: 'vchart图表' }
				},
			]
		},
		{
			path: '/login',
			component: () => import('../pages/login'),
			meta: { title: '登录' }
		},
    {
			path: '/register',
			component: () => import('../pages/register'),
			meta: { title: '注册' }
		}
	]
})



