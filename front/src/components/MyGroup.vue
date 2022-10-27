<script setup lang="ts">
import { onBeforeMount, reactive, ref } from 'vue';
import request from '@/unti/requestApi.js';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { Search } from '@element-plus/icons-vue'

interface api_team {
  team_id: {
    leader_id: string,
    subject_id: string,
    team_id: string,
    team_name: string,
    version: string,
  },
  team_leader: string,
  teammates: {
    student_id: string,
    student_name: string,
    gender: string,
    student_type: string,
    phone_number: string,
    email: string,
    dept_name: string,
    student_class: string,
  }[]
}

const groupInfo: api_team = reactive({
  team_id: {
    leader_id: "None",
    subject_id: "None",
    team_id: "None",
    team_name: "None",
    version: "None",
  },
  team_leader: "",
  teammates: []
})

const subject_name = ref("")

let studentJsonStr = sessionStorage.getItem('student');
let student = JSON.parse(studentJsonStr!!);

onBeforeMount(() => {
  load()
})

const load = () => {
  request.get("/student/team/" + student, {
  }).then((res: any) => {
    // console.log(res)
    if (res.code === 200) {
      groupInfo.team_id = res.data.team_id
      groupInfo.team_leader = res.data.team_leader
      groupInfo.teammates = res.data.teammates
      noTeam.value = false
      let teammatesNum: number = groupInfo.teammates.length
      // console.log("teammatesNum:"+teammatesNum);
      for (let i: number = 0; i < teammatesNum; i++) {
        // console.log(groupInfo.teammates[i]);
        request.get("/student/id/" + groupInfo.teammates[i].student_id, {
        }).then((res: any) => {
          // console.log(res.data)
          if (res.code == 200) {
            groupInfo.teammates[i] = res.data
            groupInfo.teammates[i].gender = groupInfo.teammates[i].gender ? '男' : '女'
          } else if (res.code == 400) {
            ElMessage({
              message: res.msg,
              type: 'error',
            })
          }
        })
      }

      request.get("/subjects/" + groupInfo.team_id.subject_id).then((res: any) => {
        if (res.code == 200) {
          subject_name.value = res.data.subject_name
        } else {
          ElMessage({
            message: '查找小组选题信息失败！',
            type: 'error',
          })
        }
      })
      // console.log(res)
    } else if (res.code === 401) {
      ElMessage({
        message: '尚未加入小组，请及时加入！',
        type: 'warning',
      })
    }
  })
}

//创建小组
const createGroupForm = reactive({
  group_name: '',
})
const createGroupRules = reactive<FormRules>({
  group_name: [
    { required: true, message: '请输入小组名称！', trigger: 'blur' },
  ],
})

const createGroupView = ref(false)
const createGroupFormRef = ref<FormInstance>()

const createmygroup = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      request.put("/student/team/" + student, {
        team_name: createGroupForm.group_name
      }).then((res: any) => {
        if (res.code == 200) {
          // console.log(res.data);
          //清空创建小组表单
          createGroupForm.group_name = ""
          //传小组信息
          groupInfo.team_id = res.data.team_id
          groupInfo.team_leader = res.data.team_leader
          groupInfo.teammates = res.data.teammates
          noTeam.value = false
          load()
        } else if (res.code == 402) {
          // console.log(res.msg);
          ElMessage({
            message: '已在小组中请勿重复加入！',
            type: 'error',
          })
        } else {
          ElMessage({
            message: '创建失败！',
            type: 'error',
          })
        }
        createGroupView.value = false
      })
    } else {
      console.log('error submit!', fields)
    }
  })
}

//编辑组名
const editGroupNameForm = reactive({
  group_name: "",
})
const editGroupNameRules = reactive<FormRules>({
  group_name: [
    { required: true, message: '请输入小组名称！', trigger: 'blur' },
  ],
})

const editGroupNameView = ref(false)
const editGroupNameFormRef = ref<FormInstance>()

const editGroupName = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      request.post("/student/team/" + student, {
        team_name: editGroupNameForm.group_name
      }).then((res: any) => {
        if (res.code == 200) {
          // console.log(res.data);
          //清空创建小组表单
          editGroupNameForm.group_name = ""
          load()
          ElMessage({
            message: '修改成功！',
            type: 'success',
          })
        } else {
          ElMessage({
            message: '修改失败！',
            type: 'error',
          })
        }
        editGroupNameView.value = false
      })
    } else {
      console.log('error submit!', fields)
    }
  })
}

