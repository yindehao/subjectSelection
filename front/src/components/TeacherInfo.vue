<script setup lang="ts">

import { ElMessage, FormInstance, FormRules } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';
import request from '@/unti/requestApi.js';
import { User, Reading, Iphone, MessageBox, Postcard } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';

const router = useRouter();
const formSize = ref('default')
const instructorInfoRef = ref<FormInstance>()

let teacherJsonStr = sessionStorage.getItem('teacher');
let teacher_id = JSON.parse(teacherJsonStr!!);

const instructorInfo = reactive({
  instructor_name: "",
  username: "",
  gender: "",
  dept_name: "",
  dept_id:"",
  TELE: "",
  Email: "",
  birthday: new Date(),
  description: "",
  title: "",
})

const inputRules = reactive<FormRules>({
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
  request.get("/teacher/id/" + teacher_id, {
  }).then((res: any) => {
    if (res.code == '200') {
      // console.log(res.data)
      instructorInfo.instructor_name = res.data.instructor_name
      instructorInfo.username = res.data.instructor_id
      instructorInfo.gender = res.data.gender
      instructorInfo.dept_name = res.data.dept_name
      instructorInfo.TELE = res.data.phone_number
      instructorInfo.Email = res.data.email
      instructorInfo.birthday = new Date(res.data.birthday)
      instructorInfo.description = res.data.description
      instructorInfo.title = res.data.title
    } else {
      console.log("error")
    }
  })
}

onMounted(() => {
  load()
})

const submit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate(async (valid) => {
    if (valid) {
      instructorInfo.birthday.setHours(instructorInfo.birthday.getHours() + 8);
      await request.post("/teacher/update", instructorInfo).then((res: any) => {
        // console.log(res);
        if (res.code == 200) {
          ElMessage({
            message: res.msg,
            type: 'success',
          })
          router.push("/teacher/info")
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
      <el-form ref="instructorInfoRef" :model="instructorInfo" label-position="right" label-width="auto"
        :size="formSize" status-icon :rules="inputRules">
        <el-descriptions :column="4" border>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              姓名
            </template>
            {{ instructorInfo.instructor_name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              学工号
            </template>
            {{ instructorInfo.username }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              性别
            </template>
            <el-tag size="small">{{ instructorInfo.gender }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <User />
              </el-icon>
              职称
            </template>
            {{ instructorInfo.title }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <el-icon>
                <Reading />
              </el-icon>
              院系
            </template>
            {{ instructorInfo.dept_name }}
          </el-descriptions-item>
        </el-descriptions>
        <el-form-item label="TELE" prop="TELE">
          <el-input clearable v-model="instructorInfo.TELE" :prefix-icon="Iphone"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="Email">
          <el-input clearable v-model="instructorInfo.Email" :prefix-icon="MessageBox"></el-input>
        </el-form-item>
        <el-form-item label="出生日期" prop="birthday">
          <el-date-picker v-model="instructorInfo.birthday" type="date" :default-value="new Date(2000, 9, 1)" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input clearable v-model="instructorInfo.description" :rows="6" resize="none" type="textarea"
            :prefix-icon="Postcard" maxlength="300" show-word-limit />
        </el-form-item>
        <el-form-item>
          <el-button plain type="primary" @click="submit(instructorInfoRef)">修改</el-button>
        </el-form-item>
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
</style>