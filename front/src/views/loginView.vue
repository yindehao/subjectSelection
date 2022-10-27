<script setup lang="ts">

import request from "@/unti/requestApi.js"
import { ElMessage, FormInstance, FormRules } from "element-plus";

import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const formSize = ref('default')
const loginFormRef = ref<FormInstance>()
const loginForm = reactive({
  username: '',
  password: '',
  identity: '学生',
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入账号！', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码！', trigger: 'blur' },
  ],
  identity: [
    {
      required: true,
      message: '请选择登录身份！',
      trigger: 'change',
    },
  ],
})

const submit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      if (loginForm.identity === '学生') {
        // todo 更改后端端口
        request.post("/student/login", loginForm).then((res: any) => {
          // console.log(res)
          if (res.code !== 200) {
            ElMessage({
              message: "账号或密码错误！",
              type: "error"
            })
          }
          else {
            sessionStorage.setItem("student", JSON.stringify(res.data.student_id))//存储用户信息到浏览器
            // console.log(res.data)
            router.push("/student")
          }
        })
      }
      else {
        request.post("/teacher/login", loginForm).then((res: any) => {
          if (res.code == 200) {
            console.log(res)
            sessionStorage.setItem("teacher", JSON.stringify(res.data.instructor_id))//存储用户信息到浏览器
            router.push("/teacher")
          }
          else {
            ElMessage({
              message: "账号或密码错误！",
              type: "error"
            })
          }
        })
      }
    } else {
      console.log('error submit!', fields)
    }
  })
}
</script>


<template>
  <div class="body">
    <div class="title">
      工程实践选题系统
    </div>
    <hr>
    <div class="login"><br>
      <el-card style="width: 450px; margin: 0 auto;background-color: rgba(255, 255, 255, 0.8);">
        <h2 style="padding:10px 0 30px 0;text-align: center;">用户登录</h2>
        <div style="text-align: -webkit-center">
          <el-form label-placement="left" label-width="60px" :style="{
            maxWidth: '300px',
            margin: '0 auto',
          }" ref="loginFormRef" :model="loginForm" :rules="rules" :size="formSize" status-icon>
            <el-form-item label="账号" prop="username">
              <el-input clearable placeholder="请输入账号" v-model="loginForm.username" />
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input clearable show-password type="password" placeholder="请输入密码" v-model="loginForm.password" />
            </el-form-item>
            <el-form-item label="身份" prop="identity">
              <el-radio-group v-model="loginForm.identity">
                <el-radio label="学生" />
                <el-radio label="教师" />
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submit(loginFormRef)">登录</el-button>
            </el-form-item>
          </el-form>
          <br>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.body {
  text-align: -webkit-flex;
  flex-direction: row;
  align-items: center;
  border: 1px solid #c3c3c3;
  background-color: rgb(238, 243, 247);
  width: 100%;
  height: 100%;
}

.title {
  background-color: rgb(238, 243, 247);
  margin: 0 auto;
  padding: 5px 40px;
  font-size: 30px;
  width: 100%;
  height: 80px;
  line-height: 80px;
  color: rgb(3, 78, 161);
  vertical-align: middle;
}

hr {
  background-color: rgba(159, 190, 225, 0.5);
  border: none;
  height: 1px;
}

.login {
  align-content: center;
  padding: 150px 0;
  margin: 0 auto;
}

.el-button {
  margin: 0 auto;
  font-size: 16px;
  text-align: center;
  padding: 0 50px;
}
</style>