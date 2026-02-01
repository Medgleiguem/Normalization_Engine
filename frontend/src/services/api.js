/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      if (onProgress) {
        onProgress(percentCompleted);
      }
    },
  });
  
  return response.data;
};

export const analyzeFile = async (fileId) => {
  const response = await api.post(`/analysis/analyze/${fileId}`);
  return response.data;
};

export const getAnalysisStatus = async (analysisId) => {
  const response = await api.get(`/analysis/status/${analysisId}`);
  return response.data;
};

export const getDownloadUrl = (analysisId, type) => {
  return `${API_BASE_URL}/download/${type}/${analysisId}`;
};

export default api;
