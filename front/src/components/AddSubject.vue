<script setup lang="ts">
import { reactive, ref } from 'vue';
import request from '@/unti/requestApi.js';
import router from '@/router';
import { ElMessage, FormInstance, FormRules } from 'element-plus';

let teacherJsonStr = sessionStorage.getItem('teacher');
let teacher_id = JSON.parse(teacherJsonStr!!);

interface addSubjectInterface {
  id: string,//导师id
  name: string,
  description: string,
  language: string,
  platform: string,
  instructor_name: string,
  min_person: number,
  max_person: number,
  innovation: string,
  max_group: number,
  origin: string,
  created_time: string,
  last_modified_time: string,
  version: string,
}

const subject: addSubjectInterface = reactive({
  id: teacher_id,
  name: "",
  description: "",
  language: "",
  platform: "",
  instructor_name: "",
  min_person: 3,
  max_person: 4,
  innovation: "",
  max_group: 1,
  origin: "导师课题",
  created_time: "",
  last_modified_time: "",
  version: "",
})


const subjectFormRef = ref<FormInstance>()

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入课题名称！', trigger: 'blur' },
  ],
  language: [
    { required: true, message: '请输入开发语言！', trigger: 'blur' },
  ],
  description: [
    { required: true, message: '请输入课题简介！', trigger: 'blur' },
  ],
  origin: [
    { required: true, message: '请选择课题来源！', trigger: 'blur' },
  ],
  min_person: [
    { required: true, message: '请选择小组最小人数限制！', trigger: 'blur' },
  ],
  max_person: [
    { required: true, message: '请选择小组最大人数限制！', trigger: 'blur' },
  ],
  max_group: [
    { required: true, message: '请选择小组数量限制！', trigger: 'blur' },
  ],
})

const addSubject = async (formEl: FormInstance | undefined) => {
  subject.id = teacher_id
  if (!formEl) return
  await formEl.validate(async (valid) => {
    // console.log(valid);
    if (valid) {
      if (subject.min_person <= subject.max_person) {
        request.post("/teacher/subject/post", subject).then((res: any) => {
          if (res.code == 200) {
            ElMessage({
              message: res.msg,
              type: 'success',
            })
            router.push("/teacher")
          } else {
            ElMessage({
              message: "发布失败！",
              type: 'error',
            })
          }
        })
      } else {
        ElMessage({
          message: "小组最小限制人数超过最大限制人数，请重新选择!",
          type: 'error',
        })
      }
    } else {
      ElMessage({
        message: "发布失败！请填入所需要的完整信息！",
        type: 'error',
      })
    }
  })
}

const goBack = () => {
  router.push("/teacher")
}

</script>


<template>
  <div class="subjectbox">
    <h3>发布新的课题</h3>
    <el-scrollbar height="550px" style="padding:0px 20px; margin:3px 0 3px;">
      <div class="subjectdetail">
        <el-form :model="subject" label-width="150px" ref="subjectFormRef" :rules="rules">
          <el-form-item label="课题名称" prop="name">
            <el-input v-model="subject.name" />
          </el-form-item>
          <el-form-item label="开发语言" prop="language">
            <el-input v-model="subject.language" />
          </el-form-item>
          <el-form-item label="开发平台">
            <el-input v-model="subject.platform" />
          </el-form-item>
          <el-form-item label="创新点">
            <el-input v-model="subject.innovation" :rows="3" resize="none" type="textarea" maxlength="300"
              show-word-limit />
          </el-form-item>
          <el-form-item label="课题简介" prop="description">
            <el-input v-model="subject.description" :rows="6" resize="none" type="textarea" maxlength="300"
              show-word-limit />
          </el-form-item>
          <el-form-item label="课题来源" prop="origin">
            <el-radio-group v-model="subject.origin">
              <el-radio label="导师课题" />
              <el-radio label="企业选题" />
            </el-radio-group>
          </el-form-item>
          <el-form-item label="每组最小人数限制" prop="min_person">
            <div style="width: 500px;padding-left: 10px;">
              <el-slider v-model="subject.min_person" :min=1 :max=4 :step=1 />
            </div>
          </el-form-item>
          <el-form-item label="每组最大人数限制" prop="max_person">
            <div style="width: 500px;padding-left: 10px;">
              <el-slider v-model="subject.max_person" :min=1 :max=4 :step=1 />
            </div>
          </el-form-item>
          <el-form-item label="可容纳组数" prop="max_group">
            <div style="width: 500px;padding-left: 10px;">
              <el-slider v-model="subject.max_group" :min=1 :max=4 :step=1 />
            </div>
          </el-form-item>
          <div class="btns">
            <el-form-item>
              <el-button type="primary" plain style="margin:0 50px; width:100px" @click="addSubject(subjectFormRef)">发布
              </el-button>
              <el-button type="info" plain style="margin-left:100px; width:100px" @click="goBack()">返回</el-button>
            </el-form-item>
          </div>
        </el-form>
      </div>
    </el-scrollbar>
  </div>
</template>


<style scoped lang="less">
.subjectbox {
  margin: 0 auto;
  background-color: rgb(238, 243, 247);

  h3 {
    padding-top: 15px;
    text-align: center;
    font-size: 23px;
  }
}

.subjectdetail {
  margin: 0 auto;
  padding: 10px 350px 10px 250px;
}

.btns {
  padding: 15px 0px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.subjectfoot {
  margin: 0 0 0 50px;
  display: flex;
  align-items: center;
  justify-content: space-around;

  span {
    margin: 0 15px;
    font-size: 13px;
  }
}
</style>