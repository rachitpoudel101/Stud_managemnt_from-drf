<script setup>
import Navbar from './components/Navbar.vue';
</script>

<template>
  <div>
    <Navbar />
    <router-view />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  margin: 0;
  padding: 0;
}

.logo {
  display: block;
  margin: 0 auto 1rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding: 0;
    margin: 0;
  }

  .logo {
    margin: 0 1rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    width: 100%;
  }
}

main {
  margin: 0;
  padding: 0;
  width: 100%;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}
</style>
