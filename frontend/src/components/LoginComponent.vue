<template>
  <div class="container-fluid d-flex flex-column min-vh-100">
    <!-- Head -->
    <header class="bg-primary text-white py-4 d-flex justify-content-center align-items-center">
      <h1 class="col-12 text-center">Header</h1>
    </header>

    <!-- Main -->
    <main class="flex-grow-1 bg-secondary text-white py-4 d-flex flex-column justify-content-center align-items-center">
      <!-- Message -->
      <div class="text-center mb-4 col-12">
        <h2>Login</h2>
      </div>
      <!-- Login Methods -->
      <div class="w-100 d-flex flex-column align-items-center">
        <div class="form-wrapper w-100 px-3">
          <!-- Email -->
          <p v-if="errorMessage" class="bg-danger p-2">{{ errorMessage }}</p>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" v-model="username">

            <label for="password" class="form-label mt-3">Password</label>
            <input type="password" class="form-control" id="password" v-model="password">
          </div>
          <button class="btn btn-primary mb-3 w-100" @click="submitForm()">OK</button>
          <p class="text-center mb-3">
            Don't have an account? 
            <a href="/register" class="text-white">Register</a>
          </p>
          <!-- Separator -->
          <hr class="w-100 mb-3">
          <!-- OAuth -->
          <div class="text-center">
            <button class="btn btn-secondary" @click="sendAuthRequest">42</button>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <Modal v-if="showModal" :username="username" :password="password" @close="showModal = false">
      <p></p>
      <button class="btn btn-danger" @click="showModal = false">Close Modal</button>
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue';
import { postData } from '@/stores/api';
import Modal from '@/components/OTPComponent.vue'

export default {
  components: {
    Modal
  },
  data() {
    return {
      username: "",
      password: "",
      showModal: false,
      errorMessage: ""
    };
  },
  methods: {
    sendAuthRequest() {
      window.location.href = import.meta.env.VITE_APP_BACKEND_URL + "/oauth/authorize/";
    },
  
    async submitForm() {
        this.errorMessage = '';
        if (!this.username || !this.password) {
          errorMessage.value = "Username and Password are required";
          return;
        }
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('password', this.password);
        //console.log("formData: ", formData.entries());
        const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/twofa/send-code/", formData);
        //console.log(data);
        if (data) {
          //console.log("data: ", data);
          this.showModal = true; // Show the modal when data is received
        } else {
          //console.log("error: ", error);
          this.errorMessage = error.response.data.error || "An error occurred. Please try again.";
        }
      },
  },
}
</script>

<style scoped>
html, body, #app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  background-color: #fff;
}

.container-fluid {
  width: 100%;
  padding: 0;
}

.min-vh-100 {
  min-height: 100vh;
}

.flex-grow-1 {
  flex-grow: 1;
}

.form-wrapper {
  max-width: 500px; /* Set your desired maximum width here */
  width: 100%;
}

.header, .main, .footer {
  width: 100%;
}
</style>