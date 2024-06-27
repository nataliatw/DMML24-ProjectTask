import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Insights from './component/Insights';

function App() {
  const [passengerClass, setPassengerClass] = useState('');
  const [age, setAge] = useState('');
  const [familyCount, setFamilyCount] = useState('');
  const [gender, setGender] = useState('');
  const [port, setPort] = useState('');
  const [prediction, setPrediction] = useState('');
  const [insights, setInsights] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [feedbackResponse, setFeedbackResponse] = useState('');
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);

  const handlePredict = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict', {
        passenger_class: passengerClass,
        age: age,
        family_count: familyCount,
        gender: gender,
        port: port
      });
      setPrediction(response.data.prediction);
      setInsights(response.data.insights);

      setPassengerClass('');
      setAge('');
      setFamilyCount('');
      setGender('');
      setPort('');
    } catch (error) {
      console.error("There was an error making the request:", error);
    }
  };

  const handleFeedback = async () => {
    if (feedback.trim() === '') {
      alert('Feedback cannot be empty');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/feedback', {
        feedback: feedback
      });
      setFeedbackResponse(response.data.message);
      setFeedbackSuccess(true);
      setFeedback('');
      setTimeout(() => setFeedbackSuccess(false), 3000);
    } catch (error) {
      console.error("There was an error sending the feedback:", error);
      setFeedbackResponse('Failed to send feedback');
      setFeedbackSuccess(false);
    }
  };

  return (
    <div className="App">
      <div className="header">
        <h1>Survival Prediction</h1>
        <p>Prediction of your survival now</p>
      </div>
      <div className="prediction-container">
        <form>
          <select value={passengerClass} onChange={(e) => setPassengerClass(e.target.value)} className="input-field">
            <option value="" disabled>Select Passenger Class</option>
            <option value="1">1st Class</option>
            <option value="2">2nd Class</option>
            <option value="3">3rd Class</option>
          </select>
          <div className="input-group">
            <label htmlFor="age-range">Passenger Age</label>
            <input
              type="range"
              id="age-range"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="input-field"
              min="0"
              max="100"
            />
            <span>Selected Age: {age}</span>
          </div>
          <input
            placeholder="Total Number of Family on Board"
            value={familyCount}
            onChange={(e) => setFamilyCount(e.target.value)}
            className="input-field"
          />
          <select value={gender} onChange={(e) => setGender(e.target.value)} className="input-field">
            <option value="" disabled>Select Gender</option>
            <option value="0">Male</option>
            <option value="1">Female</option>
          </select>
          <select value={port} onChange={(e) => setPort(e.target.value)} className="input-field">
            <option value="" disabled>Select Onboarding Port</option>
            <option value="0">Cherbourg</option>
            <option value="1">Queenstown</option>
            <option value="2">Southampton</option>
          </select>
          <button type="button" onClick={handlePredict} className="predict-button">Predict Now</button>
        </form>
        {prediction && <p className="prediction-text">{prediction}</p>}
        {insights && <Insights insights={insights} />}
      </div>
      <div className="feedback">
        <h2>Share Your Feedback with US</h2>
        <p>Do you have suggestion or found some bug? Let us know in the field below</p>
        <div>
          <textarea 
            placeholder="Send your Feedback here"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            className="feedback-textarea"
          ></textarea>
        </div>
        <button onClick={handleFeedback} className="feedback-button" disabled={!feedback.trim()}>Send</button>
        {feedbackSuccess && <h3 style={{ color: 'green' }}>{feedbackResponse}</h3>}
      </div>
    </div>
  );
}

export default App;
