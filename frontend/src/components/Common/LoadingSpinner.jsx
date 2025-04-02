import './LoadingSpinner.css';

export default function LoadingSpinner() {
  return (
    <div className="spinner-container">
      <div className="loading-spinner"></div>
      <p className="loading-text">Processing your file...</p>
    </div>
  );
}