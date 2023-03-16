<template>
  <div class="top-group">
      <div class="div1">
        <h3>select your Excel here</h3>
        <el-upload
          class="upload-demo"
          ref="upload"
          drag
          :headers="headers"
          :action="backUrl"
          :before-upload="handleBefore"
          :on-change="handleChange"
          :on-success="uploadSuccess"
          :show-file-list="true"
          :on-remove="handleRemove"
          :file-list="fileList"
          :limit="1"
          :auto-upload="true"
        >
        <!-- accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"  添加后拖拽不生效 -->
        <!-- :on-change="handleChange" -->
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传xlsx/xls文件，且不超过5M</div>
        </el-upload>
      </div>
      <div class="div2" v-if="cities">
          <h3>There is sheets of Excel!</h3>
          <div style="margin: 15px 0;"></div>
          <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
            <el-checkbox v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox>
          </el-checkbox-group>
          <el-button @click="getXML" :disabled="sheetnames.length > 0 ? false : true" type="primary" class="downtn">点击下载xml</el-button>
      </div>

  </div>
</template>

<script>
export default {
  name: '',
  data() {
    return {
      fileList: [],
      tableData2: [],
      sheetnames:[],
      checkedCities: [],
      cities: "",
      isIndeterminate: true,
      backUrl:"",
      headers: {
        'Authorization': "Token " + this.$auth.token
      }
    }
  },
  components: {},
  mounted() {
    let backURLl
    backURLl = window.VUE_APP_URL.backURL    //上传接口
    this.backUrl=backURLl + "/api/v1/AvatarUpload/"
  },
  methods: {
    // excel表上传
    handleBefore(file) {
        // 文件类型
      const isType = file.type === 'application/vnd.ms-excel'
      const isTypeComputer = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      const fileType = isType || isTypeComputer
      if (!fileType) {
        this.$message.error('上传文件只能是xls/xlsx格式！')
      }
      // 文件大小限制为2M
      const fileLimit = file.size / 1024 / 1024 < 5
      if (!fileLimit) {
        this.$message.error('上传文件大小不超过5M！')
      }
      return fileType && fileLimit
    },
    handleChange(file, fileList) {
      this.fileTemp = file.raw
    },
    // 移除excel表
    handleRemove(file, fileList) {
      this.fileTemp = null
    },
    uploadSuccess(res,file,fileList){
        this.$refs.upload.clearFiles();
        this.cities=res
        this.sheetnames.splice(0,this.sheetnames.length)
    },
    importfxx(obj) {
      console.log("导入的是",obj);
      let _this = this
      // 通过DOM取文件数据
      this.file = obj
      var rABS = false //是否将文件读取为二进制字符串
      var f = this.file
      var reader = new FileReader()
      FileReader.prototype.readAsBinaryString = function (f) {
        var binary = ''
        var rABS = false //是否将文件读取为二进制字符串
        var pt = this
        var wb //读取完成的数据
        var outdata
        var reader = new FileReader()
        reader.onload = function (e) {
          var bytes = new Uint8Array(reader.result)
          var length = bytes.byteLength
          for (var i = 0; i < length; i++) {
            binary += String.fromCharCode(bytes[i])
          }
          var XLSX = require('xlsx')
          if (rABS) {
            wb = XLSX.read(btoa(fixdata(binary)), {
              //手动转化
              type: 'base64',
            })
          } else {
            wb = XLSX.read(binary, {
              type: 'binary',
            })
          }
          console.log("解析文件",wb);
          _this.checkedCities=wb.SheetNames
          _this.cities=wb.SheetNames
          _this.sheetnames=wb.SheetNames
          console.log("找到sheet",_this.cities);

        }
        reader.readAsArrayBuffer(f)
      }
      if (rABS) {
        reader.readAsArrayBuffer(f)
      } else {
        reader.readAsBinaryString(f)
      }
    },
    // 导入表格-el-upload--end
    handleCheckAllChange(val) {
      this.checkedCities = val ? cityOptions : [];
      this.isIndeterminate = false;
    },
    handleCheckedCitiesChange(value) {
      this.sheetnames=value
      let checkedCount = value.length;
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length;
    },
    async getXML(){
      this.sheetnames.forEach(item=>{
        this.$http.getXML(item).then(res=>{
          let url = this.backUrl +  "?sheetname=" + item
          window.open(url)
        }).catch(err=>{
          this.$message.error("something not found")
        })
    })


    },
  },
  watch: {},
}
</script>
<style lang='scss'>
.upload-excels {
  width: 600%;
  height: 600%;
  .excel2 {
    width: 500px;
    height: 100px;
    border: 1px solid red;
  }
}

.div1{
  width:30%;
  height:300px;
  float:left;
}
.div2{
  width:50%;
  height:300px;
  float:left;
}
.downtn{
  margin:80px 0px
}
.top-group{
  padding: 20px 0;
  text-align: left;
}
</style>
