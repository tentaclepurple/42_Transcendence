<template>
  <div class="modal" @click.self="closeModal">
    <div class="modal-content">
      <div class="otp-container">
        <b-form>
          <b-form-group id="old-password-group" label="Old Password" label-for="old-password">
            <b-form-input
              ref="input0"
              id="old-password"
              v-model="oldPassword"
              type="password"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group id="password1" label="New Password" label-for="password1">
            <b-form-input
              ref="input1"
              id="password1"
              v-model="password1"
              type="password"
              required
            ></b-form-input>
          </b-form-group>
          
          <b-form-group id="password2" label="Confirm New Password" label-for="password2">
            <b-form-input
              ref="input2"
              id="password2"
              v-model="password2"
              type="password"
              required
            ></b-form-input>
          </b-form-group>

        </b-form>
      </div>
        <button @click="submitChange">Change Password</button>
        <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
        <p></p>
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { postData } from '@/stores/api';

export default {
  name: 'Modal',
  emits: ['close'],
  data() {
    return {
      oldPassword: '',
      password1: '',
      password2: '',
      errorMessage: ''
    };
  },
  mounted() {
    //mounted
  },
  methods: {
    async submitChange() {
      const formData = new FormData();
      formData.append('old_password', this.oldPassword);
      formData.append('new_password1', this.password1);
      formData.append('new_password2', this.password2);

      const token = this.$cookies.get('access_token');
      const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/auth/password/change/", formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (data) {
        this.closeModal(); // Optionally close the modal on successful verification
      } else {
        //console.log(error)
        this.errorMessage = this.extractErrorMessage(error);
      }
    },
    async closeModal() {
        this.$emit('close');
    },
    
    focusNext(nextInputIndex) {
      if (nextInputIndex !== null && nextInputIndex >= 1 && nextInputIndex <= 3) {
        this.$refs[`input${nextInputIndex}`].focus();
      }
    },

    extractErrorMessage(errors) {
        let errorMessage = ''
        for (const key in errors) {
          if (errors[key] && errors[key].length > 0) {
            switch (key) {
              case 'old_password':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'new_password1':
                errorMessage = `${errors[key].join(' ')}\n`;
                break;
              case 'new_password2':
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
}
</script>

<style>
.modal {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  background-color: rgba(0, 0, 0, 0.5); /* Change this to your backdrop color */
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  flex-basis: 600px;
  padding: 16px; /* Change this to your spacing value */
  background-color: white; /* Change this to your white color */
  border-radius: 8px; /* Change this to your border radius */
}

</style>