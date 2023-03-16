<template>
  <div class="login-wrapper">
    <div class="bg-wrapper">
      <div class="left-wrapper">
        <img
          src="../../assets/images/logo.png"
          style="border-radius: 10px; width: 80px; height: 80px"
        />
        <span class="title">注册页面</span>
      </div>
      <div class="right-wrapper">
        <el-form :model="loginForm" :rules="loginRules" ref="loginRef">
          <div class="login-title">注册用户</div>
          <el-form-item style="margin-top: 20px" prop="username">
            <el-input
              v-model="loginForm.username"
              size="large"
              style="width: 300px"
              placeholder="用户名"
              prefix-icon="el-icon-user"
            ></el-input>
          </el-form-item>
          <el-form-item style="margin-top: 20px" prop="password">
            <el-input
              show-password
              v-model="loginForm.password"
              size="large"
              style="width: 300px"
              type="password"
              placeholder="密码"
              prefix-icon="el-icon-lock"
            ></el-input>
          </el-form-item>
          <el-form-item style="margin-top: 20px" prop="userEmail">
            <el-input  v-model="loginForm.userEmail" size="large" style="width: 300px"  placeholder="邮箱" prefix-icon="el-icon-lock"></el-input>
          </el-form-item>
          <!-- <el-form-item style="margin-top: 20px" prop="userAlias">
            <el-input  v-model="loginForm.userAlias" size="large" style="width: 300px"  placeholder="用户别名" prefix-icon="el-icon-lock"></el-input>
          </el-form-item>
          <el-form-item style="margin-top: 20px" prop="userRoles">
            <el-input  v-model="loginForm.userRoles" size="large" style="width: 300px"  placeholder="角色,若有多个请用逗号分割！" prefix-icon="el-icon-lock"></el-input>
          </el-form-item><el-form-item style="margin-top: 20px" prop="userGroups">
            <el-input  v-model="loginForm.userGroups" size="large" style="width: 300px"  placeholder="用户组层级以/分割，多个逗号分割" prefix-icon="el-icon-lock"></el-input>
          </el-form-item><el-form-item style="margin-top: 20px" prop="param">
            <el-input  v-model="loginForm.param" size="large" style="width: 300px"  placeholder="请传入json格式参数" prefix-icon="el-icon-lock"></el-input>
          </el-form-item> -->
          <el-form-item style="margin-top: 30px">
            <el-button type="primary" style="width: 100%" size="large" @click="handleRegister">注册</el-button>
          </el-form-item>
          <el-form-item style="margin-top: 30px">
            <el-button type="info" style="width: 100%" size="mini" @click="gotoLogin">已有账号前去登录</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchLogin } from "../../api/login";
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
        userEmail:"",
        // userAlias:"",
        // userRoles:"",
        // userGroups:"",
        // param:"",
      },
      loginRules: {
        username: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    // 登录请求
    gotoLogin(){
      this.$router.push("/login");
    },
    handleRegister() {
      if(sessionStorage.getItem("token")){
        sessionStorage.removeItem("token")
        sessionStorage.removeItem("username")
      }
      this.$refs["loginRef"].validate((valid) => {
        if (!valid) {
          return;
        } else {
          let params = {
            username: this.loginForm.username,
            password: this.loginForm.password,
            userEmail: this.loginForm.userEmail,
            // userAlias: this.loginForm.userAlias,
            // userRoles: this.loginForm.userRoles,
            // userGroups: this.loginForm.userGroups,
            // param: this.loginForm.param,
          };
          // fetchLogin(params).then((res) => {
            this.$http.register(params).then((res) =>{
            if (res.data.code === 200) {
              this.$notify.success("恭喜注册成功，请前往登录！")
              this.$router.push("/login");
            } else {
              this.$message.error(res.data);
              return;
            }
          });
        }
      });
    },
  },
};
</script>

<style scoped>
.login-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url("../../assets/images/login_bg.jpg");
  background-size: cover;
  display: flex;
  flex-direction: row;
  z-index: 1;
  justify-content: center;
  align-items: center;
}

.bg-wrapper {
  width: 70%;
  height: 65%;
  z-index: 9999;
  opacity: 0.95;
  display: flex;
  flex-direction: row;
}

.left-wrapper {
  display: flex;
  flex: 1;
  background-color: #6190e8;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.title {
  color: white;
  font-size: 30px;
  margin-top: 30px;
}

.right-wrapper {
  flex: 1;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
}

.login-title {
  width: 300px;
  text-align: center;
  font-size: 30px;
  margin-bottom: 40px;
}
</style>