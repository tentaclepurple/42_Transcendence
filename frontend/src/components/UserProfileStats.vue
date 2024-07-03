<template>
  <div class="container">
    <div class="row bg-secondary text-white mb-2 py-4 align-items-center">
      <!-- User name -->
      <div class="col-md-2 text-center d-flex flex-column justify-content-center">
        <font-awesome-icon icon="user" />
        <div class="name h3 pt-3">{{ username }}</div>
      </div>
      <!-- Rank -->
      <div class="col-md-2 text-center d-flex flex-column justify-content-center">
        <font-awesome-icon icon="trophy" />
        <div class="elo h3 pt-3">{{ rank }}</div>
      </div>
      <!-- Elo -->
      <div class="col-md-2 text-center d-flex flex-column justify-content-center">
        <font-awesome-icon icon="star" />
        <div class="elo h3 pt-3">{{ elo }}</div>
      </div>
      <!-- Game stats -->
      <div class="col-md-3 text-center d-flex flex-column justify-content-center">
        <font-awesome-icon icon="gamepad" />
        <div class="h3 pt-3">T:{{ totalGames }} - W:{{ wins }} - L:{{ looses }}</div>
      </div>
      <!-- Pie chart for game stats -->
      <div class="col-md-3 text-center d-flex flex-column justify-content-center">
        <PieComponent :wins="wins" :looses="looses" :key="`${wins}-${looses}`"/>
      </div>
      <!-- Possible extra space or another element -->
      <div class="col-md-3 text-center d-flex flex-column justify-content-center">
        <!-- Optionally, add another element or just an empty div -->
        <div></div>
      </div>
    </div>
  </div>
</template>

<script>

  import PieComponent from '@/components/PieComponent.vue';
  import { getData } from '@/stores/api';

  export default {

    name: 'StatisticsView',
    components: {
      PieComponent,
    },

    props: {
      user_id: {
        type: Number,
        default: 0
      }
    },

    data() {
      
      return {
        username: '',
        elo: 0,
        wins: 0,
        totalGames: 0,
        looses: 0,
        rank: 0
      };
    },

    async mounted() {
      await this.getStats();
      await this.getRankNumber();
    },

    methods: {
      async getStats() {
        const token = this.$cookies.get('access_token');
        let url = import.meta.env.VITE_APP_BACKEND_URL + '/statistic/user-stats/';
        if (this.user_id != 0)
            url += `?user=${this.user_id}`;
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

      async getRankNumber() {
        const token = this.$cookies.get('access_token');
        let url = import.meta.env.VITE_APP_BACKEND_URL + '/statistic/user-rank/';
        if (this.user_id != 0)
            url += `?user=${this.user_id}`;
        const { data } = await getData(url, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (data) {
          this.rank = data;
        }
      }
    },
    watch: {
      wins(newVal) {
        this.$forceUpdate(); // This forces Vue to re-render components which might not be reacting quickly to changes
      }
    }

}

</script>