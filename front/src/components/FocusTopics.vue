<script setup lang="ts">
import { onMounted, Ref, ref } from 'vue';
import request from '@/unti/requestApi.js';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
const router = useRouter();

interface subjectInterface {
  subject_id: string,
  subject_name: string,
  description: string,
  language: string,
  platform: string,
  instructor_name: string,
  min_person: number,
  max_person: number,
  max_group: number,
  origin: string,
}

const topics:Ref<subjectInterface[]> = ref([]);

let studentJsonStr = sessionStorage.getItem('student');
let student = JSON.parse(studentJsonStr!!);
let team_id = ""


const load = () => {
  request.get("/student/team/" + student, {
  }).then((res: any) => {
    if (res.code === 200) {
      team_id = res.data.team_id.team_id
      request.get("/student/wish_list/" + team_id).then((res: any) => {
        // console.log(res)
        if (res.code == 200) {
          ElMessage({
            message: res.msg,
            type: 'success',
          })
          topics.value = res.data
        } else {
          ElMessage({
            message: "发生错误",
            type: 'error',
          })
        }
      })
    } else if (res.code === 401) {
      ElMessage({
        message: '尚未加入小组，请加入小组后使用选题愿望单！',
        type: 'warning',
      })
      ElMessage({
        message: '即将跳转到选题市场...',
        type: 'warning',
      })
      router.push('/student')
    }
  })
}

onMounted(() => {
  load()
})

</script>

<template>
  <div class="bigbox">
    <div style="text-align:center; padding:10px 0"><h2>小组选题心愿单</h2></div>
    <el-scrollbar height="500px" style="padding:10px 20px; margin:3px 0 5px;background-color:rgba(255, 255, 255, 0.5)">
      <div v-for="topic in topics" :key="topic.subject_id" class="topic">
        <router-link :to="{name:'topic',params:{id:topic.subject_id}}">
          <h2>
            {{topic.subject_id}}.{{topic.subject_name}}
          </h2>
        </router-link>
        <div class="brief">
          <span>导师姓名:{{topic.instructor_name}}</span>
          <span>选题来源:{{topic.origin}}</span>
          <span>开发语言:{{topic.language}}</span>
          <span>小组人数:{{topic.min_person}}-{{topic.max_person}}人</span>
        </div>
        <hr>
      </div>
    </el-scrollbar>
  </div>
</template>


<style scoped lang="less">
.search {
  display: flex;
  margin: 0 auto;
  padding: 5px;
  background-color: rgb(238, 243, 247);
}

.bigbox {
  margin: 0 auto;
  padding: 10px 300px;
  background-color: rgb(238, 243, 247);
}

a {
  color: rgb(1, 40, 85);
  font-size: 13px;
}

.topic {
  padding: 5px;
}

.brief {
  display: flex;
  padding: 5px;

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
  font-size: 14px;
  color: rgba(1, 47, 99, 0.651);
}

.pagination-block {
  margin: 12px auto;
  width: 400px;
}
</style>