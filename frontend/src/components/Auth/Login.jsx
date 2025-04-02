import { useState } from 'react';
import { signInWithGoogle, signInWithEmail } from '../../services/firebase';
import LoadingSpinner from '../Common/LoadingSpinner';
import { FaGoogle, FaUser } from 'react-icons/fa';
import './Login.css';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleEmailLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await signInWithEmail(email, password);
    } catch (error) {
      setError(error.message);
    }

    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="auth-card">
        <h1 className="login-title">🔍 Data Quality Analyzer</h1>

        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleEmailLogin} className="email-form">
          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={loading} className="primary-btn">
            {loading ? <LoadingSpinner /> : 'Sign In'}
          </button>
        </form>

        <div className="separator">or</div>

        <button onClick={signInWithGoogle} className="google-btn">
          <FaGoogle className="google-icon" /> Continue with Google
        </button>
      </div>
    </div>
  );
}
