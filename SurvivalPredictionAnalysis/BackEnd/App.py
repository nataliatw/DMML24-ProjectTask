from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('gradient_boosting_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    passenger_class = int(data['passenger_class'])  # Pastikan ini adalah integer
    age = float(data['age'])  # Pastikan ini adalah float
    family_count = int(data['family_count'])  # Pastikan ini adalah integer
    gender = int(data['gender'])  # Pastikan ini adalah integer
    port = int(data['port'])  # Pastikan ini adalah integer

    # Buat array fitur dalam urutan yang sama dengan data pelatihan
    features = np.array([[passenger_class, age, family_count, gender, port]])
    
    # Lakukan prediksi
    prediction = model.predict(features)

    # Return hasil prediksi
    return jsonify({'prediction': 'You Will Survive' if prediction[0] == 1 else 'You Will Not Survive'})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json(force=True)
    feedback_message = data.get('feedback')
    
    # Save feedback to a file (feedback.txt)
    with open('C:/Users/ASUS/SurvivalPredictionAnalysis/feedback.txt', 'a') as f:
        f.write(feedback_message + '\n')
    
    return jsonify({'message': 'Feedback received'})

if __name__ == '__main__':
    app.run(debug=True)