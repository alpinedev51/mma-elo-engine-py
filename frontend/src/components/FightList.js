import React, { useState, useEffect } from 'react';
import { getFighters } from '../services/apiService';

const FightList = () => {
    const [fights, setFights] = useState([]);

    // Fetch the list of fighters from the API
  useEffect(() => {
    const fetchFights = async () => {
      const fightsData = await getFights();
      setFighters(fightsData);
    };
    fetchFights();
  }, []);

  return (
    <div>
      <h1>Fight List</h1>
      <ul>
        {fights.map(fight => (
          <li key={fight.id}>
            Fighter 1: {fight.fighter_1} v. Fighter 2: {fight.fighter_2}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FightList;
