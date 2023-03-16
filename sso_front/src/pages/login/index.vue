<template>
  <div class="login-wrapper">
    <div class="bg-wrapper">
      <div class="left-wrapper">
        <img
          src="../../assets/images/logo.png"
          style="border-radius: 10px; width: 80px; height: 80px"
        />
        <span class="title">Sso单点登录</span>
      </div>
      <div class="right-wrapper">
        <el-form :model="loginForm" :rules="loginRules" ref="loginRef">
          <div class="login-title">欢迎登录</div>
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
          <el-form-item style="margin-top: 30px">
            <!-- <el-button type="primary" style="width: 100%" size="large" @click="handleLogin">登录</el-button>
            <el-button type="primary" icon="el-icon-edit" circle></el-button> -->

            <div align="left" style="float:left">
                <el-button type="primary" style="width: 300%" size="large" @click="handleLogin" >登录</el-button>
            </div>
            <div align="right">
              <!-- <el-button type="primary"  size="large" >注册</el-button> -->
                <el-button type="primary" @click="handleRegister"  size="large">注册</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from 'axios';
import { fetchLogin } from "../../api/login";
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
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
    handleLogin() {
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
          };
          //api分类综合管理
          // this.$api.login.fetchLogin(params).then(res=>{
          //   console.log("res",res);
          // })
          // fetchLogin(params).then((res) => {
          this.$http.login(params).then((res) =>{
            if (res.data.code === 200) {
              sessionStorage.setItem("token", res.data.data);
              sessionStorage.setItem("username", res.data.username);
              sessionStorage.setItem("uuid", res.data.uuid);
              this.$router.push("/dashboard");
              this.$notify.success("登录成功")
            } else {
              this.$message.error(res.data);
              return;
            }
          }).catch(error=>{
            this.$notify.error("账号或密码不正确哦！");
          });
        }
      });
    },
    handleRegister(){
      this.$router.push("/register").catch(err =>(console.log("1")));
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