import { useAuth } from './context/AuthContext';
import Login from './components/Auth/Login';
import Upload from './components/Dashboard/Upload';
import Results from './components/Dashboard/Results';
import { useState } from 'react';
import './App.css';

export default function App() {
  const { user, loading, logout } = useAuth();
  const [results, setResults] = useState(null);

  if (loading) {
    return <div className="app-loading">Loading...</div>;
  }

  if (!user) return <Login />;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="welcome-text">Welcome, {user.email}</h1>
        <button onClick={logout} className="logout-btn">
          <i className="fas fa-sign-out-alt"></i> Logout
        </button>
      </header>
      
      {!results ? (
        <Upload onUploadSuccess={setResults} />
      ) : (
        <Results data={results} onReset={() => setResults(null)} />
      )}
    </div>
  );
}
