import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const getPollData = () => api.get('/poll');
export const submitVote = (optionId) => api.post(`/poll/vote?option_id=${optionId}`);