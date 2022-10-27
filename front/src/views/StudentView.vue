<script setup lang="ts">
import LayoutHeader from '../components/LayoutHeader.vue'
import MenuBar from '../components/MenuBar.vue'
</script>

<template>
  <div>
    <LayoutHeader />
    <hr>
    <MenuBar />
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