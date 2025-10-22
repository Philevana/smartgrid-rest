<template>
  <el-card shadow="hover">
    <template #header>
      <span>thermostat — {{ deviceId }}</span>
    </template>

    <div v-if="!state || !light">
      <el-empty description="loading..." />
    </div>

    <div v-else>
      <el-descriptions border :column="1" size="small">
        <el-descriptions-item label="Current Temperature">
          <el-tag type="info">{{ state.measured_temp }} °C</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="Set Point">
          <el-input-number
            v-model="localSetpoint"
            :min="15"
            :max="30"
            :step="0.5"
          />
          <el-button type="primary" size="small" @click="applySetpoint">
            Set
          </el-button>
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

      <div style="margin-top: 10px; font-size: 12px; color: #999;">
        Last Update Time: {{ lastUpdated }}
      </div>
    </div>
    
    <div style="margin-top: 20px;">
      <el-descriptions border :column="1" size="small">
        <el-descriptions-item label="Light Switch">
          <el-switch
            v-model="localLightOn"
            active-text="ON"
            inactive-text="OFF"
            @change="applyLightChange"
          />
        </el-descriptions-item>

        <el-descriptions-item label="Brightness">
          <el-slider
            v-model="localBrightness"
            :min="0"
            :max="100"
            :step="1"
            show-input
            @change="applyLightChange"
          />
        </el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 10px; font-size: 12px; color: #999;">
        Light On: {{ localLightOn ? "Yes" : "No" }} — Brightness:
        {{ localBrightness }}%
      </div>
    </div>
  </el-card>

</template>

<script>
import { ref, watch, computed } from "vue";

export default {
  props: {
    deviceId: {
      type: String,
      required: true
    },
    state: Object,
    light: Object
  },
  emits: ["update-setpoint", "toggle-auto", "set-light"],
  setup(props, { emit }) {
    const localSetpoint = ref(props.state?.setpoint ?? 22.0);
    const autoMode = ref(props.state?.auto_mode ?? false);
    const localLightOn = ref(props.light?.light_on ?? false);
    const localBrightness = ref(props.light?.brightness ?? 0);

    // Watch for state and light updates
    watch(
      [() => props.state, () => props.light],
      ([newState, newLight]) => {
        if (newState) {
          localSetpoint.value = newState.setpoint;
          autoMode.value = !!newState.auto_mode;
        }
        if (newLight) {
          localLightOn.value = !!newLight.light_on;
          localBrightness.value = newLight.brightness;
        }
      },
      { deep: true, immediate: true }
    );

    function applySetpoint() {
      emit("update-setpoint", localSetpoint.value);
    }

    function toggleAuto() {
      emit("toggle-auto", autoMode.value);
    }

    function applyLightChange() {
      emit("set-light", localLightOn.value, localBrightness.value);
    }

    const lastUpdated = computed(() =>
      props.state?.updated_at
        ? new Date(props.state.updated_at).toLocaleString()
        : "—"
    );

    return {
      localSetpoint,
      autoMode,
      localLightOn,
      localBrightness,
      applySetpoint,
      toggleAuto,
      applyLightChange,
      lastUpdated
    };
  }
};
</script>