//搜索已有小组
interface api_allTeams {
  groupInfo: {
    leader_id: string,
    subject_id: string,
    team_id: string,
    team_name: string,
    team_leader: string,
    version: string,
  }[]
}

const allGroupInfo: api_allTeams = reactive({
  groupInfo: []
})
// console.log(allGroupInfo);

const searchGroupForm = reactive({
  search_method: "leader_id",
  search_value: ""
})
const searchGroupFormRules = reactive<FormRules>({
  search_method: [
    { required: true, message: '请选择搜索方式！', trigger: 'blur' },
  ],
  search_value: [
    { required: true, message: '请输入搜索所需要的信息！', trigger: 'blur' },
  ],
})

const searchGroupView = ref(false)
const searchGroupFormRef = ref<FormInstance>()

const search = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (searchGroupForm.search_method == "leader_id") {
        request.get("/student/team", {
          params: {
            student_id: searchGroupForm.search_value
          }
        }).then((res: any) => {
          // console.log(res.data);
          allGroupInfo.groupInfo = res.data
        })
      } else if (searchGroupForm.search_method == "leader_name") {
        request.get("/student/teams", {
          params: {
            student_name: searchGroupForm.search_value
          }
        }).then((res: any) => {
          // console.log(res.data)
          allGroupInfo.groupInfo = res.data
        })
      } else {
        console.log("error");

      }
    } else {
      console.log('error submit!', fields)
    }
  })
}

//加入小组
const pickedGroup = ref()
//获得选中的小组信息
const handlePickedGroup = (val: api_allTeams) => {
  pickedGroup.value = val
  // console.log(pickedGroup.value.team_id);
  // console.log(student)
}

// 退出小组后重新加入 之前申请记录没有被覆盖
const joinGroup = () => {
  // console.log(typeof(pickedGroup.value.team_id));
  request.post("/student/team/" + student + '/join', {
    team_id: pickedGroup.value.team_id
  }).then((res: any) => {
    if (res.code == 200) {
      // console.log(res.data);
      searchGroupForm.search_method = ""
      searchGroupForm.search_value = ""
      allGroupInfo.groupInfo = []
      ElMessage({
        message: res.msg,
        type: 'success',
      })
      searchGroupView.value = false
      load()
    } else if (res.code == 400) {
      // console.error(res);
      ElMessage({
        message: res.msg,
        type: 'error',
      })
    }
  })
}

//退出小组
const exitGroupView = ref(false)

const exitGroup = async () => {
  if (student === groupInfo.team_leader) {
    // console.log("组长");
    request.delete("/student/team/" + student,).then((res: any) => {
      if (res.code == 200) {
        ElMessage({
          message: res.msg,
          type: 'success',
        })
        exitGroupView.value = false
        groupInfo.team_id = {
          leader_id: "None",
          subject_id: "None",
          team_id: "None",
          team_name: "None",
          version: "None",
        };
        groupInfo.team_leader = ""
        groupInfo.teammates = []
        noTeam.value = true
        load()
      } else {
        console.log("error");
      }
    })
  } else {
    console.log("组员");
    request.post("/student/team/" + student + '/quit',).then((res: any) => {
      if (res.code == 200) {
        ElMessage({
          message: res.msg,
          type: 'success',
        })
        exitGroupView.value = false
        groupInfo.team_id = {
          leader_id: "None",
          subject_id: "None",
          team_id: "None",
          team_name: "None",
          version: "None",
        };
        groupInfo.team_leader = ""
        groupInfo.teammates = []
        noTeam.value = true
        load()
      } else {
        console.log("error");
      }
    })
  }
}

const noTeam = ref(true);
</script>

