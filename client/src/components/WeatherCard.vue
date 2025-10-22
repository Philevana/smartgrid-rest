<template>
  <el-card shadow="hover" class="weather-card">
    <template #header>
      <div class="card-header">
        <span>{{ weather?.station || 'unknown' }}</span>
        <el-tag size="small" type="info">{{ weather?.time }}</el-tag>
      </div>
    </template>

    <div v-if="!weather">
      <el-empty description="loading..." />
    </div>

    <div v-else>
      <el-row :gutter="10">
        <el-col :span="12">
          <el-statistic title="Air Temperature" :value="weather.air_temp" suffix="°C" />
        </el-col>
        <el-col :span="12">
          <el-statistic title="Sensible Temperature" :value="weather.apparent_temp" suffix="°C" />
        </el-col>
      </el-row>

      <el-divider />

      <el-row :gutter="10">
        <el-col :span="12">
          <el-statistic title="Humidity" :value="weather.humidity" suffix="%" />
        </el-col>
        <el-col :span="12">
          <el-statistic title="Atmospheric Pressure" :value="weather.pressure" suffix="hPa" />
        </el-col>
      </el-row>

      <el-divider />

      <el-descriptions :column="1" border size="small">
        <el-descriptions-item label="Wind Direction">
          {{ weather.wind?.dir }} ({{ weather.wind?.speed_kmh }} km/h, gust {{ weather.wind?.gust_kmh }} km/h)
        </el-descriptions-item>
        <el-descriptions-item label="Weather Phenomena">
          {{ weather.weather || 'Nan' }}
        </el-descriptions-item>
        <el-descriptions-item label="Cloud Coverage">
          {{ weather.cloud || 'Unknown' }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </el-card>
</template>

<script>
import { ref, onMounted } from 'vue'
import api from '../api'

export default {
  name: 'WeatherCard',
  setup() {
    const weather = ref(null)

    async function loadWeather() {
      try {
        const res = await api.fetchWeather()
        weather.value = res
      } catch (err) {
        console.error('Failed to load weather', err)
      }
    }

    onMounted(() => {
      loadWeather()
      setInterval(loadWeather, 300000) // 每 5 分钟刷新
    })

    return { weather }
  }
}
</script>

<style scoped>
.weather-card {
  max-width: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
