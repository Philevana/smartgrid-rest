<template>
  <div>
    <canvas ref="canvas" style="width:100%;height:260px;"></canvas>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { Chart, LineController, LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip } from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip)

export default {
  props: { prices: { type: Array, default: () => [] } },
  setup(props) {
    const canvas = ref(null)
    let chart = null

    function buildData(prices) {
      const labels = prices.map(p => new Date(p.t).toLocaleTimeString())
      const data = prices.map(p => p.price)
      return { labels, data }
    }

    function renderChart() {
      if (!canvas.value) return
      const { labels, data } = buildData(props.prices)
      if (chart) {
        chart.data.labels = labels
        chart.data.datasets[0].data = data
        chart.update()
        return
      }
      chart = new Chart(canvas.value.getContext('2d'), {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: '电价 (AUD/MWh 或单位)',
            data,
            fill: false,
            tension: 0.2,
            pointRadius: 3
          }]
        },
        options: {
          responsive: true,
          plugins: { title: { display: true, text: '近期电价' } },
          scales: { y: { beginAtZero: false } }
        }
      })
    }

    onMounted(renderChart)
    watch(() => props.prices, renderChart, { deep: true })

    return { canvas }
  }
}
</script>
