<template>
  <div class="wrapper">
    <common-header></common-header>
    <common-sidebar></common-sidebar>
    <div class="content-box" :class="{'content-collapse':collapse}">
      <common-tags></common-tags>
      <div class="content">
        this is 首页
        <br>
      <div style="width: 500px; height: 500px">
        <ve-pie :data="chartData4"></ve-pie>
      </div>
        <!-- <transition name="move" mode="out-in">
          <keep-alive>
            <router-view></router-view>
          </keep-alive>
        </transition> -->
        <el-backtop target=".content"></el-backtop>
      </div>
    </div>
  </div>
</template>

<script>
import commonHeader from "./common/commonHeader";
import commonSidebar from "./common/commonSidebar";
import commonTags from "./common/commonTags";
import bus from "../service/bus";

export default {
  components: {
    commonHeader,
    commonSidebar,
    commonTags,
  },
  data() {
    return {
      collapse: false,
      chartData4: {
        columns: ["日期", "访问用户"],
        rows: [
          { 日期: "1/1", 访问用户: 1393 },
          { 日期: "1/2", 访问用户: 3530 },
          { 日期: "1/3", 访问用户: 2923 },
          { 日期: "1/4", 访问用户: 1723 },
          { 日期: "1/5", 访问用户: 3792 },
          { 日期: "1/6", 访问用户: 4593 },
        ],
      },
    };
  },
  created() {
    // 控制折叠面板
    bus.$on("collapse-content", (msg) => {
      this.collapse = msg;
    });
  },
};
</script>

<style scoped>
</style>
