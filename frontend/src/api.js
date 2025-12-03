import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // Adjust if backend runs elsewhere
});

export const generateCreatives = async (formData) => {
    const response = await api.post('/generate-creatives', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob', // Important for downloading zip
    });
    return response;
};

export default api;
