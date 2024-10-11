import React from 'react';
import Fighter from './components/Fighter';
import EloRecordsByFighter from './components/EloRecordsByFighter';
import './App.css'
import './Stats.css'

const App = () => {
    return (
        <div className = "App-content">
            <h1 className = "App-content-title">MMA Elo Ratings</h1>
            <div className="App-stats-box">
                <div className="Fighter">
                    <Fighter />
                </div>
                <div className="EloRecordsByFighter">
                    <EloRecordsByFighter />
                </div>
            </div>
        </div>
    );
};

export default App;