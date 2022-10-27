<script setup lang="ts">
import request from '@/unti/requestApi.js';
import { ElMessage } from 'element-plus';
import { onBeforeMount, ref, Ref } from 'vue';

interface teamRequestInterface {
  team_id: string,
  team_name: string,
  leader_id: string,
  team_leader: string,
  created_time: string,
  status: string,
}
const teamRequest: Ref<teamRequestInterface[]> = ref([]);

interface subjectRequestInterface {
  subject_id: string,
  subject_name: string,
  instructor_name: string,
  origin: string,
  created_time: string,
  status: string,
}
const subjectRequest: Ref<subjectRequestInterface[]> = ref([]);

let studentJsonStr = sessionStorage.getItem('student');
let student = JSON.parse(studentJsonStr!!);

const load = () => {
  //获取小组申请信息
  request.get('/student/team/' + student + '/join_team').then((res: any) => {
    console.log(res);
    if (res.code == 200) {
      teamRequest.value = res.data
      for (let i = 0; i < teamRequest.value.length; i++) {
        let team_id = teamRequest.value[i].team_id
        request.get("/student/teams/" + team_id).then((res: any) => {
          if (res.code == 200) {
            teamRequest.value[i].team_name = res.data.team_name
            teamRequest.value[i].leader_id = res.data.leader_id
            teamRequest.value[i].team_leader = res.data.team_leader
          }
          else {
            console.log('error');
          }
        })
      }
    } else {
      ElMessage({
        message: '获取小组申请信息失败',
        type: 'error',
      })
    }
  })
  //获取选题申请信息
  request.get("/student/team/" + student + "/selected_subject").then((res: any) => {
    console.log(res);
    if (res.code == 200) {
      subjectRequest.value = res.data
      for (let i = 0; i < subjectRequest.value.length; i++) {
        let subject_id = subjectRequest.value[i].subject_id
        request.get("/subjects/" + subject_id).then((res: any) => {
          if (res.code == 200) {
            subjectRequest.value[i].subject_name = res.data.subject_name
            subjectRequest.value[i].instructor_name = res.data.instructor_name
            subjectRequest.value[i].origin = res.data.origin
          }
          else {
            console.log('error');
          }
        })
      }
    } else {
      ElMessage({
        message: '获取选题申请信息失败',
        type: 'error',
      })
    }
  })
}

onBeforeMount(() => {
  load()
})

</script>

<template>
  <div class="request">
    <div class="team">
      <h2>我发出的小组申请</h2>
      <el-scrollbar height="232px">
        <el-table :data="teamRequest" stripe style="width: 100%;" height="220">
          <el-table-column prop="team_id" label="小组号" width="90" />
          <el-table-column prop="team_name" label="小组名称" width="200" />
          <el-table-column prop="leader_id" label="组长学号" width="110"  />
          <el-table-column prop="team_leader" label="组长姓名"  width="130"/>
          <el-table-column prop="created_time" label="申请时间" />
          <el-table-column prop="status" label="申请状态"  width="180"/>
        </el-table>
      </el-scrollbar>
    </div>

    <div class="subject">
      <h2>所在小组发出的选题申请</h2>
      <el-scrollbar height="225px">
        <el-table :data="subjectRequest" stripe style="width: 100%;" height="210">
          <el-table-column prop="subject_id" label="课题ID" width="70" />
          <el-table-column prop="subject_name" label="课题名称" />
          <el-table-column prop="instructor_name" label="导师姓名"   width="130"/>
          <el-table-column prop="origin" label="课题来源"   width="130"/>
          <el-table-column prop="created_time" label="申请时间" />
          <el-table-column prop="status" label="申请状态"  width="180"/>
        </el-table>
      </el-scrollbar>
    </div>
  </div>
</template>


<style scoped lang="less">
.request {
  margin: 0 auto;
  padding: 20px 300px;
  background-color: rgb(238, 243, 247);

  h2 {
    margin: 10px 10px 5px;
    font-size: 18px;
  }

  .team {
    margin-top: 20px;
  }

  .subject {
    margin-top: 20px;
  }
}
</style>