import React, { useEffect, useState } from 'react';

function Insights() {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    fetch('/survival_insights.json')
      .then(response => response.json())
      .then(data => setInsights(data))
      .catch(error => console.error('Error fetching the insights:', error));
  }, []);

  if (!insights) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Survival Insights</h2>
      <div>
        <h3>Survival Rate by Gender:</h3>
        <ul>
          {Object.entries(insights.gender).map(([key, value]) => (
            <li key={key}>{key}: {value.toFixed(2)}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Survival Rate by Class:</h3>
        <ul>
          {Object.entries(insights.class).map(([key, value]) => (
            <li key={key}>{key}: {value.toFixed(2)}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Survival Rate by Age Group:</h3>
        <ul>
          {Object.entries(insights.age_group).map(([key, value]) => (
            <li key={key}>{key}: {value.toFixed(2)}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Survival Rate by Family Size:</h3>
        <ul>
          {Object.entries(insights.family_size).map(([key, value]) => (
            <li key={key}>{key}: {value.toFixed(2)}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Insights;