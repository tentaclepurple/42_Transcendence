<template>
  <div style="width: 100%; height: 100%">
    <LineChart v-bind="lineChartProps" />
  </div>
</template>

<script>

import { computed, defineComponent, ref } from "vue";
import { LineChart, useLineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import { getData } from "@/stores/api";

Chart.register(...registerables);
export default defineComponent({
  name: "App",
  components: { LineChart },
  props: {
    user_id: {
      type: Number,
      default: 0,
    },
  },
  setup() {
    const dataValues = ref([]);
    const dataLabels = ref([]);
    const toggleLegend = ref(true);

    const testData = computed(() => ({
      labels: dataLabels.value,
      datasets: [
        {
          label: 'Data One',
          fill: false,
          data: dataValues.value,
          pointBackgroundColor: '#2c3e50', // Smooth blue color for the dots
          pointBorderColor: '#2c3e50', // Ensure the border of dots is the same color
          pointRadius: 3, // Adjust point size as needed
          pointHoverBackgroundColor: '#0056b3', // Darker blue when hovering over points
          pointHoverBorderColor: '#0056b3' // Darker blue border for hover effect
        },
      ],
    }));

    const options = computed(() => ({
      responsive: true,
      plugins: {
        legend: {
          position: toggleLegend.value ? "top" : "bottom",
        },
      },
      scales: {
        x: {
          ticks: {
            color: '#000000', // Color for x-axis labels
            },
            },
            y: {
              ticks: {
                color: '#000000', // Color for y-axis labels
                },
                }
              }
            }));

    const { lineChartProps, lineChartRef } = useLineChart({
      chartData: testData,
      options,
    });

    function switchLegend() {
      toggleLegend.value = !toggleLegend.value;
    }

    return {
      switchLegend,
      dataValues,
      dataLabels,
      testData,
      options,
      lineChartRef,
      lineChartProps,
    };
  },
  mounted() {
    this.update_line_chart();
  },
  methods: {
    async update_line_chart() {

      const token = this.$cookies.get('access_token');
      let url = import.meta.env.VITE_APP_BACKEND_URL + '/pong/games/';
      if (this.user_id)
        url += `?user=${this.user_id}`;

      const { data, error } = await getData(url, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (data) {
        this.dataValues = data[0];
        this.dataLabels = data[1];

        if (this.lineChartRef) {
          this.lineChartRef.update();
        }
      } else {
        //console.error(error);
      }

    }
  }
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