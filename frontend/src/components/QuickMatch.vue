<script>
import {getData, postData} from '@/stores/api';

export default {
  data() {
    return {
      showModal: false,
      show: false,
      textModal: '',
      userId: null,
      users: [],
      selectedUser: null
    };
  },
  async mounted() {

    let data, error;
    const token = this.$cookies.get('access_token');

    ({data, error} = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/user_list/', {
      headers: {Authorization: `Bearer ${token}`}
    }));
    if (data) {
      this.users = data;
    } else {
      //console.error("error:", error);
    }


    ({data, error} = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/profile/', {
      headers: {Authorization: `Bearer ${token}`}
    }));

    if (data) {
      this.userId = data.id;
    } else {
      //console.error("error:", error);
      this.errorMessage = 'An error occurred while fetching user info';
    }
  },
  methods: {
    myTournaments() {
      this.$router.push("/tournaments");
    },
    async createTournament() {
      const token = this.$cookies.get("access_token");
      if (!token)
        return ;

      const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/tournament/create/", "", {
        headers: {Authorization: `Bearer ${token}`}
      });
      if (data)
        this.$router.push("/tournaments");
      //console.error("Cannot create a tournament");
    },
    async createGame() {
      const token = this.$cookies.get('access_token');

      const payload = {
        player1: this.userId,
        player2: this.selectedUser
      }
      const {data, error} = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/pong/games/', payload, {
        headers: {Authorization: `Bearer ${token}`}
      });
      if (data) {
        this.textModal = import.meta.env.VITE_APP_FRONTEND_URL + `/game/${data.id}`;
        this.show = true;
        this.showModal = true;
      } else {
        //console.error("error:", error);
      }
    },
    copyText() {
      navigator.clipboard.writeText(this.textModal);
    }
  }
};
</script>

<template>
  <b-card>
    <b-card-header>
      Quick Match
    </b-card-header>
    <b-card-body>
      <label for="opponent">Choose your opponent:</label>
      <b-form-select id="opponent" v-model="selectedUser">
        <b-form-select-option
            v-for="user in users"
            :key="user.id"
            :value="user.id"
            :disabled="user.id === userId">
          {{ user.username }}
        </b-form-select-option>
      </b-form-select>
      <b-button variant="primary" @click="createGame" :disabled="!selectedUser">Create Game</b-button>
      <b-button variant="primary" @click="myTournaments">My Tournament</b-button>
      <b-button variant="primary" @click="createTournament">Create Tournament</b-button>
    </b-card-body>
  </b-card>

  <div v-if="show">
    <b-modal v-model="showModal" title="Game created successfully" @ok="copyText" hide-footer>
      <b-link :href="textModal" target="_blank">{{ textModal }}</b-link>
      <template #modal-footer>
        <b-button variant="primary" @click="copyText">Copy Link</b-button>
        <b-button variant="secondary" @click="showModal = false">Close</b-button>
      </template>
    </b-modal>
  </div>

</template>

<style scoped>

</style>