import logo from './logo.svg';
import './App.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register the necessary components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

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

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <main>
        <h2>Fighter ELO Chart</h2>
        <Line data={data} />
      </main>
    </div>
  );
}

export default App;
