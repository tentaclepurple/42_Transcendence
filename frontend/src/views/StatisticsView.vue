<template>
  <div class="container">
    <!-- Upper -->
    <div class="row mb-4">
      <div class="col">
        <UserProfileStats :user_id="user_id"/>
      </div>
    </div>
    <!-- Middle -->
    <div class="row">
      <div class="col-md-4 mb-4">
        <div class="bg-secondary p-3">
          <GameRecordComponent :user_id="user_id"/>
        </div>
      </div>
      <div class="col-md-5 mb-4">
        <div class="bg-secondary p-3">
          <LineComponent :user_id="user_id"/>
        </div>
      </div>
      <div class="col-md-3 mb-4 bg-secondary p-3 d-flex align-items-center justify-content-center">
        <RankingComponent :user_id="user_id"/>
      </div>
    </div>
  </div>
</template>

<script>

import PieComponent from '@/components/PieComponent.vue';
import LineComponent from '@/components/LineComponent.vue';
import UserProfileStats from '@/components/UserProfileStats.vue';
import RankingComponent from '@/components/RankingComponent.vue';
import GameRecordComponent from '@/components/GameRecordComponent.vue';

export default {

  name: 'StatisticsView',
  components: {
    PieComponent,
    LineComponent,
    UserProfileStats,
    RankingComponent,
    GameRecordComponent
  },

  props: {
    user_id: {
      type: Number,
      default: 0
    }
  },

}

</script>

<style scoped>
</style>
