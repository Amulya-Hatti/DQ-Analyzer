import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints for data quality analysis
const dataApi = {
  // Table operations
  getTables: () => api.get('/tables/'),
  analyzeTable: (tableName) => api.get(`/analyze-table/?table_name=${tableName}`),
  
  // Validation rules operations
  storeRules: (tableName, rulesData) => 
    api.post(`/validation/store-rules/?table_name=${tableName}`, rulesData),
  getRules: (tableName = null, columnName = null) => {
    let url = '/validation/rules/';
    const params = new URLSearchParams();
    if (tableName) params.append('table_name', tableName);
    if (columnName) params.append('column_name', columnName);
    if (params.toString()) url += `?${params.toString()}`;
    return api.get(url);
  },
  generateSql: (ruleId) => api.post(`/validation/generate-sql/${ruleId}`),
  runValidation: (ruleId) => api.post(`/validation/run-validation/${ruleId}`),
  getDashboardData: (tableName = null) => {
    let url = '/validation/dashboard-data/';
    if (tableName) url += `?table_name=${tableName}`;
    return api.get(url);
  }
};

export default dataApi;