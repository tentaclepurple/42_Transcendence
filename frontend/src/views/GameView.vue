<template>
  <div>
    <Game :game_id="game_id"/>
  </div>
</template>
<script>
import Game from "@/components/Game.vue";

export default {
  components: {Game},
  props: {
    game_id: {
      type: Number,
      default: undefined
    }
  }
}
</script>