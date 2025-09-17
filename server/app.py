from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域

# 连接 Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)


# 工具函数：获取当前时间 ISO 格式
def now_iso():
    return datetime.utcnow().isoformat() + "Z"


# ========== 电价 API ==========

@app.route("/api/price", methods=["GET"])
def get_price():
    raw = r.get("prices_json")
    if raw:
        prices = json.loads(raw)
    else:
        # 如果没有价格，就生成一份示例
        prices = []
        base_price = 40.0
        for i in range(6):
            prices.append({
                "t": (datetime.utcnow()).isoformat() + "Z",
                "price": base_price + i * 5
            })
        r.set("prices_json", json.dumps(prices))
    return jsonify({"now": now_iso(), "prices": prices})


# ========== 设备 API ==========

@app.route("/api/device/<device_id>/state", methods=["GET"])
def device_state(device_id):
    key = f"device:{device_id}:state"
    raw = r.get(key)
    if raw:
        state = json.loads(raw)
    else:
        # 默认状态
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
    # 更新状态
    state.update(body)
    state["device_id"] = device_id
    state["updated_at"] = now_iso()
    r.set(key, json.dumps(state))
    return jsonify(state)


# ========== 聚合 API（可选） ==========

@app.route("/api/agg/summary", methods=["GET"])
def summary():
    keys = r.keys("device:*:state")
    devices = []
    for k in keys:
        raw = r.get(k)
        if raw:
            devices.append(json.loads(raw))
    return jsonify({"devices": devices, "count": len(devices)})


# 入口
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
