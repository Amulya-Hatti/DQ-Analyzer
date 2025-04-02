import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { uploadCSV } from '../../services/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import './Upload.css';

export default function Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const { token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }
    
    try {
      setLoading(true);
      setError('');
      const response = await uploadCSV(file, token);
      onUploadSuccess(response.data);
    } catch (error) {
      console.error('Upload Error:', error);
      setError(error.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">Data Quality Rule Suggestion</h1>
      <p className="upload-description">Based on data profiling, this tool helps generate rules for better data quality.</p>
      <form onSubmit={handleSubmit} className="upload-form">
        <label className="file-input-label">
          <input 
            type="file" 
            accept=".csv" 
            onChange={handleFileChange}
            disabled={loading}
          />
          <span className="file-label">Choose CSV File</span>
        </label>
        {file && <p className="file-name">Selected File: {file.name}</p>}
        
        <div className="button-group">
          <button 
            type="submit" 
            disabled={!file || loading}
            className="analyze-btn"
          >
            {loading ? <LoadingSpinner /> : 'Analyze CSV'}
          </button>
        </div>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}