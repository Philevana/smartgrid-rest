<template>
  <div>
    <div style="display:flex;gap:16px;align-items:flex-start;">
      <div style="flex:1;">
        <PriceChart :prices="prices" />
      </div>
      <div style="width:360px;">
        <ThermostatClient
          device-id="house-001"
          :state="deviceState"
          @update-setpoint="onSetpoint"
          @toggle-auto="onToggleAuto"
        />
      </div>
    </div>

    <div style="margin-top:18px;">
      <button @click="refreshAll">刷新数据</button>
      <span style="margin-left:12px;color:#666">上次刷新: {{ lastUpdateDisplay }}</span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import PriceChart from './PriceChart.vue'
import ThermostatClient from './ThermostatClient.vue'

export default {
  components: { PriceChart, ThermostatClient },
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
      // 如果开启自动响应，可在前端决定策略或请求后端开启策略
      if (!deviceState.value) return
      try {
        // 这里示例直接上报到 /report，后端根据字段存储
        await api.reportDevice('house-001', { auto_mode: enable })
        // 重新加载
        await loadDevice()
      } catch (e) { console.error(e) }
    }

    onMounted(async () => {
      await refreshAll()
      // 短轮询：每 15s 刷新价格（示例）
      setInterval(loadPrices, 15000)
    })

    const lastUpdateDisplay = computed(() => lastUpdate.value ? lastUpdate.value.toLocaleTimeString() : '未刷新')

    return { prices, deviceState, refreshAll, onSetpoint, onToggleAuto, lastUpdateDisplay }
  }
}
</script>
