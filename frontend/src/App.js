import React from 'react';
import Fighter from './components/Fighter';
import EloProgressionByFighter from './components/ProgressionByFighter';
import Events from './components/Events';
import './style/App.css';
import './style/Stats.css';

const Sidebar = () => {
    return (
        <div className="sidebar">
            <h2 className="sidebar-title">MMA Elo Ratings</h2>
            <ul className="sidebar-menu">
                <li><a href="#fighter">Fighter Info</a></li>
                <li><a href="#elo-records">Elo Records</a></li>
            </ul>
        </div>
    );
};

const App = () => {
    return (
        <div className="app-container">
            <Sidebar />
            <div className="main-content">
                <h1 className="app-content-title">MMA Elo Ratings</h1>
                <div className="app-content-section">
                    <div id="fighter" className="content-section Fighter">
                        <Fighter />
                    </div>
                    <div id="elo-records" className="content-section EloProgressionByFighter">
                        <EloProgressionByFighter />
                    </div>
                    <div id="events" className="content-section Events">
                        <Events />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
