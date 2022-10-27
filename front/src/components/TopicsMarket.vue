<script setup lang="ts">
import { onMounted, reactive, Ref, ref } from 'vue';
import request from '@/unti/requestApi.js';
import { Search } from '@element-plus/icons-vue'

const formSize = ref('default')

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

let instructor_names = ref([]);
let languages = ref([]);
let origin = ref([]);
let max_person = ref();
let min_person = ref();

//通过后端数据获取
let total = ref(30)


const searchForm = reactive({
  instructor: [],
  language: '',
  origin: [],
  minperson: 1,
  // maxperson: 4,
})

const load = (topicURL: string) => {
  //请求获取指定条件选题
  request.get(topicURL, {
  }).then((res: any) => {
    // console.log(res)
    topics.value = res.data
  })
}

onMounted(() => {
  //请求获取搜索选项
  request.get("/subjects/items", {
  }).then((res: any) => {
    // console.log(res)
    instructor_names.value = res.data.instructor_names;
    languages.value = res.data.languages;
    origin.value = res.data.origin;
    max_person.value = res.data.max_person;
    min_person.value = res.data.min_person;
    // range_person.value=[min_person.value,max_person.value]
    // console.log("res_:"+res.data.instructor_names)
    // console.log("languages:"+languages);
    // console.log("instructor_names:"+instructor_names);
    // console.log("origin:"+origin);
    // console.log("max_person:"+max_person);
    // console.log("min_person:"+min_person);
  })
  //请求获取课题总数
  request.get("/subjects/count", {
  }).then((res: any) => {
    // console.log(res)
    total.value = res
  })
  //请求获取课题
  load("/subjects")
})

// const subText = (text: string) => {
//   const maxLength: number = 200;
//   return (text.length > maxLength) ? text.slice(0, maxLength - 3) + "..." : text;
// }

const submit = () => {
  // console.log(searchForm);
  let requestURL = new URL('http://47.92.33.188:5000/subjects?')
  if (searchForm.instructor != null) {
    for (let i in searchForm.instructor) {
      requestURL.href += 'instructor_name=' + searchForm.instructor[i] + '&'
      // params.append('instructor_name',searchForm.instructor[i])
    }
  }
  if (searchForm.language != '') {
    requestURL.href += 'language=' + searchForm.language + '&'
  }
  if (searchForm.origin != null) {
    for (let i in searchForm.origin) {
      requestURL.href += 'origin=' + searchForm.origin[i] + '&'
    }
  }
  // requestURL.href += 'page_index=' + currentPage.value + '&'
  requestURL.href += 'min_person=' + searchForm.minperson
  // requestURL.href += 'max_person=' + searchForm.maxperson
  // console.log(requestURL)
  load(requestURL.href)
}
</script>

<template>
  <div style="text-align:center; padding:10px 0; background-color: rgb(238, 243, 247);">
    <h2>选题市场</h2>
  </div>
  <div class="search">
    <el-form label-position="right" label-width="100px" :style="{
      maxWidth: '1500px',
      margin: '0 auto',
    }" ref="loginFormRef" :model="searchForm" :size="formSize" status-icon inline="true">
      <el-form-item label="导师姓名">
        <el-select v-model="searchForm.instructor" multiple placeholder="可多选" style="width: 200px;">
          <el-option v-for="instructor in instructor_names" :key="instructor" :label="instructor" :value="instructor" />
        </el-select>
      </el-form-item>
      <el-form-item label="课题来源">
        <el-select v-model="searchForm.origin" multiple placeholder="可多选" style="width: 230px;">
          <el-option v-for="o in origin" :key="o" :label="o" :value="o" />
        </el-select>
      </el-form-item>
      <el-form-item label="开发语言">
        <el-select v-model="searchForm.language" placeholder="请选择" style="width: 100px;">
          <el-option v-for="language in languages" :key="language" :label="language" :value="language" />
        </el-select>
      </el-form-item>
      <el-form-item label="小组人数">
        <div style="width: 200px;padding-left: 10px;">
          <el-slider v-model="searchForm.minperson" :min="min_person" :max="max_person" :step="1" />
        </div>
      </el-form-item>
      <el-button style="vertical-align: top;" type="primary" plain @click="submit">
        <el-icon>
          <Search />
        </el-icon>
      </el-button>
    </el-form>
  </div>
  <div class="bigbox">
    <el-scrollbar height="450px" style="padding:0px 20px 10px; margin:3px 0 5px;">
      <div v-for="topic in topics" :key="topic.subject_id" class="topic">
        <router-link :to="{ name: 'topic', params: { id: topic.subject_id } }">
          <h2>
            {{ topic.subject_name }}
          </h2>
        </router-link>
        <div class="brief">
          <span>导师姓名:{{ topic.instructor_name }}</span>
          <span>选题来源:{{ topic.origin }}</span>
          <span>开发语言:{{ topic.language }}</span>
          <span>小组人数:{{ topic.min_person }}-{{ topic.max_person }}人</span>
        </div>
        <!-- <div class="brief"> -->
        <!-- <span>开发平台:{{topic.platform}}</span> -->
        <!-- <span>最大可容纳组数:{{topic.max_group}}组</span> -->
        <!-- </div> -->
        <!-- <div class="description">
        {{subText(topic.description)}}
      </div> -->
        <hr>
      </div>
    </el-scrollbar>
    <!-- <div class="pagination-block">
      <el-pagination v-model:currentPage="currentPage" v-model:page-size="pageSize" layout="prev, pager, next"
        :total="total"  />
    </div> -->
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