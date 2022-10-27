<script lang="ts" setup>
import { onMounted, Ref, ref } from 'vue';
import request from '@/unti/requestApi.js';
import router from '@/router';
import { ElMessage } from 'element-plus';

const props = defineProps({
  id: String,
})

interface subjectInterface {
  subject_id: string,
  subject_name: string,
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

let topic: Ref<subjectInterface> = ref({
  subject_id: "",
  subject_name: "",
  description: "",
  language: "",
  platform: "",
  instructor_name: "",
  min_person: 1,
  max_person: 4,
  innovation: "",
  max_group: 4,
  origin: "",
  created_time: "",
  last_modified_time: "",
  version: "",
})

const load = () => {
  // console.log("props.id", props.id);

  request.get("/subjects/" + props.id, {
  }).then((res: any) => {
    if (res.code == 200) {
      // console.log(res.data)
      topic.value = res.data
    } else {
      ElMessage({
        message: "无法获取课题数据！",
        type: 'error',
      })
    }
  })
}

onMounted(() => {
  load()
})

let studentJsonStr = sessionStorage.getItem('student');
let student = JSON.parse(studentJsonStr!!);
let team_id = ""

// 申请选题
//FIXME 重新申请选题 之前申请记录没有被覆盖
const apply = () => {
  request.get("/student/team/" + student).then((res: any) => {
    if (res.code == 200) {
      if (res.data.team_leader == student) {
        //组长才能申请选题
        let person_num = res.data.teammates.length
        let min_person = topic.value.min_person
        let max_person = topic.value.max_person
        if (person_num >= min_person && person_num <= max_person) {
          request.post("/student/team/" + student + "/select", {
            subject_id: topic.value.subject_id
          }).then((res: any) => {
            console.log(res)
            if (res.code == 200) {
              ElMessage({
                message: res.msg,
                type: 'success',
              })
            }
            else {
              console.log("error");
            }
          })
        } else {
          ElMessage({
            message: "小组人数不符合该课题申请要求！",
            type: 'error',
          })
        }
      } else {
        ElMessage({
          message: "您不是所在小组组长，无法申请选题！",
          type: 'error',
        })
      }
    } else if (res.code == 401) {
      ElMessage({
        message: res.msg,
        type: 'warning',
      })
    } else {
      console.log('error');
    }
  })
}

// 加入心愿单
const addToWish = () => {
  request.get("/student/team/" + student, {
  }).then((res: any) => {
    // console.log(res)
    if (res.code === 200) {
      team_id = res.data.team_id.team_id
      request.put("/student/wish_list/" + team_id, {
        subject_id: topic.value.subject_id
      }).then((res: any) => {
        // console.log(res)
        if (res.code == 200) {
          ElMessage({
            message: res.msg,
            type: 'success',
          })
        }
        else if (res.code == 400) {
          ElMessage({
            message: res.msg,
            type: 'error',
          })
        } else {
          console.log("error");
        }
      })
    } else if (res.code === 401) {
      ElMessage({
        message: '尚未加入小组，无法使用愿望单功能！',
        type: 'warning',
      })
    }
  })
}

// 删除心愿单中的选题
const deleteWish = () => {
  request.get("/student/team/" + student, {
  }).then((res: any) => {
    // console.log(res)
    if (res.code === 200) {
      team_id = res.data.team_id.team_id
      request.delete("/student/wish_list/" + team_id, {
        data: {
          subject_id: topic.value.subject_id
        }

      }).then((res: any) => {
        console.log(res)
        // console.log(topic.value.subject_id)
        if (res.code == 200) {
          ElMessage({
            message: res.msg,
            type: 'success',
          })
        }
        else if (res.code == 400) {
          ElMessage({
            message: res.msg,
            type: 'error',
          })
        } else {
          console.log("error");
        }
      })
    } else if (res.code === 401) {
      ElMessage({
        message: '尚未加入小组，无法使用愿望单功能！',
        type: 'warning',
      })
    }
  })
}

const goBack = () => {
  router.push("/student")
}

</script>

<template>
  <div class="topic">
    <h2>
      {{ topic.subject_name }}
    </h2>
    <div class="brief">
      <span><b>导师姓名:</b>{{ topic.instructor_name }}</span>
      <span><b>选题来源:</b>{{ topic.origin }}</span>
    </div>
    <div class="brief">
      <span><b>开发语言:</b>{{ topic.language }}</span>
      <span><b>开发平台:</b>{{ topic.platform }}</span>
      <span><b>小组人数:</b>{{ topic.min_person }}-{{ topic.max_person }}人</span>
      <span><b>最大可容纳组数:</b>{{ topic.max_group }}组</span>
    </div>
    <el-scrollbar height="320px">
      <div class="description">
        <b>课题描述：</b>{{ topic.description }}
      </div>
      <div class="description">
        <b>项目创新点：</b>{{ topic.innovation }}
      </div>
    </el-scrollbar>
    <div class="brief">
      <span><b>创建时间:</b>{{ topic.created_time }}</span>
      <span><b>最近修改时间:</b>{{ topic.last_modified_time }}</span>
      <span><b>版本号:</b>{{ topic.version }}</span>
    </div>
    <hr>
    <div class="btns">
      <el-button type="primary" plain @click="apply()">申请选题</el-button>
      <el-button type="warning" plain @click="addToWish()">收藏选题</el-button>
      <el-button type="danger" plain @click="deleteWish()">取消收藏</el-button>
      <el-button type="Info" plain @click="goBack()">返回首页</el-button>
    </div>
  </div>
</template>

<style scoped lang="less">
.topic {
  /* margin: 50px 200px; */
  padding: 25px 300px 10px 300px;
  background-color: rgb(238, 243, 247);
  // height: 1000px;

  h2 {
    padding: 30px 0 30px 0;
    text-align: center;
    font-size: 25px;
  }
}

.brief {
  display: flex;
  padding: 0 0 5px 0;

  span {
    font-size: 13px;
    display: inline-block;
    width: 25%;
    text-align: left;
    color: rgba(1, 47, 99, 0.651);
  }
}

.description {
  padding: 10px 0;
  font-size: 16px;
  line-height: 30px;
  color: rgb(2, 37, 78);
}

hr {
  margin: 10px 0 0 0;
}

.btns {
  padding: 15px 0px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
</style>