<template>
  <div class="group">


    <el-dialog v-model="createGroupView" title="创建小组" width="30%" align-center>
      <el-form :model="createGroupForm" label-width="100px" :rules="createGroupRules" ref="createGroupFormRef">
        <el-form-item label="小组名称" prop="group_name">
          <el-input v-model="createGroupForm.group_name" style="width: 250px;" clearable />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createGroupView = false">取消</el-button>
          <el-button type="primary" @click="createmygroup(createGroupFormRef)">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="editGroupNameView" title="编辑组名" width="30%" align-center>
      <el-form :model="editGroupNameForm" label-width="100px" :rules="editGroupNameRules" ref="editGroupNameFormRef">
        <el-form-item label="小组名称" prop="group_name">
          <el-input v-model="editGroupNameForm.group_name" style="width: 250px;" clearable />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editGroupNameView = false">取消</el-button>
          <el-button type="primary" @click="editGroupName(editGroupNameFormRef)">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="searchGroupView" title="搜索小组" width="60%" align-center>
      <el-form :model="searchGroupForm" :rules="searchGroupFormRules" ref="searchGroupFormRef" inline="true">
        <el-form-item label="搜索方式" prop="search_method" label-width="130px">
          <el-radio-group v-model="searchGroupForm.search_method">
            <el-radio label="leader_id">组长学号</el-radio>
            <el-radio label="leader_name">组长姓名</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="组长学号/姓名" prop="search_value" label-width="200px">
          <el-input v-model="searchGroupForm.search_value" style="width: 150px;" clearable />
        </el-form-item>
        <el-button style="vertical-align: top;" type="primary" plain @click="search(searchGroupFormRef)">
          <el-icon>
            <Search />
          </el-icon>
        </el-button>
      </el-form>
      <!-- <div style="padding-left: 20px;font-size: 13px;color: red">优先使用组长学号进行搜索！</div> -->
      <div style="padding-left: 20px;">
        <el-table :data="allGroupInfo.groupInfo" style="width: 100%" highlight-current-row
          @current-change="handlePickedGroup">
          <el-table-column prop="team_id" label="小组号" />
          <el-table-column prop="team_name" label="小组名称" />
          <el-table-column prop="leader_id" label="组长学号" />
          <el-table-column prop="team_leader" label="组长姓名" />
          <el-table-column prop="subject_id" label="选题ID" />
        </el-table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="searchGroupView = false">取消</el-button>
          <el-button type="primary" @click="joinGroup()">
            加入
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="exitGroupView" title="退出小组" width="30%" align-center>
      <span style="padding-left: 10px; font-size: 16px;">确定退出小组吗？</span>
      <br>
      <span style="padding-left: 10px; font-size: 10px; color: red;">如果你是队长，该小组将被解散！</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="exitGroupView = false">取消</el-button>
          <el-button type="primary" @click="exitGroup()">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-card style="margin: 10px 50px 20px 50px;padding:20px 30px 0px 30px;background-color: rgba(238, 243, 247, 0.6);">
      <h2 style="text-align: center; margin-bottom: 10px">小组基本信息</h2>
      <div style="margin-bottom: 20px">
        <el-descriptions :column="4" border>
          <el-descriptions-item>
            <template #label>
              小组号
            </template>
            {{ groupInfo.team_id.team_id }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              小组名称
            </template>
            {{ groupInfo.team_id.team_name }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <h3 style="margin:10px 0 5px 0">小组成员信息</h3>
      <el-scrollbar height="200px">
        <div class="teammates">
          <el-table :data="groupInfo.teammates" style="width: 100%" title="小组成员信息">
            <el-table-column prop="student_id" label="学号" width="130" />
            <el-table-column prop="student_name" label="姓名" width="100" />
            <el-table-column prop="gender" label="性别" width="70" />
            <el-table-column prop="dept_name" label="院系" />
            <el-table-column prop="student_class" label="班级" />
            <el-table-column prop="phone_number" label="手机号码" />
            <el-table-column prop="email" label="Email" />
          </el-table>
        </div>
      </el-scrollbar>
      <!-- FIXME 所选课题显示的是申请的选题而非申请通过的选题 -->
      <h3 style="margin:10px 0 5px 0">小组选题信息</h3>
      <div style="margin-bottom: 10px">
        <el-descriptions :column="4" border>
          <el-descriptions-item>
            <template #label>
              所选课题ID
            </template>
            {{ groupInfo.team_id.subject_id }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              所选课题名称
            </template>
            {{ subject_name }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <div v-if="noTeam">
        <div class="groupbtn">
          <el-button type="primary" plain @click="createGroupView = true">创建小组</el-button>
          <el-button type="warning" plain @click="searchGroupView = true">加入小组</el-button>
        </div>
      </div>
      <div v-else>
        <div class="groupbtn">
          <el-button type="primary" plain @click="editGroupNameView = true">编辑组名</el-button>
          <el-button type="danger" plain @click="exitGroupView = true">退出小组</el-button>
        </div>
      </div>
    </el-card>

  </div>
</template>


<style scoped lang="less">
.group {
  margin: 0 auto;
  padding: 10px 150px 10px 150px;
  background-color: rgb(238, 243, 247);
}

.groupbtn {
  margin: 17px 0 10px 0;
  padding: 5px 0px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.dialog-footer button:first-child {
  margin-right: 10px;
}

.teammates {
  margin: 10px 0;

}
</style>