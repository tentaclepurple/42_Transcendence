<template>
  <div class="container mt-4">
    <b-card title="Tournament Brackets" class="list-card">
      <div class="row" v-for="(tournament, index) in tournaments" :key="tournament.id">
        <!-- Semi-Final 1 -->
        <div class="col-md-4">
          <table class="table-condensed" style="width:100%">
            <tr>
              <td class="col-md-5">
                <div :class="['input-group', {'winner': tournament.semiFinals[0].winner === tournament.semiFinals[0].player1}]">
                  <div class="form-control">{{ tournament.semiFinals[0].player1 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[0].winner === tournament.semiFinals[0].player1 ? 'Winner' : tournament.semiFinals[0].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
              <td class="col-md-5" rowspan="2">
                <div class="input-group">
                  <div class="form-control">{{ tournament.final.player1 || 'TBD' }}</div>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[0].winner === tournament.semiFinals[0].player2}]">
                  <div class="form-control">{{ tournament.semiFinals[0].player2 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[0].winner === tournament.semiFinals[0].player2 ? 'Winner' : tournament.semiFinals[0].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Final -->
        <div class="col-md-4 text-center">
          <table class="table-condensed" style="width:100%">
            <tr>
              <td class="col-md-5">
                <div :class="['input-group', {'winner': tournament.final.winner === tournament.final.player1}]">
                  <div class="form-control">{{ tournament.final.player1 || 'TBD' }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.final.winner === tournament.final.player1 ? 'Winner' : tournament.final.winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
              <td class="col-md-2">vs</td>
              <td class="col-md-5">
                <div :class="['input-group', {'winner': tournament.final.winner === tournament.final.player2}]">
                  <div class="form-control">{{ tournament.final.player2 || 'TBD' }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.final.winner === tournament.final.player2 ? 'Winner' : tournament.final.winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Semi-Final 2 -->
        <div class="col-md-4">
          <table class="table-condensed" style="width:100%">
            <tr>
              <td class="col-md-5">
                <div :class="['input-group', {'winner': tournament.semiFinals[1].winner === tournament.semiFinals[1].player1}]">
                  <div class="form-control">{{ tournament.semiFinals[1].player1 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[1].winner === tournament.semiFinals[1].player1 ? 'Winner' : tournament.semiFinals[1].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
              <td class="col-md-5" rowspan="2">
                <div class="input-group">
                  <div class="form-control">{{ tournament.final.player2 || 'TBD' }}</div>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[1].winner === tournament.semiFinals[1].player2}]">
                  <div class="form-control">{{ tournament.semiFinals[1].player2 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[1].winner === tournament.semiFinals[1].player2 ? 'Winner' : tournament.semiFinals[1].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </b-card>
  </div>
</template>

<script>
import { getData } from '@/stores/api';

export default {
  data() {
    return {
      tournaments: []
    };
  },
  mounted() {
    this.getCurrentTournaments();
  },
  methods: {
    async getCurrentTournaments() {
      const token = this.$cookies.get("access_token");
      const { data, error } = await getData(import.meta.env.VITE_APP_BACKEND_URL + "/tournament/current/", {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (data) {
        this.tournaments = data.map(tournament => ({
          id: tournament.id,
          semiFinals: [
            {
              player1: tournament.player1,
              player2: tournament.player2,
              winner: tournament.game1_winner
            },
            {
              player1: tournament.player3,
              player2: tournament.player4,
              winner: tournament.game2_winner
            }
          ],
          final: {
            player1: tournament.game1_winner,
            player2: tournament.game2_winner,
            winner: tournament.final_game_winner
          }
        }));
        //console.log(this.tournaments);
      }
    }
  }
};
</script>

<style scoped>
.custom-list-item {
  cursor: pointer;
}
.winner .form-control {
  background-color: #d4edda;
}
</style>
