<!-- SignupForm.vue -->
<template>

    <form @submit.prevent="submitForm">
      <input type="text" v-model="username" placeholder="Username" required>
      <input type="email" v-model="email" placeholder="Email" required>
      <input type="password" v-model="password" placeholder="Password" required>
      <button type="submit">Sign Up</button>
    </form>
  </template>
  
  <script>
  export default {
    name: 'SignupForm',
    data() {
      return {
        username: '',
        email: '',
        password: ''
      };
    },
    methods: {
      submitForm() {
        // Handle form submission here
        console.log('Form submitted:', this.username, this.email, this.password);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your CSS styles here */
  </style>
  