<template>
  <div class='myDiv'>
    <div>
      <el-input v-model="tarUrl" autocomplete="off" placeholder="请输入链接"></el-input>
      <el-button type="primary" @click="gotoUrl">提交</el-button>
    </div>
    <h1>Yonghong Integrate Dashboard Demo</h1>
    <div id='root'></div>
  </div>
</template>

<script>
// import xxx from './xxx';
import YHIntegrateDashboard from 'yh-integrate-dashboard-manager/es/YHIntegrateDashboard';
export default {
   name:'jsjicheng',
  props:[''],
  components: {},
  data() {
    return {
      tarUrl:"http://192.168.0.187:8090/bi/?proc=1&action=viewer&hback=true&isAir=true&platform=WAP&browserType=chrome",
    };
  },
  methods: {
    gotoUrl(){
      console.log("地址",this.tarUrl);
        var div = document.getElementById('root');
        YHIntegrateDashboard.init(div, this.tarUrl,'', '1440px', '900px', {style: {border: 'none', display: 'none'}});
        setTimeout(() => {
          YHIntegrateDashboard.open(div, {
              db: '123', // db path
              dbType: 16640 + ''
          });
        }, 0);
    },
  },
  mounted() {
    // var div = document.getElementById('root');
    // YHIntegrateDashboard.init(div, 'http://192.168.0.187:8090/bi/?proc=1&action=viewer&hback=true&isAir=true&platform=WAP&browserType=chrome',
    // '', '1440px', '900px', {style: {border: 'none', display: 'none'}});

    // // open the report
    // setTimeout(() => {
    //   YHIntegrateDashboard.open(div, {
    //       db: '12345', // db path
    //       dbType: 16640 + ''
    //   });
    // }, 0);
  }, //生命周期 - 挂载完成
}
</script>
<style scoped>
.myDiv {
    padding: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.el-input {
  width: 450px;
}

</style>