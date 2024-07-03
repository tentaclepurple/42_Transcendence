<template>
  <div class="modal d-flex align-items-center justify-content-center" @click.self="closeModal">
    <div class="modal-dialog">
      <div class="modal-content border-danger">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title">Confirm Profile Deletion</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
          <p> Are you sure you want to delete your profile? All your data will be deleted forever</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
          <button type="button" class="btn btn-danger" @click="submitDeletion">Delete Profile</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { deleteData, postData } from '@/stores/api';

export default {
  name: 'DeleteModal',
  emits: ['close'],
  data() {
    return {
      password: '',
      errorMessage: ''
    };
  },
  mounted() {
    //mounted
  },
  methods: {
    async submitDeletion() {
      const token = this.$cookies.get('access_token');
      const refresh = this.$cookies.get('refresh_token');
      const refresh_data = {
        "refresh": refresh
      };
      const { data, error } = await deleteData(import.meta.env.VITE_APP_BACKEND_URL + "/users/profile/delete/", {
        headers: { Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'},
          data: JSON.stringify(
            {
              "password":this.password,
              "refresh":refresh
          })
      });
      if (data) {
        this.closeModal(); // Optionally close the modal on successful verification

        this.$cookies.remove("access_token");
        this.$cookies.remove("token_auth");
        this.$store.dispatch('logout');
        this.$router.push("/");
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