import React from 'react';
import EloRecordsByFighter from './components/EloRecordsByFighter'; // Adjust the import based on your file structure

const App = () => {
    return (
        <div>
            <h1>MMA Elo Ratings</h1>
            <EloRecordsByFighter />
        </div>
    );
};

export default App;