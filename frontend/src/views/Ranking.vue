<template>
  <div v-for="user in ranking" :key="user.id" class="mb-4">
    <div class="row bg-secondary text-white mb-2 py-4">
      <!-- User name and elo -->
      <div class="col-md-6 text-center">
        <div class="name">{{ user.username }}</div>
      </div>
      <div class="col-md-6 text-center">
        <div class="elo">{{ user.elo }}</div>
      </div>
    </div>
    <div class="row bg-secondary text-white mb-2 py-4">
      <!-- User t/w/l and pieChart -->
      <div class="col-md-6 text-center">
        <div>{{ user.games_won }}/0/{{ user.game_lost }}</div>
      </div>
    </div>
  </div>

</template>

<script>
  import { getData } from '@/stores/api';
  export default {
    data() {
      return {
        ranking: [],
      };
    },

    mounted() {
      this.getRanking();
    },
    async getRanking() {
      const token = this.$cookies.get('access_token');
      //console.log(token);

      try {
        const { data } = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/statistic/ranking/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.ranking = data;
      } catch (error) {
        //console.log(error);
        this.errorMessage = 'An error occurred while fetching ranking info';
      }
    },
  };
</script>
