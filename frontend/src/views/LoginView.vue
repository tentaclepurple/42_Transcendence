<template>
  <div>
    <div class="flex min-h-screen">
      <div class="flex-1 d-flex flex-column">
        <div class="flex-grow-1 d-flex align-items-center">
          <LoginForm />
        </div>
      </div>
      <div class="hidden flex-1 bg-gray-50 lg:flex">
        <div class="mx-auto d-flex align-items-center">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '../components/LoginComponent.vue'; // Ensure the correct path

export default {
  name: 'LoginView',
  components: {
    LoginForm
  },
  data() {
    return {
      info: null
    };
  },
  async created() {
  }
}
</script>

<style scoped>
/* Ensure full height and remove any global black background */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: #fff;
}
</style>