<template>
  <div class="container">
    <div class="top-group">
      <span>选择分支：</span>
      <el-select v-model="selectvalue" placeholder="请选择">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.value"
          :value="item.value">
        </el-option>
      </el-select>
      <span>然后选择一个模块吧：</span>
      <el-select v-model="testSuiteTest" placeholder="请选择">
        <el-option
          v-for="item in Packages"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-button type="primary" icon="el-icon-search" @click="report">查询</el-button>
      <el-button type="success" icon="el-icon-edit" @click="SvnUpdate">SvnUpdate</el-button>
      <el-button type="warning" icon="el-icon-s-comment" @click="showDetail">ShowDetail</el-button>
    </div>

<div ref="list" style="height:630px;overflow-y: scroll;"  @scroll="scrollEvent">
  <!-- style="height:640px;overflow-y: scroll;" -->
  <div>
  <div  :style="{ transform: getTransform }">
    <el-table
      ref="multipleTable"
      :data="visibleData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
      row-key="id"
      border
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
      :row-style="{ height: itemSize + 'px',lineHeight: itemSize + 'px' }"
    >
    <!-- default-expand-all 全部扩展-->
      <!-- <el-table-column type="selection" width="55"></el-table-column> -->
      <el-table-column prop="name" label="用例名称"></el-table-column>
      <el-table-column label="执行结果">
         <template slot-scope="scope">
          <el-tag type="danger" v-if="scope.row.children" >Fail</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作"  width="500%">
        <template slot-scope="scope"  v-if="!scope.row.children">
          <el-button size="mini" plain type="primary" @click="gotoExp(scope.row)">预览Exp</el-button>
          <el-button size="mini" plain type="primary" @click="gotoRes(scope.row)">预览Res</el-button>
          <el-button size="mini" plain type="danger" @click="replaceExp(scope.row)">替换,187暂时禁用</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  </div>
