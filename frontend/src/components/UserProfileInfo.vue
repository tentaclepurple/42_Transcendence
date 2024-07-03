<template>
  <div class="mx-auto flex w-full max-w-sm flex-col">
    <b-container fluid>
      <b-row class="mb-4">
        <b-col>
          <h1 class="text-2xl font-semibold text-white">
            User Profile
          </h1>
          <hr>
        </b-col>
      </b-row>
    </b-container>

    <b-form @submit.prevent="submitForm">
      <div class="form-group">
        <input type="hidden" name="id" v-model="id"/>
      </div>

      <b-form-group id="username-group" label="Username" label-for="username" label-class="text-white" class="mb-4">
        <b-form-input
        type="text"
        id="username"
        v-model.trim="username"
        placeholder="Enter your username"
        required
        />
      </b-form-group>

      <b-form-group id="email-group" label="Email" label-for="email" label-class="text-white" class="mb-4">
        <b-form-input
        type="email"
        id="email"
        v-model.trim="email"
        placeholder="Enter your email"
        required
        />
      </b-form-group>

      <b-form-group id="nickname-group" label="Nickname" label-for="nickname" label-class="text-white" class="mb-4">
        <b-form-input
            type="text"
            id="nickname"
            v-model.trim="nickname"
            placeholder="Enter your nickname"
            required
        />
      </b-form-group>
    
    <b-form-group id="avatar-group" label="Avatar" label-for="avatar" label-class="text-white" class="mb-4">
      <b-row>
        <b-col cols="12">
          <b-img v-if="showAvatar" :src="avatar" fluid thumbnail alt="User Avatar" width="200" class="mb-4"></b-img>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <input
            class="mt-1 rounded border py-1 px-3 text-sm shadow"
            id="avatar"
            type="file"
            @change="onFileChange"
          />
        </b-col>
      </b-row>
    </b-form-group>

      <b-button type="submit" variant="primary" class="me-4">Update Profile</b-button>
      <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
    </b-form>
    <div class="mt-4">
      <b-button type="change" variant="info" @click="showModal = true" class="button_margin">Change Password</b-button>
      <b-button variant="danger" @click="showDeleteModal = true" class="button_margin">Delete Profile</b-button>
      <b-button variant="secondary" @click="cancelForm" class="button_margin">Cancel</b-button>    
    </div>
    <!-- Modal -->
    <Modal v-if="showModal" @close="showModal = false">
      <button @click="showModal = false">Close Modal</button>
    </Modal>
    <DeleteModal v-if="showDeleteModal" @close="showDeleteModal = false">
      <button @click="showDeleteModal = false">Close Modal</button>
    </DeleteModal>
  </div>
</template>

<script>
  import { getData, postData } from '@/stores/api';
  import Modal from '@/components/ChangePassword.vue';
  import DeleteModal from '@/components/DeleteProfileModal.vue';

  export default {
    components: {
      Modal,
      DeleteModal
    },

    data() {
      return {
        id: '',
        username: '',
        email: '',
        nickname: '',
        avatar: null,
        showAvatar: true,
        errorMessage: '',
        showModal: false,
        showDeleteModal: false
      };
    },

  mounted() {
    this.getUserInfo();
  },

  methods: {
    async getUserInfo() {
      const token = this.$cookies.get('access_token');
      const { data, error } = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (data) {
        this.id = data.id;
        this.username = data.username;
        this.email = data.email;
        this.avatar = data.avatar;
        this.nickname = data.nickname;
      } else {
        //console.log(error);
        this.errorMessage = 'An error occurred while fetching user info';
      }
    },

    onFileChange(event) {
      this.showAvatar = null;
      this.avatar = event.target.files[0];
    },
  
    async submitForm() {
      this.errorMessage = '';
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('email', this.email);
      formData.append('nickname', this.nickname);
      if (this.avatar) {
        formData.append('avatar', this.avatar);
      }
      const token = this.$cookies.get('access_token');
      const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/users/update/', formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      //console.log(data);
      if (error) {
        //console.log(error)
        this.errorMessage = this.extractErrorMessage(error.response.data);
      }
      else {
        this.$router.push({ name: 'home' });
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
            case 'non_field_errors':
              errorMessage = `${errors[key].join(' ')}\n`;
              break;
            case 'nickname':
              errorMessage = `${errors[key].join(' ')}\n`;
              break;
            default:
              errorMessage = `An error occurred while registering the user`;
              break;
          }
        }
      }
      return errorMessage.trim();
    },

    cancelForm() {
      //console.log('Cancel button clicked');
      this.$router.push({ name: 'home' });
    }
  },

  };
  </script>
<style>
  .button_margin {
    margin-right: 12px;
  }
</style>