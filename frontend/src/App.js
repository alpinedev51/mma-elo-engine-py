import React from 'react';
import Fighter from './components/Fighter';
import EloRecordsByFighter from './components/EloRecordsByFighter';
import './App.css'

const App = () => {
    return (
        <div classname = "App">
            <h1>MMA Elo Ratings</h1>
            <div className="App-header">
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