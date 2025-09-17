<template>
  <el-card shadow="hover">
    <template #header>
      <span>Trend of electricity prices</span>
    </template>
    <canvas ref="canvas" style="width:100%;height:300px;"></canvas>
  </el-card>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Filler
} from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Filler)

export default {
  props: { prices: { type: Array, default: () => [] } },
  setup(props) {
    const canvas = ref(null)
    let chart = null

    function buildData(prices) {
      const labels = prices.map(p => new Date(p.t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
      const data = prices.map(p => p.price)
      return { labels, data }
    }

    function renderChart() {
      if (!canvas.value) return
      const ctx = canvas.value.getContext('2d')

      const { labels, data } = buildData(props.prices)

      // 创建渐变色
      const gradient = ctx.createLinearGradient(0, 0, 0, 300)
      gradient.addColorStop(0, 'rgba(64,158,255,0.5)')   // Element Plus 主色
      gradient.addColorStop(1, 'rgba(64,158,255,0.05)')

      if (chart) {
        chart.data.labels = labels
        chart.data.datasets[0].data = data
        chart.update()
        return
      }

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: '电价 (AUD/MWh)',
            data,
            borderColor: '#409EFF',
            backgroundColor: gradient,
            fill: true,
            tension: 0.3,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: '#409EFF'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#409EFF',
              titleColor: '#fff',
              bodyColor: '#fff',
              callbacks: {
                label: ctx => ` Price: ${ctx.parsed.y.toFixed(2)} AUD/MWh `
              }
            },
            title: {
              display: false
            }
          },
          scales: {
            x: {
              ticks: { color: '#666' },
              grid: { color: 'rgba(200,200,200,0.2)' }
            },
            y: {
              ticks: { color: '#666' },
              grid: { color: 'rgba(200,200,200,0.2)' },
              beginAtZero: false
            }
          }
        }
      })
    }

    onMounted(renderChart)
    watch(() => props.prices, renderChart, { deep: true })

    return { canvas }
  }
}
</script>
