<template>
  <div class="header">
    <div class="logo">成都单点测试环境</div>
    <div class="collapse-btn" @click="handleCollapseChange">
      <i v-if="!collapse" class="el-icon-s-fold"></i>
      <i v-else class="el-icon-s-unfold"></i>
    </div>
    <div class="header-right">
      <div class="header-user-con">
        <div class="btn-fullscreen" @click="handleFullScreen">
          <el-tooltip effect="dark" :content="fullScreen?`取消全屏`:`全屏`" placement="bottom">
            <i class="el-icon-rank"></i>
          </el-tooltip>
        </div>
        <div class="user-avator">
          <img src="../../assets/images/logo.png" />
        </div>
        <el-dropdown class="user-name" trigger="click" @command="handleCommand">
          <span class="el-dropdown-link">
            <!-- 北京xxxxxx公司 -->
            {{login_user}}
            <i class="el-icon-caret-bottom"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
             <!-- <a href="https://github.com/FTLLOVE/vue-system-admin" target="_blank">
              <el-dropdown-item>项目仓库</el-dropdown-item>
            </a> -->
            <a href="http://192.168.0.187:9999/cent187" target="_blank">
              <el-dropdown-item>测试环境</el-dropdown-item>
            </a>
            <a :href="demo" target="_blank">
              <el-dropdown-item>用例模板</el-dropdown-item>
            </a>
            <el-dropdown-item divided command="logout" >退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<script>
import bus from "../../service/bus";
export default {
  name: "commonHeader",
  data() {
    return {
      collapse: false,
      fullScreen: false,
      login_user:sessionStorage.getItem('username'),
      demo:window.VUE_APP_URL.backURL+"/api/v1/AvatarUpload/"
    };
  },
  methods: {
    // 全屏
    handleFullScreen() {
      let element = document.documentElement;
      if (this.fullScreen) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      } else {
        if (element.requestFullscreen) {
          element.requestFullscreen();
        } else if (element.webkitRequestFullScreen) {
          element.webkitRequestFullScreen();
        } else if (element.msRequestFullscreen) {
          element.msRequestFullscreen();
        }
      }
      this.fullScreen = !this.fullScreen;
    },

    // 下拉菜单选择
    handleCommand(commond) {
      if (commond === "logout") {
      sessionStorage.removeItem("token")
      sessionStorage.removeItem("username")
      sessionStorage.removeItem("uuid")
      this.$notify.success("退出成功！")
      this.$router.push("/login");
      }
    },

    // 控制折叠面板
    handleCollapseChange() {
      this.collapse = !this.collapse;
      bus.$emit("collapse", this.collapse);
    },
    clearToken(){

    }
  },
};
</script>

<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 22px;
  background-color: #6190e8;
  color: #ffffff;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
}
.collapse-btn {
  float: left;
  padding: 0 21px;
  cursor: pointer;
  line-height: 70px;
  color: #ffffff;
}
.header .logo {
  float: left;
  line-height: 70px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  color: #ffffff;
  margin-left: 15px;
}
.header-right {
  float: right;
  padding-right: 20px;
}
.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}
.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 5px;
  font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
}
.btn-bell-badge {
  position: absolute;
  right: 0;
  top: -2px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #999;
}
.btn-bell .el-icon-bell {
  color: #999;
}
.user-name {
  margin-left: 10px;
}
.user-avator {
  margin-left: 10px;
}
.user-avator img {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.el-dropdown-link {
  color: #ffffff;
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.el-dropdown-menu__item {
  text-align: center;
}
</style>