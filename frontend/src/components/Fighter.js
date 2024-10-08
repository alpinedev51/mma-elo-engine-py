import React, { useState } from 'react';
import { getFighter } from '../services/apiService';

const Fighter = () => {
    const [fighterName, setFighterName] = useState('');
    const [eloRecords, setFighter] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        setError('');
        setFighter([]);
        try {
            const records = await getFighter(fighterName);
            setFighter(records);
        } catch (err) {
            setError('No Elo records returned for this fighter.');
        }
    };

    return (
        <div>
            <h2>Search Elo Records by Fighter</h2>
            <input
                type="text"
                value={fighterName}
                onChange={(e) => setFighterName(e.target.value)}
                placeholder="Enter fighter name"
            />
            <button onClick={handleSearch}>Search</button>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {eloRecords.length > 0 && (
                <ul>
                    {eloRecords.map((record) => (
                        <li key={record.fighter_id}>
                            <strong>{record.fighter_name}</strong>: Elo Rating - {record.elo_rating}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Fighter;
