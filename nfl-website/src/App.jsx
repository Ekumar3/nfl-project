import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from "axios"
import './App.css'

function App() {
  const [qbName, setQbName] = useState("");
  const [qbStats, setQbStats] = useState(null);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`http://3.137.179.246:5000/search?qb_name=${qbName}`);
      setQbStats(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setQbStats(null);
    }
  };

  return (
    <>
      <h1>Using 2024 NFL QB Stats to Predict 2025 QB Stats </h1>
      <div>
        <input
          type="text"
          value={qbName}
          onChange={(e) => setQbName(e.target.value)}
          placeholder="Enter a 2024 QB Name"
        />
        <button onClick={fetchStats}>Get Stats</button>
      </div>

      {qbStats && (
        <div className="stats">
        <h2>{qbStats.player}</h2>
        <p><strong>Games Played:</strong> {qbStats.games_played}</p>
        <p><strong>Fantasy Points Last Season:</strong> {qbStats.last_season_fp}</p>
        <p><strong>Fantasy Points Per Game Last Season:</strong> {qbStats.last_season_fppg}</p>
        <p><strong>Projected Fantasy Points:</strong> {qbStats.predicted_fp}</p>
        <p><strong>Projected Fantasy Points Per Game:</strong> {qbStats.predicted_fppg}</p>
        </div>
      )}
    </>
  );
}

export default App;
