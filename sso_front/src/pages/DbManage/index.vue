<template>
  <div class="container">
    <div class="top-group">
    <el-button type="primary" icon="el-icon-plus" @click="onAddProjectButtonClick">新增报告链接</el-button>
  </div>
    <el-table
      ref="multipleTable"
      :data="host"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="title" label="title" width="150%"></el-table-column>
      <el-table-column prop="url" label="url"></el-table-column>
      <el-table-column label="操作"  width="150%">
        <template slot-scope="scope">
          <el-button size="mini" plain type="primary" @click="editHost(scope.row)">编辑</el-button>
          <el-button size="mini" plain type="danger" @click="handDel(scope.row,scope.$index)">删除</el-button>
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
  <!-- 封装的分页 -->
    <!-- <Pagination
      @pagination="pagination"
      v-show="total > 0"
      :total="total"
      :page.sync="currentPage"
      :limit.sync="pageSize"
      class="pagination"
    /> -->
      <!-- 这里是dialog -->
  <el-dialog  :visible.sync="addDialogVisiable" title="新建项目" @open="openDialog()">
    <el-form ref="hostForm" :model="hostForm" label-width="80px" :rules="hostRules">
      <el-form-item label="title" prop="title">
        <el-input v-model="hostForm.title" autocomplete="off" placeholder="请输入报告名称"></el-input>
      </el-form-item>
      <el-form-item label="url" prop="url">
        <el-input v-model="hostForm.url" autocomplete="off" placeholder="从查看报告复制报告链接后，粘贴至此"></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="addDialogVisiable = false">取 消</el-button>
      <el-button type="primary" @click="onSubmitAddProject" :loading="addProjectButtonLoading">确 定</el-button>
    </div>
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
      host:[],
      addDialogVisiable:false,
      addProjectButtonLoading:false,
      dialogType : 'add',
      hostForm:{
        title:"",
        url:"",
      },
      hostRules: {
        name: [
          {required: true,message: "请输入环境名称！",trigger: "blur"},
        ],
        version: [
          {required: true,message: "请输入环境host！",trigger: "blur"},
        ],
        host: [
          {required: true,message: "请输入环境host！",trigger: "blur"},
        ]
      }
    };
  },
  mounted(){
    this.$http.getModule().then(res=>{
      const host = res.data
      this.total=host.length
      this.host=host
    })
  },
  methods: {
    pagination(p) {
      this.fetchDataNoMessage(p.page, p.limit)
    },
    initHostForm(){
      this.hostForm={
        index:"YHDB",
        title:"",
        url:"",
      }
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
    onAddProjectButtonClick(){
      this.dialogType = 'add',
      this.addDialogVisiable=true,
      this.initHostForm()
    },
    editHost(host){
      this.dialogType = 'edit'
      this.addDialogVisiable=true
      this.hostForm={
        id:host.id,
        index:"YHDB",
        title:host.title,
        url:host.url,
      }
    },
    handDel(host,index){
      console.log("要删除的内容行为",host.id);
      this.$messagebox.confirm({
        message:"您确定执行此操作吗？",
        confirmCallback:()=>{
          this.$http.delModule(host.id).then(res =>{
            this.host.splice(index,1)
            this.$notify.success("删除成功！")
            this.total--
        })
      }
      })
    },
    onSubmitAddProject(){
      this.$refs["hostForm"].validate(valid=>{
        if(!valid){
          return;
        }
        this.addProjectButtonLoading = true
        if(this.dialogType=="add"){
          this.$http.addModulet(this.hostForm).then(res=>{
            this.addProjectButtonLoading = false
            if(res){
              const host=res.data
              this.host.push(host)
              this.total++
              this.addDialogVisiable = false
              this.initHostForm()
              this.$notify.success("恭喜创建成功")
            }
          })
        }else{
          this.$http.editModule(this.hostForm.id,this.hostForm).then(res=>{
            this.addProjectButtonLoading=false
            if(res){
              this.addDialogVisiable=false
              this.initHostForm()
              this.$notify.success("恭喜，项目修改成功")
              const host = res.data
              let index = 0
              for(let loop_host of this.host){
                if(loop_host.id == host.id){
                  // Vue.set(this.host,index,host)
                  // 刷新页面
                  this.host.splice(index,1,host)
                  break
                }
                index++
              }
            }
          })
        }
      })
    }
  },
};
</script>

<style scoped>
.top-group{
  padding: 10px 0;
  text-align: left;
}
</style>