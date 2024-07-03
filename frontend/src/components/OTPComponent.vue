<template>
  <div class="modal" @click.self="closeModal">
    <div class="modal-content">
      <div class="otp-container">
        <input ref="input0" type="text" v-model="otp[0]" maxlength="1" @input="focusNext(1)" autofocus>
        <input ref="input1" type="text" v-model="otp[1]" maxlength="1" @input="focusNext(2)">
        <input ref="input2" type="text" v-model="otp[2]" maxlength="1" @input="focusNext(3)">
        <input ref="input3" type="text" v-model="otp[3]" maxlength="1" @input="focusNext(4)">
        <input ref="input4" type="text" v-model="otp[4]" maxlength="1" @input="focusNext(5)">
        <input ref="input5" type="text" v-model="otp[5]" maxlength="1" @input="focusNext(null)">
      </div>
      <p></p>
      <button class="btn btn-success" @click="submitOTP">Verify OTP</button>
      <p></p>
      <p v-if="errorMessages" class="text-danger">{{ errorMessages }}</p>
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { postData } from '@/stores/api';

export default {
  props: {
    username: String,
    password: String
  },
  name: 'Modal',
  emits: ['close'],
  data() {
    return {
      otp: Array(6).fill(''),
      errorMessages: ''
    };
  },
  mounted() {
    //mounted
  },
  methods: {
    async submitOTP() {

      const otpCode = this.otp.join(''); // Join the array to form the OTP code
      const payload = {
        username: this.username,
        password: this.password,
        code: otpCode
      };

      const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/auth/login/", payload);
      if (data) {

        this.$cookies.set('access_token', data.access_token, '1h');
        this.$cookies.set('refresh_token', data.refresh_token, '1d');
        this.$cookies.set('token_auth', data.token_auth, '1d');
        this.$store.dispatch('login', data.access_token);

        this.closeModal(); // Optionally close the modal on successful verification
        this.$router.push('/home')

      } else {
        //console.log("OTP verification failed", error || data.message);
        this.errorMessages = error.response.data.error || 'OTP verification failed';
      }
    },
    async closeModal() {
        this.$emit('close');
    },
    focusNext(nextInputIndex) {
      if (nextInputIndex !== null && this.otp[nextInputIndex - 1].length === 1) {
        this.$refs[`input${nextInputIndex}`].focus();
      }
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

.otp-container {
  display: flex;
  justify-content: space-between;
  padding: 10px;
}
.otp-container input {
  width: 40px;
  height: 40px;
  text-align: center;
  font-size: 24px;
  border: 2px solid #ccc;
  border-radius: 4px;
}
</style>