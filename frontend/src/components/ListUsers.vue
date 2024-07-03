<template>
  <div class="container mt-4">
    <b-card title="Users" class="list-card">
      <ul class="list-group">
        <li v-for="(user, index) in limitedUsers" :key="user.username"
          @click="handleUserClick(user)"
          class="list-group-item d-flex justify-content-between align-items-center custom-list-item">
          <span class="d-flex align-items-center">
            <span :class="['status-circle', user.is_con ? 'bg-success' : 'bg-danger']"></span>
            {{ user.username }}
          </span>
        </li>
      </ul>
    </b-card>

    <b-modal v-if="show" v-model="modalShow" hide-footer>
      <template v-if="state === 'user' && userSelected">
        <div class="text-center">
          <img :src="userSelected.avatar" alt="Avatar" class="rounded-circle mb-3" width="100" height="100">
          <h5>User: {{ userSelected.username }}</h5>
          <span :class="['status-circle', userSelected.is_con ? 'bg-success' : 'bg-danger']"></span>
          <div class="mt-3">
            <button v-if="userSelected.is_con" @click="startChat(userSelected)" class="btn btn-sm btn-primary">Chat</button>
            <button v-if="!isFriend(userSelected)" @click="addFriend(userSelected)" class="btn btn-sm btn-success">Add Friend</button>
            <button v-if="isFriend(userSelected)" @click="removeFriend(userSelected)" class="btn btn-sm btn-danger">Remove Friend</button>
            <button v-if="!userSelected.blocked" @click="blockUser(userSelected)" class="btn btn-sm btn-warning">Block</button>
            <button v-if="userSelected.blocked" @click="unblockUser(userSelected)" class="btn btn-sm btn-secondary">Unblock</button>
          </div>
          <h6 class="mt-4">Friends:</h6>
          <ul>
            <li v-for="friend in userSelected.friends" :key="friend">{{ friend }}</li>
          </ul>
        </div>
      </template>

      <template v-if="state === 'dummy' && userSelected">
        <div class="text-center">
          <PieComponent :wins="wins" :looses="looses" :key="`${wins}-${looses}`"/>
          <LineComponent :user_id="userSelected.id"/>
        </div>
      </template>

      <div class="d-flex justify-content-end mt-3">
        <b-button @click="toggleState">Toggle Content</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { getData, postData } from '@/stores/api';
import { mapState, mapMutations } from 'vuex';
import PieComponent from '@/components/PieComponent.vue';
import LineComponent from '@/components/LineComponent.vue';

export default {
  name: 'ListUsers',
  components: {
    PieComponent,
    LineComponent
  },
  data() {
    return {
      wins: 0,
      totalGames: 0,
      looses: 0,
      users: [],
      selectedUser: null,
      currentUser: null,
      modalShow: false,
      show: false,
      currentUserId: 0,
      state: 'user' // Added state to control modal content
    };
  },
  computed: {
    limitedUsers() {
      return this.filteredUsers.slice(0, 10);
    },
    filteredUsers() {
      return this.users.filter(user => user.username !== 'admin' && user.username !== this.currentUser);
    },
    ...mapState(['userSelected'])
  },
  async mounted() {
    const user_id = await this.getCurrentUser();
    this.getUsers();
    this.getStats(user_id);
  },
  methods: {
    ...mapMutations(['setUserSelected', 'setTriggerChatSocketInit']),
    handleUserClick(user) {
      if (this.currentUser) {
        this.setUserSelected(user);
        this.modalShow = true;
        this.show = true;
        this.state = 'user'; // Show user content
      }
    },
    async getStats(user_id) {
      const token = this.$cookies.get('access_token');

      let url = import.meta.env.VITE_APP_BACKEND_URL + "/statistic/user-stats/";

      if (user_id != 0)
          url += `?user=${user_id}`;
      const { data } = await getData(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (data) {
        this.username = data.username;
        this.elo = data.elo;
        this.wins = data.games_won;
        this.totalGames = data.games_played;
        this.looses = this.totalGames - this.wins        
        return [this.wins, this.totalGames, this.looses];
      }
      return { wins: 0, looses: 0};
    },
    async getCurrentUser() {
      const token = this.$cookies.get('token_auth');
      try {
        const response = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/profile/', {
          headers: { Authorization: `Token ${token}` }
        });
        this.currentUser = response.data.username;
        return response.data.id;
      } catch (error) {
        //console.log(error);
      }
      return 0;
    },
    async getUsers() {
      try {
        const token = this.$cookies.get('token_auth');
        const received = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/user_list/', {
          headers: { Authorization: `Token ${token}` }
        });
        const data = received.data;
        //console.log('User data:', data);
        this.users = data.map(user => ({
          id: user.id,
          username: user.username,
          is_con: user.is_connected,
          avatar: user.avatar,
          friends: user.friends,
          blocked: user.blocked // Ensure blocked property is included if applicable
        }));
      } catch (error) {
        //console.error('Error fetching users:', error);
        this.errorMessage = 'An error occurred while fetching user info';
      }
    },
    toggleState() {
      this.state = this.state === 'user' ? 'dummy' : 'user';
    },
    startChat(user) {
      try {
        this.setTriggerChatSocketInit(true);
        this.modalShow = false; // Close modal after starting chat
      } catch (error) {
        //console.error('Error starting chat:', error);
      }
    },
    async blockUser(user) {
      const token = this.$cookies.get('token_auth');
      try {
        const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/users/block_user/', {
          block_username: user.username
        }, {
          headers: { Authorization: `Token ${token}` }
        });
        if (response.data.success) {
          user.blocked = true; // Update local state on success
        }
      } catch (error) {
        //console.error('Error blocking user:', error);
      }
    },
    async unblockUser(user) {
      const token = this.$cookies.get('token_auth');
      try {
        const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/users/unblock_user/', {
          block_username: user.username
        }, {
          headers: { Authorization: `Token ${token}` }
        });
        if (response.data.success) {
          user.blocked = false; // Update local state on success
        }
      } catch (error) {
        //console.error('Error unblocking user:', error);
      }
    },
    isFriend(user) {
      return this.currentUser && user.friends.includes(this.currentUser);
    },
    async addFriend(user) {
      const token = this.$cookies.get('token_auth');
      try {
        const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/users/add_friend/', {
          friend_username: user.username
        }, {
          headers: { Authorization: `Token ${token}` }
        });
        if (response.data.success) {
          user.friends.push(this.currentUser);
        }
      } catch (error) {
        //console.error('Error adding friend:', error);
      }
    },
    async removeFriend(user) {
      const token = this.$cookies.get('token_auth');
      try {
        const response = await postData(import.meta.env.VITE_APP_BACKEND_URL + '/users/remove_friend/', {
          friend_username: user.username
        }, {
          headers: { Authorization: `Token ${token}` }
        });
        if (response.data.success) {
          const index = user.friends.indexOf(this.currentUser);
          if (index > -1) {
            user.friends.splice(index, 1);
          }
        }
      } catch (error) {
        //console.error('Error removing friend:', error);
      }
    },
  }
};
</script>

<style scoped>
.status-circle {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 10px;
}
.custom-list-item {
  border: none; /* Remove borders */
}
.list-card {
  width: 100%;
  height: 500px;
  border: 1px solid #ccc;
  display: flex;
  flex-direction: column;
  padding: 10px;
}
</style>
