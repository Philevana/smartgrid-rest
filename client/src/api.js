import axios from 'axios'

//const API_BASE = process.env.VUE_APP_API_BASE || 'http://localhost:5000/api'
const API_BASE = 'http://localhost:5000/api'

const client = axios.create({
  baseURL: API_BASE,
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})

export async function fetchPrices() {
  const r = await client.get('/price')
  return r.data
}

export async function fetchDeviceState(deviceId) {
  const r = await client.get(`/device/${deviceId}/state`)
  return r.data
}

export async function setDeviceSetpoint(deviceId, setpoint) {
  const r = await client.post(`/device/${deviceId}/setpoint`, { setpoint })
  return r.data
}

export async function reportDevice(deviceId, payload) {
  const r = await client.post(`/device/${deviceId}/report`, payload)
  return r.data
}

export async function setLightState(deviceId, { light_on, brightness }) {
  const r = await client.post(`/device/${deviceId}/setlight`, { light_on, brightness })
  return r.data
}

export async function fetchLightState(deviceId) {
  const r = await client.get(`/device/${deviceId}/lightstatus`)
  return r.data
}

export async function fetchAggSummary() {
  const r = await client.get('/agg/summary')
  return r.data
}

export async function fetchWeather() {
  const r = await client.get('/weather')
  return r.data
}

export default {
  fetchPrices,
  fetchDeviceState,
  setDeviceSetpoint,
  setLightState,
  fetchLightState,
  reportDevice,
  fetchAggSummary,
  fetchWeather
}
