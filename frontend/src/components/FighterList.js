import React, { useState, useEffect } from 'react';
import { getFighters } from '../services/apiService';

const FighterList = () => {
    const [fighters, setFighters] = useState([]);

    // Fetch the list of fighters from the API
    useEffect(() => {
      const fetchFighters = async () => {
        try {
          const fightersData = await getFighters();
          setFighters(fightersData);
        } catch (error) {
          console.error("Error fetching fighters:", error);
        }
    };
    fetchFighters();
  }, []);

  return (
    <div>
      <h1>Fighter List</h1>
      <ul>
        {fighters.map(fighter => (
          <li key={fighter.id}>
            {fighter.name} - Elo: {fighter.elo_rating}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FighterList;
