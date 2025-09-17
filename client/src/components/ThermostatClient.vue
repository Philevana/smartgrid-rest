<template>
  <div style="border:1px solid #ddd;border-radius:8px;padding:12px;">
    <h3>恒温器 ({{ deviceId }})</h3>

    <div v-if="!state">加载中...</div>
    <div v-else>
      <div style="margin-bottom:8px;">
        <strong>测温:</strong> {{ state.measured_temp }} °C
      </div>
      <div style="margin-bottom:8px;">
        <strong>当前设定:</strong>
        <input type="number" v-model.number="localSetpoint" step="0.1" />
        <button @click="applySetpoint">应用</button>
      </div>

      <div style="margin-bottom:8px;">
        <label><input type="checkbox" v-model="autoMode" @change="toggleAuto"> 自动响应模式</label>
      </div>

      <div style="margin-top:12px;color:#666;font-size:13px;">
        <div>模式: {{ state.mode || '手动' }}</div>
        <div>上次更新: {{ lastUpdated }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue'

export default {
  props: { deviceId: { type: String, required: true }, state: Object },
  emits: ['update-setpoint','toggle-auto'],
  setup(props, { emit }) {
    const localSetpoint = ref(props.state?.setpoint ?? 22.0)
    const autoMode = ref(props.state?.auto_mode ?? false)

    watch(() => props.state, (s) => {
      if (s) {
        localSetpoint.value = s.setpoint
        autoMode.value = !!s.auto_mode
      }
    })

    async function applySetpoint() {
      emit('update-setpoint', localSetpoint.value)
    }

    function toggleAuto() {
      emit('toggle-auto', autoMode.value)
    }

    const lastUpdated = computed(() => {
      if (!props.state || !props.state.updated_at) return '—'
      return new Date(props.state.updated_at).toLocaleString()
    })

    return { localSetpoint, applySetpoint, autoMode, toggleAuto, lastUpdated }
  }
}
</script>
