<template>
  <div class="container mt-4">
    <b-card title="Tournament Brackets" class="list-card">
      <div class="row" v-for="(tournament, index) in tournaments" :key="tournament.id">
        <!-- Semi-Final 1 -->
        <div class="col-md-4">
          <table class="table-condensed bracket-table">
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[0].winner === tournament.semiFinals[0].player1}]">
                  <div class="form-control bracket-item">{{ tournament.semiFinals[0].player1 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[0].winner === tournament.semiFinals[0].player1 ? 'Winner' : tournament.semiFinals[0].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[0].winner === tournament.semiFinals[0].player2}]">
                  <div class="form-control bracket-item">{{ tournament.semiFinals[0].player2 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[0].winner === tournament.semiFinals[0].player2 ? 'Winner' : tournament.semiFinals[0].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Final -->
        <div class="col-md-4 text-center">
          <table class="table-condensed bracket-table">
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.final.winner === tournament.final.player1}]">
                  <div class="form-control bracket-item">{{ tournament.final.player1 || 'TBD' }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.final.winner === tournament.final.player1 ? 'Winner' : tournament.final.winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
              <td class="col-md-2">vs</td>
              <td>
                <div :class="['input-group', {'winner': tournament.final.winner === tournament.final.player2}]">
                  <div class="form-control bracket-item">{{ tournament.final.player2 || 'TBD' }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.final.winner === tournament.final.player2 ? 'Winner' : tournament.final.winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <!-- Semi-Final 2 -->
        <div class="col-md-4">
          <table class="table-condensed bracket-table">
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[1].winner === tournament.semiFinals[1].player1}]">
                  <div class="form-control bracket-item">{{ tournament.semiFinals[1].player1 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[1].winner === tournament.semiFinals[1].player1 ? 'Winner' : tournament.semiFinals[1].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div :class="['input-group', {'winner': tournament.semiFinals[1].winner === tournament.semiFinals[1].player2}]">
                  <div class="form-control bracket-item">{{ tournament.semiFinals[1].player2 }}</div>
                  <span class="input-group-addon"><span class="badge pull-right">{{ tournament.semiFinals[1].winner === tournament.semiFinals[1].player2 ? 'Winner' : tournament.semiFinals[1].winner ? 'Lost' : 'Playing' }}</span></span>
                </div>
              </td>
            </tr>
          </table>
        </div>
        <hr v-if="index < tournaments.length - 1">
        <td colspan="3" class="text-center">
            <button v-if="tournament.pending_game_id" @click="launchGame(tournament.pending_game_id)" class="btn btn-primary">Launch Game</button>
        </td>
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
      const { data, error } = await getData(import.meta.env.VITE_APP_BACKEND_URL + "/tournament/my_tournaments/", {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (data) {
        //console.log(data);
        this.tournaments = data.map(tournament => ({
          id: tournament.id,
          pending_game_id: tournament.pending_game_id,
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
    },
    launchGame(gameId) {
        this.$router.push("/game/" + gameId);
    }
  }
};
</script>

<style>
.table-condensed {
  width: 100%;
}

.bracket-table {
  width: 100%;
}

.bracket-item {
  width: 100%;
  height: 40px; /* Adjust the height as needed */
  display: flex;
  align-items: center;
}

.input-group-addon {
  display: flex;
  align-items: center;
}

.winner .form-control {
  background-color: #d4edda;
}

.loser .form-control {
  background-color: #f8d7da;
}
</style>