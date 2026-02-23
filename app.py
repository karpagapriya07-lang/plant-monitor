from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

leaf_model = load_model("leaf_model.h5")

@app.route("/predict_leaf", methods=["POST"])
def predict_leaf():
    file = request.files["leaf_image"]
    filepath = os.path.join("static", file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = leaf_model.predict(img_array)
    result = np.argmax(prediction)

    classes = ["Healthy", "Disease"]
    return jsonify({"result": classes[result]})

app = Flask(__name__)

plant_model = joblib.load("plant_model.pkl")

latest_data = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sensor", methods=["POST"])
def receive_data():
    global latest_data

    data = request.get_json()

    soil = data["soil_percentage"]
    temp = data["temperature"]
    hum = data["humidity"]
    light = data["light_value"]

    features = np.array([[soil, temp, hum, light]])
    prediction = plant_model.predict(features)[0]

    latest_data = {
        "soil": soil,
        "temp": temp,
        "hum": hum,
        "light": light,
        "prediction": str(prediction)
    }

    print("UPDATED:", latest_data)
    return jsonify({"status": "success"})

@app.route("/get_data")
def get_data():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)