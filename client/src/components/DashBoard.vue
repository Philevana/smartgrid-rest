<template>
  <!-- 第一行：电价 + 恒温器 -->
  <el-row :gutter="20">
    <el-col :xs="24" :sm="24" :md="14">
      <PriceChart :prices="prices" />
    </el-col>

    <el-col :xs="24" :sm="24" :md="10">
      <ThermostatClient
        device-id="house-001"
        :state="deviceState"
        @update-setpoint="onSetpoint"
        @toggle-auto="onToggleAuto"
      />
    </el-col>
  </el-row>

  <!-- 第二行：天气 + 系统操作 -->
  <el-row :gutter="20" style="margin-top:20px;">
    <el-col :xs="24" :sm="24" :md="14">
      <WeatherCard />
    </el-col>
  </el-row>

  <el-row :gutter="20" style="margin-top:20px;">
    <el-col :xs="24" :sm="24" :md="14">
      <el-card shadow="hover">
        <template #header>
          <span>System Operation</span>
        </template>
        <el-space wrap>
          <el-button type="primary" @click="refreshAll">Refresh Data</el-button>
          <span>Last Refresh Time: {{ lastUpdateDisplay }}</span>
        </el-space>
      </el-card>
    </el-col>
  </el-row>
</template>


<script>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import PriceChart from './PriceChart.vue'
import ThermostatClient from './ThermostatClient.vue'
import WeatherCard from './WeatherCard.vue'

export default {
  name: 'Dashboard',
  components: { PriceChart, ThermostatClient, WeatherCard },
  setup() {
    const prices = ref([])
    const deviceState = ref(null)
    const lastUpdate = ref(null)

    async function loadPrices() {
      try {
        const d = await api.fetchPrices()
        prices.value = d.prices || []
      } catch (e) {
        console.error('fetchPrices', e)
      }
    }

    async function loadDevice() {
      try {
        const s = await api.fetchDeviceState('house-001')
        deviceState.value = s
      } catch (e) {
        console.error('fetchDeviceState', e)
        deviceState.value = null
      }
    }

    async function refreshAll() {
      await Promise.all([loadPrices(), loadDevice()])
      lastUpdate.value = new Date()
    }

    async function onSetpoint(newSetpoint) {
      try {
        const res = await api.setDeviceSetpoint('house-001', newSetpoint)
        deviceState.value = res
      } catch (e) {
        console.error('setDeviceSetpoint', e)
      }
    }

    async function onToggleAuto(enable) {
      try {
        await api.reportDevice('house-001', { auto_mode: enable })
        await loadDevice()
      } catch (e) {
        console.error('toggleAuto', e)
      }
    }

    onMounted(() => {
      refreshAll()
      setInterval(loadPrices, 15000) // 每 15 秒刷新一次电价
    })

    const lastUpdateDisplay = computed(() =>
      lastUpdate.value ? lastUpdate.value.toLocaleTimeString() : '未刷新'
    )

    return { prices, deviceState, refreshAll, onSetpoint, onToggleAuto, lastUpdateDisplay }
  }
}
</script>
