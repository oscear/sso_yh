<template>
  <div class="container">
    <el-table
      ref="multipleTable"
      :data="user"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55"></el-table-column>
      <el-table-column prop="username" label="username"></el-table-column>
      <el-table-column prop="userAlias" label="userAlias"></el-table-column>
      <el-table-column prop="email" label="email"></el-table-column>
      <el-table-column prop="userRoles" label="userRoles"></el-table-column>
      <el-table-column prop="userGroups" label="userGroups"></el-table-column>
      <el-table-column prop="param" label="param"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button size="mini" plain type="primary" @click="editHost(scope.row)">编辑</el-button>
          <!-- <el-button size="mini" plain type="danger">删除</el-button> -->
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
        <!-- 分页 -->

      <!-- 这里是dialog -->
  <el-dialog  :visible.sync="addDialogVisiable" title="新建项目" @open="openDialog()">
    <el-form ref="userForm" :model="userForm" label-width="80px" :rules="hostRules">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="userForm.username" autocomplete="off" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="别名" prop="userAlias">
        <el-input v-model="userForm.userAlias" autocomplete="off" placeholder="请输入用户别名"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input type="textarea" v-model="userForm.email" autocomplete="off" placeholder="请输入用户邮箱"></el-input>
      </el-form-item>
      <el-form-item label="角色" prop="userRoles">
        <el-input type="textarea" v-model="userForm.userRoles" autocomplete="off" placeholder="请输入用户角色，例：admin_role"></el-input>
      </el-form-item>
        <el-form-item label="分组" prop="userGroups">
        <el-input type="textarea" v-model="userForm.userGroups" autocomplete="off" placeholder="请输入用户分组"></el-input>
      </el-form-item>
      <el-form-item label="参数" prop="param">
        <el-input type="textarea" v-model.trim="userForm.param" autocomplete="off" placeholder="务必输入Json格式的对象,否则为空即可"></el-input>
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
      uuid : sessionStorage.getItem("uuid"),
      total: 1,
      currentPage4: 0,
      formInline: {
        username: "",
        region: "",
      },
      user:[],
      addDialogVisiable:false,
      addProjectButtonLoading:false,
      dialogType : 'edit',
      userForm:{
        username:"",
        password:"",
        email:"",
        userAlias:"",
        userRoles:"",
        userGroups:"",
        param:"",
      },
      hostRules: {
        name: [
          {required: true,message: "请输入环境名称！",trigger: "blur"},
        ],
        host: [
          {required: true,message: "请输入环境host！",trigger: "blur"},
        ]
      }
    };
  },
  mounted(){;
    this.$http.getUser(this.uuid).then(res=>{
      const userForm = res.data
      this.total=userForm.length
      this.user=userForm
    })
  },
  methods: {
    inituserForm(){
      this.userForm={
        name:"",
        host:"",
        description:""
      }
    },
    openDialog(){
      // 清除校验
        this.$nextTick(() => {
            this.$refs["userForm"].clearValidate();
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
      this.inituserForm()
    },
    editHost(user){
      this.dialogType = 'edit'
      this.addDialogVisiable=true
      this.userForm={
        id:user.id,
        username:user.username,
        password:user.password,
        email:user.email,
        userAlias:user.userAlias,
        userRoles:user.userRoles,
        userGroups:user.userGroups,
        param:user.param
      }
    },
    onSubmitAddProject(){
      this.$refs["userForm"].validate(valid=>{
        if(!valid){
          return;
        }
        this.addProjectButtonLoading = true
        this.$http.editUser(this.userForm.id,this.userForm).then(res=>{
          this.addProjectButtonLoading=false
          if(res){
            this.addDialogVisiable=false
            this.inituserForm()
            this.$notify.success("恭喜，信息修改成功")
            const user = res.data
            // this.user=host
            let index = 0
            for(let loop_user of this.user){
              if(loop_user.id == user[index].id){
                // Vue.set(this.host,index,host)
                // 刷新页面
                this.user.splice(index,1,user[0])
                break
              }
              index++
            }
          }
        })

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