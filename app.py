from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Allow frontend

# Load trained model
model = joblib.load("model.pkl")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Backend is healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Prepare feature vector
        features = np.array([[
            data['age'],
            1 if data['gender'] == 'M' else 0,
            data['education'],
            data['ses'],
            data['mmse'],
            data['cdr'],
            data['etiv'],
            data['nwbv'],
            data['asf']
        ]])

        # Predict
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        class_names = ['No Dementia', 'Mild Dementia', 'Moderate Dementia', 'Severe Dementia']

        return jsonify({
            "prediction": class_names[prediction],
            "confidence": float(max(probabilities)),
            "probabilities": {
                class_names[i]: float(prob) for i, prob in enumerate(probabilities)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
