<template>
<!--main-->
<div class="container-fluid">
    <!--upper-->
    <div class="row bg-primary text-white py-4 section-upper">
        <!-- Logout Button Column -->
        <div class="col-2 text-left">
            <button type="button" class="btn btn-warning" @click="handleLogOut">Logout</button>
        </div>
        <div class="col-4 text-center">
            <h2>PONG</h2>
            <p>ft_transcendence</p>
        </div>
    </div>
    <!--mid-->
    <div class="row bg-secondary text-white py-4 section-mid d-flex justify-content-between align-items-between flex-wrap">
        <div class="box p-3" @click="goToProfile">
          <div class="card text-dark">
            <div class="card-body">
              <h5 class="card-title mb-3">Profile</h5>
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <p class="mb-1"><strong>Username:</strong> {{ username }}</p>
                  <p><strong>Email:</strong> {{ email }}</p>
                </div>
                <b-img v-if="avatar" :src="avatar" alt="User Avatar" class="img-thumbnail" width="100"></b-img>
              </div>
            </div>
          </div>
        </div>
      <div class="box p-3">
        <div class="card text-dark">
          <QuickMatch />
        </div>
      </div>
      <div class="box p-3" @click="goToStatistics">
        <div class="card text-dark">
          <div class="card-body">
            <h5 class="card-title">Statistics</h5>
            <p class="card-text">Check your statistics.</p>
          </div>
        </div>
      </div>
      <div class="box p-3" @click="goToCommunity">
        <div class="card text-dark">
          <div class="card-body">
            <h5 class="card-title">Community</h5>
            <p class="card-text">Join the community.</p>
          </div>
        </div>
      </div>
    </div>
    <!--lower-->
    <div class="row bg-dark text-white py-4 section-lower">
        <div class="col text-center">
            <p></p>
            <p>by imontero, jzubizar, lugonzal, mvalient, nlibano-</p>
        </div>
    </div>
</div>
</template>

<script>

import { getData, postData } from '@/stores/api';
import QuickMatch from "@/components/QuickMatch.vue";
import TournamentBrackets from "@/components/TournamentComponent.vue"

export default {
  name: 'UserProfile',
  components: {QuickMatch, TournamentBrackets},
  data() {
    return {
      id: '',
      username: '',
      email: '',
      avatar: '',
      errorMessage: '',
      show: true,
      isTournamentModalVisible: false
    };
  },
  async mounted() {
    await this.getUserInfo();
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
        } else {
          //console.error("error:", error);
          this.errorMessage = 'An error occurred while fetching user info';
        }
    },
    async handleLogOut() {
      
      const refresh = this.$cookies.get("refresh_token");
      const token = this.$cookies.get("access_token");
      if (!refresh)
        return ;

      const payload = {
        "refresh": refresh
      }

      const { data, error } = await postData(import.meta.env.VITE_APP_BACKEND_URL + "/auth/logout/", payload, {
          headers: { Authorization: `Bearer ${token}` }
      });
      
      if (data) {
        this.$cookies.remove("access_token");
        this.$cookies.remove("refresh_token");
        this.$cookies.remove("token_auth");
        this.$store.dispatch('logout');
        this.$router.push("/");
      }
      else {
        //console.error("error:", error);
      }

    },
    tournamentPopUp() {
      this.isTournamentModalVisible = true;
    },
    goToProfile() {
        this.$router.push('/profile');
    },
    goToGame() {
      this.$router.push('/game');
    },
    goToStatistics() {
      this.$router.push('/stats');
    },
    goToCommunity() {
      this.$router.push('/community');
    },
    tournamentPopUp() {
      this.isTournamentModalVisible = true;
    }
  }
};
</script>

<style>
.section-upper {
  height: 15vh;
}

.section-mid {
  height: 70vh;
}

.section-lower {
  height: 15vh;
}

.box {
  flex: 0 0 48%; /* Adjust this width to make sure the boxes are well spaced */
  max-width: 48%; /* Ensure the boxes don't overflow */
  height: 48%; /* Adjust height to ensure proper spacing and alignment */
}

.card {
  width: 100%;
  height: 100%;
}

.card-title {
  border-bottom: 1px solid #ccc; /* Visual separation of title */
  padding-bottom: 10px; /* Spacing under the title */
}

</style>
