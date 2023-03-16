<template>
  <div class="container">
    <div class="top-group">
      <span>版本分支：</span>
      <el-select v-model="selectvalue" placeholder="请选择" width="60%">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.value"
          :value="item.value">
        </el-option>
      </el-select>
      <span>DIS否：</span>
      <el-radio-group v-model="radio1" size="small">
        <el-radio-button label="exp"></el-radio-button>
        <el-tooltip class="item" effect="dark" content="是dis才点这里" placement="top">
          <el-radio-button label="exp_dis"></el-radio-button>
        </el-tooltip>
      </el-radio-group>
      <span>测试集合：</span>
      <el-select v-model="testSuiteTest" placeholder="请选择">
        <el-option
          v-for="item in Packages"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
      <el-button type="primary" icon="el-icon-search" @click="report">查询</el-button>
      <el-tooltip class="item" effect="dark" content="更新本地的SVN仓库，勤点，没事的" placement="top">
        <el-button type="success" icon="el-icon-edit" @click="SvnUpdate">SvnUpdate</el-button>
      </el-tooltip>
      <el-tooltip class="item" effect="dark" content="展示本地仓库状态" placement="top">
        <el-button type="warning" icon="el-icon-s-comment" @click="showDetail">ShowDetail</el-button>
      </el-tooltip>

    </div>
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
      row-key="id"
      border
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
      v-if="showTable"
      lazy
      :load="load"
    >
    <!-- default-expand-all 全部扩展-->
      <!-- <el-table-column type="selection" width="55"></el-table-column> -->
      <el-table-column prop="name" label="用例名称"></el-table-column>
      <el-table-column label="执行结果">
         <template slot-scope="scope">
          <el-tag type="danger" v-if="scope.row.hasChildren" >Fail</el-tag>
          <el-tag type="danger" v-if="scope.row.hasChildren==false" >Junit Error</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作"  width="500%">
        <template slot-scope="scope"  v-if="scope.row.previewUrl">
          <el-button size="mini" plain type="primary" @click="gotoExp(scope.row)">预览Exp</el-button>
          <el-button size="mini" plain type="primary" @click="gotoRes(scope.row)">预览Res</el-button>
          <el-button size="mini" plain type="primary" @click="gotoDiff(scope.row)">预览Diff</el-button>
          <el-tooltip class="item" effect="dark" content="仅更新到本地仓库，请到顶部ShowDetail进行二次确认" placement="top">
            <el-button size="mini" plain type="danger" @click="replaceExp(scope.row)">替换本地图片</el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>
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
        <el-table-column property="state" label="状态" width="150">
          <template slot-scope="scope">
            <i v-if="scope.row.state==0" >Normal</i>
            <i v-if="scope.row.state==1" >RemoteLocked</i>
            <i v-if="scope.row.state==2" >LocalLocked</i>
            <i v-if="scope.row.state==3" >Locked</i>
            <i v-if="scope.row.state==4" >modified</i>
            <i v-if="scope.row.state==8" >远程有修改，本地需更新</i>
            <i v-if="scope.row.state==12" >有冲突，需解决</i>
            <i v-if="scope.row.state==16" >non-versioned</i>
            <i v-if="scope.row.state==32" >Error</i>
          </template>
        </el-table-column>
      </el-table>
        <span slot="footer" center class="dialog-footer">
          <el-tooltip class="item" effect="dark" content="点这里提交到svn" placement="top">
            <el-button type="primary" @click="SvnCommit">Svn Commit</el-button>
          </el-tooltip>
          <el-button @click="dialogTableVisible = false">取 消</el-button>
        </span>
    </el-dialog>
    <!-- 展示图片的dialog -->
      <div class="demo-image__preview">
        <el-image
          style="width: 0px; height: 0px"
          ref="previewImg"
          :preview-src-list="srcList"
          alt="there is no diff">
        </el-image>
    </div>
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
      host:[],
      replaceResult:[],
      commitSvnDialogVisible:false,
      dialogTableVisible:false,
      dialogDiffVisible:false,
      addProjectButtonLoading:false,
      options: junitVersion,  //在public/junitVersion下全局定义的
      selectvalue: '',
      Packages: testsuitePackage,   //在public/junitVersion下全局定义的
      testSuiteTest: '',
      tableDataCopy:'',
      tableData:[],
      showTable:true,
      props: {
          lazy: true,
          lazyLoad (node, resolve) {
            const { level } = node;
            setTimeout(() => {
              const nodes = Array.from({ length: level + 1 })
                .map(item => ({
                  value: ++id,
                  label: `选项${id}`,
                  leaf: level >= 2
                }));
              // 通过调用resolve将子节点数据返回，通知组件数据加载完成
              resolve(nodes);
            }, 1000);
          }
        },
      radio1:"exp",
      url:"",
      srcList : [],
      };

  },
  mounted(){},
  methods: {
    pagination(p) {
      this.fetchDataNoMessage(p.page, p.limit)
    },
    openDialog(){
      // 清除校验
        this.$nextTick(() => {
            this.$refs["hostForm"].clearValidate();
        })
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
      // 先清空 有bug  从0开始删除，长度为length
      if(this.selectvalue && this.testSuiteTest ){
        this.$myloading.show()
        this.$http.getReport(this.selectvalue,this.testSuiteTest).then(res=>{
          this.host=res.data
          this.total=this.host.length
          // 备份全量数据
          this.tableDataCopy = res.data || []
          this.tableData = JSON.parse(JSON.stringify(res.data)).map(item => { // 展示数据
                  // hasChildren 表示需要展示一个箭头图标
                  item.hasChildren = item.children && item.children.length > 0
                  // 只展示一层
                  // 如果有children数据，会自动加载，就不是懒加载了，也可以配置tree-props里面的children为其他字段
                  item.children = null
                  // 记住层级关系
                  item.idList = [item.id]
                  return item
                })
            // console.log("处理后的数据",this.tableData);
          // 备份处理结束
          this.$myloading.hide()
        }).catch(error=>{
              this.$notify.error("Junit还未出结果！");
              this.$myloading.hide()
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
      const ResUrl = row.previewUrl
      const ppg = ResUrl.substring(ResUrl.length-3)
      if (ppg=="png"){
        // 预览图片
        this.srcList.splice(0,this.srcList.length)
        this.srcList.push(ResUrl)
        this.$refs.previewImg.showViewer = true;
      }else{
        // 新窗口打开
        window.open(ResUrl)
      }
    },
    gotoExp(row){
      // alert(row.previewUrl)
      const ExpUrl = row.previewUrl.replace("res","exp")
      const ppg = ExpUrl.substring(ExpUrl.length-3)
      if (ppg=="png"){
        // 预览图片
        this.srcList.splice(0,this.srcList.length)
        this.srcList.push(ExpUrl)
        this.$refs.previewImg.showViewer = true;
      }else{
        // 新窗口打开
        window.open(ExpUrl)
      }
    },
    gotoDiff(row){
      const DiffUrl = row.previewUrl.replace("res","diffs")
      const ppg = DiffUrl.substring(DiffUrl.length-3)
      if (ppg=="pdf"){
        const lastUrl = DiffUrl.slice(0,-3) + "png"
        this.srcList.splice(0,this.srcList.length)
        this.srcList.push(lastUrl)
        this.$refs.previewImg.showViewer = true;
      }else{
        this.srcList.splice(0,this.srcList.length)
        this.srcList.push(DiffUrl)
        this.$refs.previewImg.showViewer = true;
      }
    },
    replaceExp(row){
      const isDis = "/".concat(this.radio1).concat("/")
      console.log("isdIS",isDis);
      let params = {version:this.selectvalue,realPath:row.realPath,isDis:isDis}
      console.log("要替换的是",row.realPath);
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
                const comment = '@author:'.concat(curUser).concat(".@reason:").concat(value)
                let params = {"version":this.selectvalue,"testsuite":this.testSuiteTest,"comment":comment}
                console.log("最终comment是",comment);
                this.$myloading.show()
                this.$http.SvnCommit(params).then(res=>{
                  this.$notify.success("更新成功")
                  this.$myloading.hide()
                  this.$messagebox.confirm({
                    message:res.data
                  })
                })
            }).catch(() => {
              this.$message({
                type: 'info',
                message: '取消关闭'
              });
            });
    },
        // 展开
    load (tree, treeNode, resolve) {
      resolveArr = null
      // 层级关系备份
      const idCopy = JSON.parse(JSON.stringify(tree.idList))

      // 查找下一层数据
      let resolveArr = this.tableDataCopy
      let id
      // eslint-disable-next-line
      while (id = tree.idList.shift()) {
        const tarItem = resolveArr.find(item => item.id === id)
        tarItem.loadedChildren = true
        resolveArr = tarItem.children
      }

      // 处理下一层数据的属性
      resolveArr = JSON.parse(JSON.stringify(resolveArr))
      resolveArr.forEach(item => {
        item.hasChildren = item.children && item.children.length > 0
        item.children = null
        // 此处需要深拷贝，以防各个item的idList混乱
        item.idList = JSON.parse(JSON.stringify(idCopy))
        item.idList.push(item.id)
      })

      // 标识已经加载子节点
      tree.loadedChildren = true
      // console.log("展开的数据",this.tableData);

      // 渲染子节点
      resolve(resolveArr)
    },
    unload () {
        this.showTable = false
        // eslint-disable-next-line
        this.$nextTick(() => this.showTable = true)
        this.tableData = JSON.parse(JSON.stringify(this.tableDataCopy)).map(item => {
          // hasChildren 表示需要展示一个箭头图标
          item.hasChildren = item.children && item.children.length > 0
          // 只展示一层
          item.children = null
          // 记住层级关系
          item.idList = [item.id]
          return item
        })
      },

  },
};
</script>

<style scoped>
.top-group{
  padding: 10px 0;
  text-align: left;
}
</style>