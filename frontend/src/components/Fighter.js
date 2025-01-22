import React, { useState } from 'react';
import { getFightersByName } from '../services/apiService';

const Fighter = () => {
    const [fighterName, setFighterName] = useState('');
    const [eloRecords, setFighter] = useState([]);
    const [error, setError] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalCount, setTotalCount] = useState(0);

    const handleSearch = async (page = 1) => {
        setError('');
        setFighter([]);
        setCurrentPage(page);
        try {
            const skip = (page - 1) * 10;
            const records = await getFightersByName(fighterName, skip, 10, 'elo_rating', 'desc');
            setFighter(records.data);
            setTotalCount(records.total_count);
            setTotalPages(records.pagination.pages);
        } catch (err) {
            setError('No fighters returned.');
        }
    };

    const handleNextPage = () => {
        if (currentPage < totalPages) {
            handleSearch(currentPage + 1);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            handleSearch(currentPage - 1);
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
            <button className="search-button" onClick={() => handleSearch(1)}>
                Search
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {eloRecords.length > 0 && (
                <>
                    <ul>
                        {eloRecords.map((record) => (
                            <li key={record.fighter_id}>
                                <strong>{record.fighter_name}</strong>: Elo Rating - {parseFloat(record.elo_rating).toFixed(1)}
                            </li>
                        ))}
                    </ul>

                    <div className="pagination">
                        <button onClick={handlePreviousPage} disabled={currentPage <= 1}>
                            Previous
                        </button>
                        <span>
                            Page {currentPage} of {totalPages}
                        </span>
                        <button onClick={handleNextPage} disabled={currentPage >= totalPages}>
                            Next
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default Fighter;
