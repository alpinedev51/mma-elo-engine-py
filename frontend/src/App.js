import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import FighterList from './components/FighterList';
// import FightList from './components/FightList';  // Placeholder for FightList component
// import EventList from './components/EventList';  // Placeholder for EventList component

// Register the necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Example data for the chart
const data = {
  labels: ['Match 1', 'Match 2', 'Match 3'],
  datasets: [
    {
      label: 'Fighter ELO',
      data: [1200, 1250, 1300],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
    },
  ],
};

const App = () => {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>MMA Elo Rating App</h1>
        </header>
        <main>
          <Routes>
            {/* Home route - Display the chart */}
            <Route path="/" element={
              <div>
                <h2>Fighter ELO Chart</h2>
                <Line data={data} />
              </div>
            } />

            {/* Fighters list */}
            <Route path="/fighters" element={<FighterList />} />
            
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
