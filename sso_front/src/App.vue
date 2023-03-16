<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  mounted(){
    // 浏览器关闭执行的是 beforeunload ， unload 这两个事件；
    // 而浏览器刷新执行的是beforeunload， unload， load 三个事件；
    window.onload = function(){
      console.log("isLogin等于",window.sessionStorage.getItem("isLogin"));
      if(window.sessionStorage.getItem("isLogin")){
        // 刷新操作
      }else{
        window.sessionStorage.removeItem("token")
      }
      };

    window.onunload = function(){
      window.sessionStorage.setItem("isLogin", true)
    };
    window.onbeforeunload = function(){
      window.sessionStorage.setItem("isLogin", true)
    };
  },
};
</script>

<style>
</style>
