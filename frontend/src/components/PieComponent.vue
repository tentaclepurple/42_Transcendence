<template>
  <div style="width: 150px">
    <PieChart v-bind="pieChartProps" />
  </div>
</template>

<script>

import { computed, defineComponent, ref } from "vue";
import { PieChart, usePieChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);
export default defineComponent({
  name: "App",
  components: { PieChart },
  props: {
    wins: Number,
    looses: Number,
  },
  setup(props) {
    const dataValues = ref([props.wins, props.looses]);
    const toggleLegend = ref(true);

    const testData = computed(() => ({
      datasets: [
        {
          data: dataValues.value,
          backgroundColor: [
            "#00EE00",
            "#EE0000",
          ],
        },
      ],
    }));

    const options = computed(() => ({
      plugins: {
        legend: {
          position: toggleLegend.value ? "top" : "bottom",
        },
      },
    }));

    const { pieChartProps, pieChartRef } = usePieChart({
      chartData: testData,
      options,
    });

    function switchLegend() {
      toggleLegend.value = !toggleLegend.value;
    }

    return {
      switchLegend,
      testData,
      options,
      pieChartRef,
      pieChartProps,
    };
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>