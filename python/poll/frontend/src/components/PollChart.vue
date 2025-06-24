<script setup>
import { ref, watch, nextTick } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  pollData: Object
});

const chartData = ref({
  labels: [],
  datasets: [{
    label: '投票数',
    backgroundColor: '#42b883',
    data: []
  }]
});

const chartOptions = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  }
};

// 强制图表在数据更新后重新渲染
const chartKey = ref(0);
const forceRerender = () => {
  chartKey.value += 1;
};

watch(() => props.pollData, (newData) => {
  console.log('图表数据变化:', newData);
  
  if (newData && newData.options) {
    chartData.value.labels = newData.options.map(opt => opt.text);
    chartData.value.datasets[0].data = newData.options.map(opt => opt.votes);
    
    // 强制图表重新渲染
    forceRerender();
  }
}, { immediate: true, deep: true });
</script>

<template>
  <div class="chart-container">
    <Bar :key="chartKey" :data="chartData" :options="chartOptions" />
  </div>
</template>