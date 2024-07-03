<template>
  <div>
    <ul class="list-group list-group-flush">
      <li v-for="(match, index) in paginatedScores" :key="index" class="list-group-item">
        {{ match.player1 }}: {{ match.score1 }} vs {{ match.player2 }}: {{ match.score2 }} on {{ match.date }}
      </li>
    </ul>
    <nav aria-label="Page navigation">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
        </li>
        <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: page === currentPage }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>

import { getData } from '@/stores/api';
    
export default {
    props: {
        user_id: {
            type: Number,
            default: 0
        }
    },

    data() {
        return {
            scores: [],
            currentPage: 1,
            totalPages: 1,
            itemsPerPage: 8
        }
    },
    computed: {
        paginatedScores() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.scores.slice(start, end);
        }
    },
    mounted() {

        this.getGameList(this.currentPage);

    },
    methods: {
        async getGameList(page) {

            const token = this.$cookies.get("access_token");
            let url = import.meta.env.VITE_APP_BACKEND_URL + "/pong/games/me/";
            if (this.user_id != 0)
                url += `?user=${this.user_id}`;
            const { data, error } = await getData(url, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (data) {
                this.scores = data;
                this.currentPage = page;
                this.totalPages = Math.ceil(data.length / this.itemsPerPage);
            } else {
                //console.error(error);
            }
        },
        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.currentPage = page;
            }
        }
    }
}
</script>