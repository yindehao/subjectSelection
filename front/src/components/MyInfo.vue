<script setup lang="ts">

import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';
import request from '@/unti/requestApi.js';
import { User, Reading, Iphone, MessageBox, Postcard } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';

const router = useRouter();
const formSize = ref('default')
const myInfoRef = ref<FormInstance>()
// // todo  定义学生实体
// let student = {
//   student_id: '',
//   team_id: '',
//   dept_id: '',
//   password: '',
//   phone_number: '',
//   email: '',
//   description: '',
//   gender: '',
//   birthday: new Date(),
//   student_name: '',
//   student_type: '',
//   student_class: '',
//   resume: '',
//   dept_name: '',
// };
let studentJsonStr = sessionStorage.getItem('student');
let student_id = JSON.parse(studentJsonStr!!);

const myInfo = reactive({
  name: "",
  username: "",
  gender: "",
  dept: "",
  class: "",
  TELE: "",
  Email: "",
  birthday: new Date(),
  description: "",
  Type: "",
  teamID: "",
})

const rules = reactive<FormRules>({
  TELE: [
    { required: true, message: '请输入手机号码！', trigger: 'blur' },
  ],
  Email: [
    { required: true, message: '请输入电子邮箱！', trigger: 'blur' },
  ],
  birthday: [
    { required: true, message: '请输入出生日期！', trigger: 'blur' },
  ],
})

const load = () => {
  request.get("/student/id/" + student_id, {
  }).then((res: any) => {
    if (res.code == '200') {
      // console.log(res.data)
      myInfo.name = res.data.student_name
      myInfo.username = res.data.student_id
      myInfo.gender = res.data.gender ? '男' : '女'
      //todo 院系名称显示
      myInfo.dept = res.data.dept_name
      myInfo.class = res.data.student_class
      myInfo.TELE = res.data.phone_number
      myInfo.Email = res.data.email
      myInfo.birthday = new Date(res.data.birthday)
      myInfo.description = res.data.description
      myInfo.Type = res.data.student_type
      myInfo.teamID = res.data.team_id
    } else {
      console.log("error")
    }
  })
}

onMounted(() => {
  load()
})

const submit = async (formEl: FormInstance | undefined) => {
  // console.log(studentJsonStr);
  // console.log(myInfo);
  if (!formEl) return
  await formEl.validate((valid) => {
    if (valid) {
      myInfo.birthday.setHours(myInfo.birthday.getHours() + 8);
      request.post("/student/info", myInfo).then((res: any) => {
        if (res.code == 200) {
          ElMessage({
            message: res.msg,
            type: 'success',
          })
          // sessionStorage.setItem("student", JSON.stringify(res.data))//存储用户信息到浏览器
          router.push("/student/myinfo")
        }
        else {
          ElMessage({
            message: res.msg,
            type: 'error',
          })
        }
      })
    } else {
      ElMessage({
            message: "修改失败！请填入所需要的完整信息！",
            type: 'error',
          })
    }
  })
}

</script>

<template>
  <div class="info">
    <el-card style="margin: 0 50px;padding:0 30px;background-color: rgba(238, 243, 247, 0.6);">
      <h2 style="padding:10px 0 30px 0;text-align: center;">个人信息</h2>
      <el-form ref="myInfoRef" :model="myInfo" label-position="right" label-width="auto" :size="formSize" status-icon
        :rules="rules">
        <el-descriptions :column="3" border>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              姓名
            </template>
            {{ myInfo.name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              学工号
            </template>
            {{ myInfo.username }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              性别
            </template>
            <el-tag size="small">{{ myInfo.gender }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              学生类型
            </template>
            {{ myInfo.Type }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <Reading />
              </el-icon>
              院系
            </template>
            {{ myInfo.dept }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <Reading />
              </el-icon>
              班级
            </template>
            {{ myInfo.class }}
          </el-descriptions-item>
        </el-descriptions>
        <el-form-item label="TELE" prop="TELE">
          <el-input clearable v-model="myInfo.TELE" :prefix-icon="Iphone"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="Email">
          <el-input clearable v-model="myInfo.Email" :prefix-icon="MessageBox"></el-input>
        </el-form-item>
        <el-form-item label="出生日期" prop="birthday">
          <el-date-picker v-model="myInfo.birthday" type="date" :default-value="new Date(2000, 9, 1)" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input clearable v-model="myInfo.description" :rows="6" resize="none" type="textarea"
            :prefix-icon="Postcard" maxlength="300" show-word-limit />
        </el-form-item>
        <!-- <div class="btn"> -->
        <!-- <div class="btn1"> -->
        <el-form-item>
          <el-button plain type="primary" @click="submit(myInfoRef)">修改</el-button>
        </el-form-item>
        <!-- </div> -->
        <!-- <div class="btn1">
            <el-form-item>
              <el-button plain type="info" @click="submit(loginFormRef)">返回</el-button>
            </el-form-item>
          </div> -->
        <!-- </div> -->
      </el-form>
    </el-card>
  </div>
</template>


<style lang="less" scoped>
.info {
  margin: 0 auto;
  padding: 5px 250px;
  display: block;
  align-items: center;
  background-color: rgb(238, 243, 247);
}

.el-descriptions {
  margin: 0 0 30px 0;
}

.el-descriptions-item {
  font-size: 30px;
}


.my-label {
  background: rgb(238, 243, 247);
}

.my-content {
  background: rgb(238, 243, 247);
}


.myInfo {
  display: block;
}

.el-button {
  margin: 5px auto;
  font-size: 16px;
  text-align: center;
  padding: 0 50px;
}

// .btn {
//   margin: 0 30px;
//   padding: 5px;
//   align-content: center;
// }

// .btn1 {
//   display: inline-block;
//   padding: 5px 100px;
// }
</style>