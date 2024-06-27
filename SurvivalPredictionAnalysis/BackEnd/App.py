from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('gradient_boosting_model.joblib')

# Load survival insights
with open('C:/Users/ASUS/OneDrive/Dokumen/Universitas/SEMESTER 4/DMML24-ProjectTask/SurvivalPredictionAnalysis/frontend/public/survival_insights.json', 'r') as f:
    survival_insights = json.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    passenger_class = int(data['passenger_class'])
    age = float(data['age'])
    family_count = int(data['family_count'])
    gender = int(data['gender'])
    port = int(data['port'])

    features = np.array([[passenger_class, age, family_count, gender, port]])
    prediction = model.predict(features)

    insights = {
        "gender": survival_insights["gender"],
        "class": survival_insights["class"],
        "age_group": survival_insights["age_group"],
        "family_size": survival_insights["family_size"]
    }

    return jsonify({
        'prediction': 'You Will Survive' if prediction[0] == 1 else 'You Will Not Survive',
        'insights': insights
    })


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