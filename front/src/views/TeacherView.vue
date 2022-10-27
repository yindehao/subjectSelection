<script setup lang="ts">
import LayoutHeader from '../components/LayoutHeader.vue'
import TeacherMenuBar from '../components/TeacherMenuBar.vue'
</script>

<template>
  <div>
    <LayoutHeader />
    <hr>
    <TeacherMenuBar />
    <RouterView/>
  </div>
</template>

<style>
hr {
  background-color: rgba(159, 190, 225, 0.5);
  border: none;
  height: 1px;
}
</style>