import React, { useState } from 'react';
import { getEvents } from '../services/apiService';

const Events = () => {
    const [skip, setSkip] = useState(0);
    const [limit, setLimit] = useState(10);
    const [sort, setSort] = useState('event_date');
    const [order, setOrder] = useState('desc');
    const [events, setEvents] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async () => {
        setError('');
        setEvents([]);
        try {
            const eventList = await getEvents(skip, limit, sort, order);
            setEvents(eventList);
        } catch (err) {
            setError('Failed to retrieve events...')
        }
    };

    return (
        <div className="events-list">
            <h2>Retrieve Events</h2>
            <div className="event-options">
                <div className="events-options-input-group">
                    <label>Skip:</label>
                    <input
                        type="number"
                        id="skip"
                        value={skip}
                        onChange={(e) => setSkip(Number(e.target.value))}
                        min="0"
                    />
                </div>

                <div className="events-options-input-group">
                    <label>Limit:</label>
                    <input
                        type="number"
                        id="limit"
                        value={limit}
                        onChange={(e) => setLimit(Number(e.target.value))}
                        min="0"
                    />
                </div>

                <div className="events-options-input-group">
                    <label>Sort By:</label>
                    <select
                        id="sort"
                        value={sort}
                        onChange={(e) => setSort(e.target.value)}
                    >
                        <option value="event_date">Event Date</option>
                        <option value="event_name">Event Name</option>
                    </select>
                </div>

                <div className="events-options-input-group">
                    <label>Order By:</label>
                    <select
                        id="order"
                        value={order}
                        onChange={(e) => setOrder(e.target.value)}
                    >
                        <option value="desc">Descending (Latest to Oldest)</option>
                        <option value="asc">Ascending (Oldest to Latest)</option>
                    </select>
                </div>
            </div>
            <button className="search-button" onClick={handleSearch}>
                Retrieve Events
            </button>

            {error && <p style={{ color: 'red' }}>{error}</p>}
            {events.length > 0 && (
                <ul>
                    {events.map((event) => (
                        <li key={event.event_id}>
                            <strong>{event.event_name}</strong> - {new Date(event.event_date).toLocaleDateString()}
                        </li>
                    ))}
                </ul>
             )}
        </div>
    );
};

export default Events;
