<template>
  <el-card shadow="hover">
    <template #header>
      <span>thermostat — {{ deviceId }}</span>
    </template>

    <div v-if="!state">
      <el-empty description="loading..." />
    </div>

    <div v-else>
      <el-descriptions border column="1" size="small">
        <el-descriptions-item label="Current Temperature">
          <el-tag type="info">{{ state.measured_temp }} °C</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Set Point">
          <el-input-number v-model="localSetpoint" :min="15" :max="30" step="0.5" />
          <el-button type="primary" size="small" @click="applySetpoint">Set</el-button>
        </el-descriptions-item>

        <el-descriptions-item label="Mode">
          <el-switch
            v-model="autoMode"
            active-text="Auto"
            inactive-text="Manual"
            @change="toggleAuto"
          />
        </el-descriptions-item>
      </el-descriptions>

      <div style="margin-top:10px;font-size:12px;color:#999;">
        Last Update Time: {{ lastUpdated }}
      </div>
    </div>
  </el-card>
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

    function applySetpoint() {
      emit('update-setpoint', localSetpoint.value)
    }

    function toggleAuto() {
      emit('toggle-auto', autoMode.value)
    }

    const lastUpdated = computed(() =>
      props.state?.updated_at ? new Date(props.state.updated_at).toLocaleString() : '—'
    )

    return { localSetpoint, autoMode, applySetpoint, toggleAuto, lastUpdated }
  }
}
</script>
