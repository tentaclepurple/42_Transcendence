<template>
    <div class="col-md-8 d-flex" style="width: 100%; height: 100%;">
      <div class="card w-100">    <!-- Ensures the card expands to fill the flex container -->
        <div class="card-header">
          Ranking
        </div>
        <div class="card-body" style="max-height: 400px; overflow-y: auto;" ref="scrollContainer">
          <ul class="list-group list-group-flush w-100">  <!-- Ensures the list uses full width -->
            <li v-for="(user, index) in users" :key="user.user_id" 
                :class="{ 'highlighted': user.user_id === highlightedUserId }" 
                class="list-group-item d-flex justify-content-between" style="width: 100%;"> <!-- Flex and width adjustment -->
              <div class="ranking-item w-100"> <!-- Ensures the ranking item uses full width -->
                <div class="ranking-item__position">{{ index + 1 }}</div>
                <div class="ranking-item__username">{{ user.username }}</div>
                <div class="ranking-item__elo">{{ user.elo }}</div>
              </div>
            </li>
          </ul>
        </div>
      </div>
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
        users: [],
        highlightedUserId: null,
      };
    },

    mounted() {
    this.getUserInfo();
    this.getRanking();
    },

    methods: {
      async getUserInfo() {
        const token = this.$cookies.get('access_token');
        const { data } = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/users/profile/', {
      headers: { Authorization: `Bearer ${token}` }
        });
        this.highlightedUserId = this.user_id || data.id;
      },

      async getRanking() {
        const token = this.$cookies.get('access_token');
        const { data } = await getData(import.meta.env.VITE_APP_BACKEND_URL + '/statistic/all-user-stats/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.users = data;
        this.scrollToHighlighted();
      },

      scrollToHighlighted() {
        this.$nextTick(() => {
          const container = this.$refs.scrollContainer;
          const highlightedItem = container.querySelector('.highlighted');
          if (highlightedItem) {
            const containerTop = container.scrollTop;
            const containerBottom = containerTop + container.clientHeight;
            const itemTop = highlightedItem.offsetTop;
            const itemBottom = itemTop + highlightedItem.clientHeight;

            if (itemTop < containerTop || itemBottom > containerBottom) {
              container.scrollTop = itemTop - (container.clientHeight / 2) + (highlightedItem.clientHeight / 2);
            }
          }
        });
      }
    },

  
  }
</script>

<style scoped>
  .card-header {
    background-color: #007bff; /* Bootstrap primary color for headers */
    color: #ffffff;            /* White text for better contrast */
  }

  .ranking {
    padding-left: 20px;
  }

  .highlighted {
    background-color: #ffc107;
    font-weight: bold;
  }
  
  .list-group-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .ranking-item {
    display: flex;
    width: 100%;
    justify-content: space-between;
  }

  .ranking-id, .ranking-username, .ranking-elo {
    flex: 1;
    text-align: center;
  }

  .ranking-id {
    flex: 0.5;
  }

</style>