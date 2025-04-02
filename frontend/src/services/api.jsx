import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

export const uploadCSV = async (file, token) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/upload-csv/', formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
};