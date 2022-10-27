<script lang="ts" setup>

import { ref } from 'vue';
import { useRouter } from 'vue-router';
const activeIndex = ref('/student')
const router = useRouter();
const handleSelect = (index: string) => {
  // console.log(index);
  router.push({
    path: "/student/" + index,
  })
  activeIndex.value=index
}

</script>

<template>
  <div style="display:block">
    <el-menu mode="horizontal" background-color="rgb(238, 243, 247)"
      text-color="rgb(3, 78, 161)" @select="handleSelect" :default-active="activeIndex">
      <el-menu-item v-for="(i, item) in $route.matched[0].children.slice(0,5)" :key="item" :index=i.path>
        <el-icon>
          <component :is="i.meta?.icon"></component>
        </el-icon>
        {{i.meta?.title}}
      </el-menu-item>
    </el-menu>
  </div>
</template>

<style>
.el-menu-item.is-active {
  background-color: rgba(238, 243, 247,0.1) !important;
}

/* 设置选中el-menu-item时的样式 */
.el-menu-item:hover {
  background-color: rgba(230, 230, 230,0.1) !important;
}

.el-menu .el-menu-item {
  margin: 0 20px;
  width: 300px;
}
</style>
