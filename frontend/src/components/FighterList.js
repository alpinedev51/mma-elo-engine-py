import React, { useState, useEffect } from 'react';
import { getFighters } from '../services/apiService';

const FighterList = () => {
    const [fighters, setFighters] = useState([]);

    // Fetch the list of fighters from the API
  useEffect(() => {
    const fetchFighters = async () => {
      const fightersData = await getFighters();
      setFighters(fightersData);
    };
    fetchFighters();
  }, []);

  return (
    <div>
      <h1>Fighter List</h1>
      <ul>
        {fighters.map(fighter => (
          <li key={fighter.id}>
            {fighter.name} - Elo: {fighter.elo}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FighterList;
