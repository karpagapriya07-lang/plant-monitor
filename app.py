from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Store latest sensor data
sensor_data = {
    "temperature": 0,
    "humidity": 0,
    "soil_percentage": 0,
    "light_value": 0,
    "timestamp": ""
}

# ------------------------------
# Home Page
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------
# ESP32 sends sensor data here
# ------------------------------
@app.route("/sensor", methods=["POST"])
def receive_sensor_data():
    global sensor_data
    data = request.get_json()

    sensor_data["temperature"] = data.get("temperature", 0)
    sensor_data["humidity"] = data.get("humidity", 0)
    sensor_data["soil_percentage"] = data.get("soil_percentage", 0)
    sensor_data["light_value"] = data.get("light_value", 0)
    sensor_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Received:", sensor_data)

    return jsonify({"status": "success"})


# ------------------------------
# Frontend fetches live data
# ------------------------------
@app.route("/get_data")
def get_data():
    return jsonify(sensor_data)


# ------------------------------
# Simple Plant Health Logic
# ------------------------------
@app.route("/predict_health")
def predict_health():
    soil = sensor_data["soil_percentage"]
    temp = sensor_data["temperature"]

    if soil < 30:
        result = "Plant needs water 💧"
    elif temp > 35:
        result = "Temperature too high ☀️"
    else:
        result = "Plant looks healthy 🌿"

    return jsonify({"prediction": result})


# ------------------------------
# Leaf Upload (Simple Dummy)
# ------------------------------
@app.route("/predict_leaf", methods=["POST"])
def predict_leaf():
    if 'file' not in request.files:
        return jsonify({"prediction": "No file uploaded"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"prediction": "No file selected"})

    # Save file (optional)
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Dummy prediction
    return jsonify({"prediction": "Leaf looks healthy 🌿 (Demo Mode)"})


# ------------------------------
# Required for Render
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)