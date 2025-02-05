import React, { useState } from 'react';
import { getEloRecordsByFighter } from '../services/apiService';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const EloRecordsByFighter = () => {
    const [fighterName, setFighterName] = useState('');
    const [eloRecords, setEloRecords] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        setError('');
        setEloRecords([]);
        setLoading(true);

        try {
            setEloRecords(records);
            const records = await getEloRecordsByFighter(fighterName, 'asc');

            const formattedRecords = records.map((record, index) => ({
                fight: index,
                fighterName: record.fighter_name,
                elo: parseFloat(record.elo_rating),
            }));
            setEloRecords(formattedRecords);
        } catch (err) {
            setError('No Elo records returned for this fighter.');
        } finally {
            setLoading(false);
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
                    <li key={record.fight}>
                        <strong>{record.fighterName}</strong>: Elo Rating - {parseFloat(record.elo).toFixed(1)}
                    </li>
                </ul>
            )}

            {eloRecords.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-xl font-semibold mb-2">Elo Progression</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={eloRecords}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="fight" label={{ value: "Fight Number", position: "insideBottom", offset: -5 }} />
                            <YAxis domain={["auto", "auto"]} label={{ value: "Elo rating", angle: -90, position: "insideLeft" }} />
                            <Line type="monotone" dataKey="elo" stroke="#1D4ED8" strokeWidth={2} dot={{ r: 4 }} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    );
};

export default EloRecordsByFighter;