</div>
    <div>

      <!--这里是分页控件 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage4"
        :page-size="10"
        layout="total,  prev, pager, next, jumper"
        :total="total"
         class="pagination"
      ></el-pagination>
      <!-- 这里是dialog -->
    <el-dialog  :visible.sync="dialogTableVisible" center>
      <el-table :data="replaceResult">
        <el-table-column property="file" label="结果清单"></el-table-column>
        <el-table-column property="state" label="状态" width="100"></el-table-column>
      </el-table>
        <span slot="footer" center class="dialog-footer">
          <el-button type="primary" @click="SvnCommit">Svn Commit</el-button>
          <el-button @click="dialogTableVisible = false">取 消</el-button>
        </span>
    </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: "btable",
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      total: 0,
      currentPage4: 0,
      listData:[],
      replaceResult:[],
      commitSvnDialogVisible:false,
      dialogTableVisible:false,
      options: junitVersion,  //在public/junitVersion下全局定义的
      selectvalue: '',
      Packages: testsuitePackage,   //在public/junitVersion下全局定义的
      testSuiteTest: '',
      //  每行高度
      itemSize: 41,
      //可视区域高度
      screenHeight:0,
      //偏移量
      startOffset:0,
      //起始索引
      start:0,
      //结束索引
      end:null,
    };
  },
  mounted(){
    this.screenHeight = this.$el.clientHeight;
    console.log("this.screenHeight ",this.screenHeight );
    this.start = 0;
    this.end = this.start + this.visibleCount;
  },
  watch:{
      length(val){
          // 超过10行数据，就按照最大40*10 400px高度的列表就行
          if (val >= 10) {
            this.$refs.list2.style.height = this.listData.length * this.itemSize
          } else {
          // 不足10行数据，这边 加57是因为表头的高度，具体情况，你们加不加无所谓
            this.$refs.listWrap.style.height = this.itemSize * val + 57 + 'px'
          }
      }
  },
  computed:{
    //列表总高度
    listHeight(){
      return this.listData.length * this.itemSize;
    },
    //可显示的列表项数
    visibleCount(){
      // return Math.ceil(this.screenHeight / this.itemSize)
      return 50
    },
    //偏移量对应的style
    getTransform(){
      return `translate3d(0,${this.startOffset}px,0)`;
    },
    //获取真实显示列表数据
    visibleData(){
      console.log("当前数据是",this.listData.slice(this.start, Math.min(this.end,this.listData.length)));
      return this.listData.slice(this.start, Math.min(this.end,this.listData.length));
    },
    length(){
      return this.listeData.length || 0
    }

  },
  methods: {
    pagination(p) {
      this.fetchDataNoMessage(p.page, p.limit)
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach((row) => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    report(){
      if(this.selectvalue && this.testSuiteTest ){
        this.$myloading.show()
        this.$http.getReport(this.selectvalue,this.testSuiteTest).then(res=>{
          this.listData=res.data
          this.total=this.listData.length
          this.$myloading.hide()
        }).catch(error=>{
              this.$notify.error("先选择一下？");
        })
      }else{
        this.$notify.error("不可以为空，请选择！")
      }

    },
    SvnUpdate(){
      if(this.selectvalue && this.testSuiteTest ){
        this.$messagebox.confirm({
          message:"你现在要更新的是" + this.selectvalue +"版本的" + this.testSuiteTest + "模块，确认执行Svn update吗？？？",
          confirmCallback:()=>{
            this.$myloading.show()
            let params = {"version":this.selectvalue,"testsuite":this.testSuiteTest}
            this.$http.SvnUpdate(params).then(res=>{
              this.$myloading.hide()
              this.$messagebox.confirm({
                message:res.data[0]
              })
            })
        }
        })
      }else{
        this.$notify.error("不可以为空，请选择！")
      }
    },
    showDetail(){
      // 获取新数据
      if(this.selectvalue && this.testSuiteTest ){
        this.$myloading.show()
        this.$http.showDetail(this.selectvalue,this.testSuiteTest).then(res=>{
          this.replaceResult = res.data
          this.$myloading.hide()
          this.dialogTableVisible=true
        })
      }else{
        this.$notify.error("不可以为空")
      }
    },
    gotoRes(row){
      // alert(row.previewUrl)
      window.open(row.previewUrl)
    },
    gotoExp(row){
      // alert(row.previewUrl)
      const ExpUrl = row.previewUrl.replace("res","exp")
      window.open(ExpUrl)
    },
    replaceExp(row){
      let params = {version:this.selectvalue,realPath:row.realPath}
      this.$http.replaceExp(params).then(res=>{
        if(res.status==200){
          this.$notify.success(res.data)
        }
      }).catch(error=>{
        this.$notify.error(error.data.error)
      })
    },
    SvnCommit(){
      this.$prompt('输入commitMessage：', '确认提交到Svn?', {
              confirmButtonText: '提交',
              cancelButtonText: '取消',
              inputType:"textarea",
              inputValidator: (value) => {
                if(!value) {
                  return '这个是必填项';
                }
              },
              beforeClose: (action, instance, done) => { // 取消回车确认事件
              if (action === 'confirm') {
                instance.$refs['confirm'].$el.onclick = function (e) {
                e = e || window.event;
                if (e.detail !== 0) {
                    done();
                }
                  }();
              } else {
                  done();
              }
            }
            }).then(({ value }) => {
                const curUser = sessionStorage.getItem("username")
                const comment = '@user:'.concat(curUser).concat(".@reason:").concat(value)
                let params = {"version":this.selectvalue,"testsuite":this.testSuiteTest,"comment":comment}
                console.log("最终comment是",value);
                this.$myloading.show()
                this.$http.SvnCommit(params).then(res=>{
                  this.$notify.success("更新成功")
                  this.$myloading.hide()
                  this.$messagebox.confirm({
                    message:res
                  })
                })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '取消关闭'
              });
            });
    },
    scrollEvent() {
      //当前滚动位置
      let scrollTop = this.$refs.list.scrollTop;
      //此时的开始索引
      this.start = Math.floor(scrollTop / this.itemSize);
      //此时的结束索引
      this.end = this.start + this.visibleCount;
      //此时的偏移量偏移量
      this.startOffset = scrollTop - (scrollTop % this.itemSize);

      // this.$refs.list2.style.transform = `translateY(${this.start * this.itemSize}px)`
      // console.log("11当前滚动的位置",scrollTop);
      console.log("11开始索引",this.start);
      // console.log("11可以显示的条数",this.visibleCount);
      console.log("11结束索引",this.end);
      // console.log("11偏移量",this.startOffset);
    }
  },
};
</script>

<style scoped>
.top-group{
  padding: 10px 0;
  text-align: left;
}
.infinite-list-container {
  height: 100%;
  overflow: auto;
  position: relative;
  -webkit-overflow-scrolling: touch;
}

.infinite-list-phantom {
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  z-index: -1;
}

.infinite-list {
  left: 0;
  right: 0;
  top: 0;
  position: absolute;
  text-align: center;
}

.infinite-list-item {
  padding: 10px;
  color: #555;
  box-sizing: border-box;
  border-bottom: 1px solid #999;
}
</style>