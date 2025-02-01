<script setup>
import sidenav from './components/side-nav.vue'
</script>
<template>
  <div class="row">

    <div class="side-nav">
      <sidenav/>
    </div>
    <div class="content-div">
      <router-view/>  
    </div>
  </div>
</template>

<style scoped>
.side-nav {
  width: 5%;
  height: 95vh;
}
.content-div {
  width: 95%;
}
</style>
