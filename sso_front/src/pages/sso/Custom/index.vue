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
  <span>然后选模块：</span>
  <el-select v-model="cur_page" placeholder="请选择" @change="selectChanged">
    <el-option
      v-for="item in allpage"
      :key="item.url"
      :label="item.label"
      :value="item.url">
      <span style="float: left">{{ item.alias }}</span>
      <span style="float: right; color: #8492a6; font-size: 13px">{{ item.label }}</span>
    </el-option>
  </el-select>
    <el-divider></el-divider>
    <iframe  id="iframe" :src="iframesrc" ref="iframe" width="100%" height="1000"></iframe>
  </div>
</template>

<script>
import pagetype from "../pagetype"
export default {
  name: "custom",
  data() {
    return {
      pagetype,
      allpage:pagetype.allpage,
      iframesrc:pagetype.page.conn,
      all_host:[],
      host:[],
      token:"",
      cur_page:"",
      cur_host:""
    };
  },
  mounted(){
    this.$http.getHost().then(res=>{
      const host = res.data
      const token = sessionStorage.getItem("token")
      this.all_host=host
      // this.host=host[0].host
      this.token=token
    })
  },
  methods:{
    selectChangedHost(event){
      this.host=event
    },
    selectChanged(event){
      const url = "http://"+ this.host + event + "&token=" + this.token
      // const url = config.productURL + event + "&token=" + this.token
      this.iframesrc= url
      console.log("当前url为",this.iframesrc);
    }

  }
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