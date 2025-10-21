from flask import Flask, jsonify, request
from flask_cors import CORS
import redis, json
from datetime import datetime
from pathlib import Path
import logging
import sys

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True
app.config['TESTING'] = True

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('flask_debug.log')
    ]
)

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


# ========= Weather API =========
WEATHER_FILE = Path("./weather.json")

@app.route("/api/weather", methods=["GET"])
def get_weather():
    if not WEATHER_FILE.exists():
        return jsonify({"error": "weather.json not found"}), 404

    with open(WEATHER_FILE, "r", encoding="utf-8") as f:
        bom = json.load(f)

    header = bom.get("observations", {}).get("header", [{}])[0]
    data = bom.get("observations", {}).get("data", [])

    latest = data[0] if data else {}

    simplified = {
        "station": header.get("name", latest.get("name")),
        "time": header.get("refresh_message"),
        "air_temp": latest.get("air_temp"),
        "apparent_temp": latest.get("apparent_t"),
        "humidity": latest.get("rel_hum"),
        "pressure": latest.get("press"),
        "wind": {
            "dir": latest.get("wind_dir"),
            "speed_kmh": latest.get("wind_spd_kmh"),
            "gust_kmh": latest.get("gust_kmh"),
        },
        "cloud": latest.get("cloud"),
        "weather": latest.get("weather"),
        "lat": latest.get("lat"),
        "lon": latest.get("lon"),
    }
    return jsonify(simplified)


# ========= Price API =========
@app.route("/api/price", methods=["GET"])
def get_price():
    raw = r.get("prices_json")
    if raw:
        prices = json.loads(raw)
    else:
        prices = []
        for i in range(6):
            prices.append({
                "t": (datetime.utcnow()).isoformat() + "Z",
                "price": 40 + i * 5
            })
        r.set("prices_json", json.dumps(prices))
    return jsonify({"now": now_iso(), "prices": prices})


# ========= Device API =========
@app.route("/api/device/<device_id>/state", methods=["GET"])
def device_state(device_id):
    key = f"device:{device_id}:state"
    raw = r.get(key)
    if raw:
        state = json.loads(raw)
    else:
        state = {
            "device_id": device_id,
            "measured_temp": 24.0,
            "setpoint": 22.0,
            "mode": "manual",
            "auto_mode": False,
            "updated_at": now_iso()
        }
        r.set(key, json.dumps(state))
    return jsonify(state)


@app.route("/api/device/<device_id>/setpoint", methods=["POST"])
def set_setpoint(device_id):
    key = f"device:{device_id}:state"
    body = request.get_json()
    setpoint = float(body.get("setpoint", 22.0))
    raw = r.get(key)
    state = json.loads(raw) if raw else {}
    state.update({
        "device_id": device_id,
        "setpoint": setpoint,
        "updated_at": now_iso()
    })
    r.set(key, json.dumps(state))
    return jsonify(state)


@app.route("/api/device/<device_id>/report", methods=["POST"])
def report_device(device_id):
    key = f"device:{device_id}:state"
    body = request.get_json()
    raw = r.get(key)
    state = json.loads(raw) if raw else {}
    state.update(body)
    state["device_id"] = device_id
    state["updated_at"] = now_iso()
    r.set(key, json.dumps(state))
    return jsonify(state)

@app.route("/api/device/<device_id>/lightstatus", methods=["GET"])
def device_lightstatus(device_id):
    key = f"device:{device_id}:lightstatus"
    raw = r.get(key)
    if raw:
        status = json.loads(raw)
    else:
        status = {
            "device_id": device_id,
            "light_on": False,
            "brightness": 0,
            "updated_at": now_iso()
        }
        r.set(key, json.dumps(status))
    return jsonify(status)


# ========= Aggregated =========
@app.route("/api/agg/summary", methods=["GET"])
def summary():
    keys = r.keys("device:*:state")
    devices = []
    for k in keys:
        raw = r.get(k)
        if raw:
            devices.append(json.loads(raw))
    return jsonify({"devices": devices, "count": len(devices)})


if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0', 
        port=5000,
        use_reloader=True,
        use_debugger=True,
        threaded=True
    )
    