<template>
  <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-secondary">
    <div class="row justify-content-center w-100">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h1 class="card-title text-center mb-4">User Register</h1>
            <form @submit.prevent="submitForm">
              <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                />
              </div>
              <div class="form-group mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="email"
                />
              </div>
              <div class="form-group mb-3">
                <label for="password1" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password1"
                  v-model="password1"
                />
              </div>
              <div class="form-group mb-3">
                <label for="password2" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password2"
                  v-model="password2"
                />
              </div>
              <div class="form-group mb-3">
                <label for="nickname" class="form-label">Nickname</label>
                <input
                  type="text"
                  class="form-control"
                  id="nickname"
                  v-model="nickname"
                />
              </div>
              <div class="form-group mb-4">
                <label for="avatar" class="form-label">Avatar</label>
                <input
                  type="file"
                  class="form-control"
                  id="avatar"
                  @change="onFileChange"
                />
              </div>
              <button type="submit" class="btn btn-primary w-100">Register</button>
              <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { postData } from '@/stores/api';
  export default {
    data() {
      return {
        username: '',
        email: '',
        password1: '',
        password2: '',
        nickname: '',
        avatar: null,
        errorMessage: ''
      };
    },

    methods: {
      onFileChange(event) {
        this.avatar = event.target.files[0];
      },
  
      async submitForm() {
        this.errorMessage = '';
        const formData = new FormData();
        formData.append('username', this.username);
        formData.append('email', this.email);
        formData.append('password1', this.password1);
        formData.append('password2', this.password2);
        formData.append('nickname', this.nickname);
        if (this.avatar) {
          formData.append('avatar', this.avatar);
        }
        const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/auth/registration/', formData);
        //console.log(data);
        if (error) {
          //console.log(error)
          this.errorMessage = this.extractErrorMessage(error.response.data);
        }
        else {
          this.$router.push({ name: 'login' });
        }
      },

      extractErrorMessage(errors) {
        let errorMessage = ''
        for (const key in errors) {
          if (errors[key] && errors[key].length > 0) {
            switch (key) {
              case 'username':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'email':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'password1':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'password2':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'nickname':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'non_field_errors':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              default:
                errorMessage = `An error occurred while registering the user`;
                break;
            }
          }
        }
        return errorMessage.trim();
      }
    }
  };
  </script>

<style scoped>
.container-fluid {
  background-color: #6c757d; /* Bootstrap secondary background color */
}
.card {
  border: none;
}
.card-title {
  font-size: 1.5rem;
}
.form-control {
  box-shadow: none !important;
}
</style>