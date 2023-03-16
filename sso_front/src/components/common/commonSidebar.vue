<template>
  <div class="sidebar">
    <el-menu :default-active="onRoute"
             class="sidebar-el-menu"
             :collapse="collapse"
             background-color="#fff"
             text-color="#333"
             active-text-color="#6190e8"
             router
             unique-opened>
      <template v-for="item in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index"
                      :key="item.index">
            <template slot="title">
              <!-- 预留字体图标 -->
              <i :class="item.icon"></i>
              <span slot="title"
                    class="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-submenu v-if="subItem.subs"
                          :index="subItem.index"
                          :key="subItem.index"
                          class="title">
                <template slot="title"
                          class="title">{{ subItem.title }}</template>
                <el-menu-item v-for="(threeItem,i) in subItem.subs"
                              :key="i"
                              :index="threeItem.index"
                              class="title">{{ threeItem.title }}</el-menu-item>
              </el-submenu>
              <el-menu-item v-else
                            :index="subItem.index"
                            :key="subItem.index"
                            class="title">{{ subItem.title }}</el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index"
                        :key="item.index"
                        class="title">
            <!-- 预留字体图标 -->
            <i :class="item.icon"></i>
            <span slot="title"
                  class="title">{{ item.title }}</span>
          </el-menu-item>
          <!-- 嵌套报告 -->
        </template>
      </template>
      <!-- //下面是自定义报告 -->
      <template v-for="item in dbs">
        <template v-if="item.subs">
          <el-submenu :index="item.index"
                      :key="item.index">
            <template slot="title">
              <!-- 预留字体图标 -->
              <i :class="item.icon"></i>
              <span slot="title"
                    class="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-submenu v-if="subItem.subs"
                          :index="subItem.index"
                          :key="subItem.id"
                          class="title">
                <template slot="title"
                          class="title">
                  {{ subItem.title }}
                </template>
                <el-menu-item v-for="(threeItem) in  subItem.subs"
                              :key="threeItem.index"
                              :index="threeItem.index"
                              class="title">
                  123{{ threeItem.title }}
                </el-menu-item>
              </el-submenu>
              <!-- 实际渲染成下面这个了，你要看看正常不  index不一样，可能路由没找对，我看看线现象对不对 -->
              <!-- 刷新路由菜单初始化匹配有问题，只是改下面的这个为id，我以为渲染的是上面的，结果是下面这个  啥意思  没啥  就是key重复的问题  vue的每个标签上都有data-开头的唯一值，表示这个dom，你重复了就让vue认为这个节点匹配上了，因为vue只认key -->
              <el-menu-item v-else
                            :index="subItem.id.toString()"
                            :key="subItem.id"
                            class="title"
                            :route="{ path: subItem.index, query: { href: subItem.url,title:subItem.title }, params: { id: '123'}}">{{ subItem.title }}</el-menu-item>
            </template>
          </el-submenu>
        </template>
      </template>
      <!-- 自定义表格结束 -->
    </el-menu>
  </div>
</template>

<script>
import bus from '../../service/bus'
export default {
  name: 'commonSidebar',
  data() {
    return {
      collapse: false,
      items: [
        // {
        //   icon: "el-icon-location-outline",
        //   index: "dashboard",
        //   title: "系统首页",
        // },
        // {
        //   icon: "el-icon-notebook-2",
        //   index: "table",
        //   title: "基础表格",
        // },
        {
          icon: 'el-icon-notebook-2',
          index: 'userDetail',
          title: '用户信息',
        },
        {
          icon: 'el-icon-reading',
          index: 'Host',
          title: '主机配置',
        },
        {
          icon: 'el-icon-data-board',
          index: 'DbManage',
          title: '报告配置',
        },
        {
          icon: 'el-icon-data-board',
          index: 'testlink',
          title: 'testlink',
        },
        {
          icon: 'el-icon-data-board',
          index: 'JunitReplace',
          title: 'Junit',
        },
        // {
        //   icon: 'el-icon-data-board',
        //   index: 'jsjicehng',
        //   title: 'js集成',
        // },
        {
          icon: 'el-icon-reading',
          index: '3',
          title: 'Sso单点',
          subs: [
            // {
            //   index: "form",
            //   title: "基本表单",
            // },
            // {
            //   index: "form-detail",
            //   title: "表单详情",
            // },
            {
              index: 'editor',
              title: '制作报告',
            },
            {
              index: 'viewerManager',
              title: '查看报告',
            },
            {
              index: 'workflow',
              title: '流程审批',
            },
            {
              index: 'Custom',
              title: '自定义内容',
            },
          ],
        },
      ],
      dbs: [
        {
          id: 1,
          index: '报告嵌套',
          title: '报告嵌套',
          icon: 'el-icon-data-board',
          subs: '',
          // subs: [
          //   {
          //   id:1,
          //     index: 'YHDB',
          //     title: '第一个报告',
          //     url: 'http://192.168.0.254:8066/bi/Viewer?proc=1&action=viewer&hback=true&db=33333.db&platform=PC&browserType=chrome',
          //   },
          // ]
        },
      ],
    }
  },
  created() {
    // 控制折叠面板
    bus.$on('collapse', (msg) => {
      this.collapse = msg
      bus.$emit('collapse-content', msg)
    })
    this.$http.getModule().then((res) => {
      this.dbs[0].subs = res.data
    })
  },
  computed: {
    // 路由配置
    onRoute() {
      return this.$route.path.replace('/', '')
    },
  },
}
</script>

<style scoped>
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
  width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}
.sidebar > ul {
  height: 100%;
}

.title {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.el-menu-item {
  border-left: #fff solid 6px;
}
/* 设置鼠标悬停时el-menu-item的样式 */
.el-menu-item:hover {
  border-left: #6190e8 solid 6px !important;
  background-color: #e2eff9 !important;
  color: #6190e8 !important;
}

.el-menu-item:hover i {
  color: #6190e8;
}

/* 设置选中el-menu-item时的样式 */
.el-menu-item.is-active {
  border-left: #6190e8 solid 6px !important;
  background-color: #e2eff9 !important;
  color: #6190e8 !important;
}
</style>