<script setup>
import SignupForm from './components/SignupForm.vue'
</script>

<template>
  <main>
    <SignupPage />
  </main>
</template>

<script>
import SignupPage from './components/SignupPage.vue'
export default {
  name: 'App',
  components: {
    SignupPage
  }
}
</script>

<style scoped>

</style>
