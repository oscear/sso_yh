<template>
  <div>
  <span>请先选主机：</span>
  <el-select v-model="cur_host" placeholder="请选择" @change="selectChangedHost">
    <el-option
      v-for="item in all_host"
      :key="item.id"
      :label="item.name"
      :value="item.proxy_host?item.proxy_host:item.host">
      <!-- :value="item.host"> -->
      <span style="float: left">{{ item.name }}</span>
      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.proxy_host?item.proxy_host:item.host }}</span>
    </el-option>
  </el-select>
  <el-divider></el-divider>
    <iframe  id="iframe" :src="iframesrc" width="100%" height="1000"></iframe>
  </div>
</template>

<script>
import pagetype from "../pagetype"
export default {
  name: "viewerManager",
  data() {
    return {
      host:[],
      all_host:[],
      pagetype,
      token:"",
      cur_host:"",
      // iframesrc:"/bi/Viewer?proc=0&action=editor"
      iframesrc:pagetype.page.viewerManager
    };
  },
  mounted(){
    this.$http.getHost().then(res=>{
      const host = res.data
      const token = sessionStorage.getItem("token")
      this.all_host=host
      this.token=token
    })
  },
  methods:{
    selectChangedHost(event){
      this.host=event
      const url = "http://"+ this.host + pagetype.page.viewerManager + "&token=" + this.token
      this.iframesrc= url
    }
  },
};
</script>

<style scoped>
.card-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>