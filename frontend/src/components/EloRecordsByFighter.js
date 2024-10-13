import React, { useState } from 'react';
import { getEloRecordsByFighter } from '../services/apiService';

const EloRecordsByFighter = () => {
    const [fighterName, setFighterName] = useState('');
    const [eloRecords, setEloRecordsByFighter] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        setError('');
        setEloRecordsByFighter([]);
        try {
            const records = await getEloRecordsByFighter(fighterName);
            console.log(records)
            setEloRecordsByFighter(records);
        } catch (err) {
            setError('No Elo records returned for this fighter.');
        }
    };

    return (
        <div className="elo-records">
            <h2>Search Elo Records by Fighter</h2>
            <input
                type="text"
                value={fighterName}
                onChange={(e) => setFighterName(e.target.value)}
                placeholder="Enter fighter name"
            />
            <button className="search-button" onClick={handleSearch}>
                Search
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {eloRecords.length > 0 && (
                <ul>
                    {eloRecords.map((record) => (
                        <li key={record.id}>
                            <strong>{record.fighter_name}</strong>: Elo Rating - {parseFloat(record.elo_rating).toFixed(1)}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default EloRecordsByFighter;
