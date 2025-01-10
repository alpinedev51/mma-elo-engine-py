import axios from 'axios';

// Set up base URL for API
const api = axios.create({
    baseURL: 'http://backend:5050'
});

// Get all fighters
export const getFighters = async (skip, limit, sort, order) => {
    try {
        const response = await api.get('api/fighters', {
            params:
            {
                skip: skip,
                limit: limit,
                sort: sort,
                order: order
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching fighters:', error);
        throw error;
    }
};

// Function to fetch Elo records by fighter name
export const getFightersByName = async (fighterName, sort, order) => {
    try {
        const response = await api.get('api/fighters/search', {
            params: 
            { 
                fighter_name: fighterName,
                sort: sort,
                order: order
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching fighter records:', error);
        throw error;
    }
};
  
  // Get all fights
export const getFights = async () => {
    const response = await api.get('api/fights');
    return response.data;
};
  
// Get all events
export const getEvents = async (skip, limit, sort, order) => {
    try {
        const response = await api.get('api/events/', {
            params:
            {
                skip: skip,
                limit: limit,
                sort: sort,
                order: order
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching events:', error);
        throw error;
    }
};

// Function to fetch Elo records by fighter name
export const getEloRecordsByFighter = async (fighterName, sort, order) => {
    try {
        const response = await api.get('api/elo-records/search', {
            params: 
            { 
                fighter_name: fighterName,
                sort: sort,
                order: order
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching Elo records:', error);
        throw error;
    }
};
