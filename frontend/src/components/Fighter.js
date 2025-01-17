import React, { useState } from 'react';
import { getFightersByName } from '../services/apiService';

const Fighter = () => {
    const [fighterName, setFighterName] = useState('');
    const [eloRecords, setFighter] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        setError('');
        setFighter([]);
        try {
            const records = await getFightersByName(fighterName, 0, 10, 'elo_rating', 'desc');
            setFighter(records);
            console.log(records);
        } catch (err) {
            setError('No fighters returned.');
        }
    };

    return (
        <div className="fighter-stats">
            <h2>Search Fighter</h2>
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
                        <li key={record.fighter_id}>
                            <strong>{record.fighter_name}</strong>: Elo Rating - {parseFloat(record.elo_rating).toFixed(1)}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Fighter;
