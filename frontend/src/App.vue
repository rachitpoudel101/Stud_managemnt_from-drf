<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div class="min-h-screen">
    <Navbar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>
