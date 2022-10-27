<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import { Remove } from '@element-plus/icons-vue'
import { onBeforeMount, ref } from 'vue';
import request from '@/unti/requestApi.js';

const router = useRouter();

const exit = () => {
  sessionStorage.removeItem("student")
  ElMessage({
    message: "退出成功！",
    type: "success"
  })
  router.push("/login")
}


onBeforeMount(() => {
  let teacherJsonStr = sessionStorage.getItem('teacher');
  let teacher = JSON.parse(teacherJsonStr!!);

  let studentJsonStr = sessionStorage.getItem('student');
  let student = JSON.parse(studentJsonStr!!);

  if (teacher != null) {
    ID.value = teacher
    request.get("/teacher/id/" + teacher).then(((res: any) => {
      if (res.code == 200) {
        name.value = res.data.instructor_name
      } else {
        ElMessage({
          message: "无法获取用户信息！",
          type: 'error',
        })
      }
    }))
  } else if (student != null) {
    ID.value = student
    request.get("/student/id/" + student).then(((res: any) => {
      if (res.code == 200) {
        name.value = res.data.student_name
      } else {
        ElMessage({
          message: "无法获取用户信息！",
          type: 'error',
        })
      }
    }))
  } else {
    ID.value = "未登录"
  }
})

const ID = ref("1111")
const name = ref("2222")

</script>

<template>
  <div class="box">
    <div class="title">
      工程实践选题系统
    </div>

    <span class="loginInfo">当前用户：{{ ID }}&nbsp;&nbsp;{{name}}</span>
    <div class="nbutton">
      <el-button type="error" @click="exit">
        <el-icon>
          <Remove />
        </el-icon>
        退出登录
      </el-button>
    </div>
  </div>
</template>



<style lang="less">
.box {
  // background-color: rgb(3, 78, 161);
  background-color: rgb(238, 243, 247);
  text-align: left;
  // 两元素贴边
  display: flex;
  justify-content: space-between;
  height: 80px;
  color: rgb(3, 78, 161);
}

.title {
  margin: 0 auto;
  padding: 5px 40px;
  font-size: 30px;
  width: 100%;
  height: 80px;
  line-height: 80px;
  vertical-align: middle;
}

.nbutton {
  margin: 30px;
  display: flex;
}

.welcome {
  margin-top: 5px;
  margin-right: 20px;
  font-size: 18px;
  color: rgba(255, 255, 255, 1);
}

.loginInfo{
  margin: 30px 20px;
  width: 350px;
}
</style>
