<script setup lang="ts">
import { onMounted, Ref, ref } from 'vue';
import request from '@/unti/requestApi.js';


interface subjectInterface {
  subject_id: string,
  subject_name: string,
  description: string,
  language: string,
  platform: string,
  min_person: number,
  max_person: number,
  max_group: number,
  origin: string,
}

const subjects: Ref<subjectInterface[]> = ref([]);

let teacherJsonStr = sessionStorage.getItem('teacher');
let teacher = JSON.parse(teacherJsonStr!!);

const load = () => {
  //请求获取指定条件选题
  request.get("/teacher/subject/list/" + teacher, {
  }).then((res: any) => {
    // console.log(res)
    subjects.value = res.data
  })
}

onMounted(() => {
  //请求获取课题
  load()
})
</script>

<template>
  <div style="text-align:center; padding:10px 0; background-color: rgb(238, 243, 247);">
    <h2>我发布的课题</h2>
  </div>
  <div class="bigbox">
    <el-scrollbar height="510px"
      style="padding:0px 20px 10px; margin:3px 0 5px; background-color: rgba(255,255,255,0.5);">
      <div v-for="subject in subjects" :key="subject.subject_id" class="subject">
        <router-link :to="{ name: 'mysubject', params: { id: subject.subject_id } }">
          <h2>
            {{ subject.subject_id }}.{{ subject.subject_name }}
          </h2>
        </router-link>
        <div class="brief">
          <span>选题来源:{{ subject.origin }}</span>
          <span>开发语言:{{ subject.language }}</span>
          <span>小组人数:{{ subject.min_person }}-{{ subject.max_person }}人</span>
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
  padding: 10px 350px;
  background-color: rgb(238, 243, 247);
}

a {
  color: rgb(1, 40, 85);
  font-size: 13px;
}

.subject {
  padding: 5px;
}

.brief {
  display: flex;
  padding: 5px;

  span {
    font-size: 13px;
    display: inline-block;
    width: 35%;
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