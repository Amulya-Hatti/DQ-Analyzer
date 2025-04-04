import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FcGoogle } from 'react-icons/fc';
import './Login.css';

const Login = () => {
  const [error, setError] = useState('');
  const { signInWithGoogle, currentUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (currentUser) {
      navigate('/dashboard');
    }
  }, [currentUser, navigate]);

  const handleGoogleSignIn = async () => {
    try {
      setError('');
      await signInWithGoogle();
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError('Failed to sign in with Google. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Data Quality Analyzer</h1>
          <p>Analyze database quality and generate validation rules</p>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="login-methods">
          <button className="google-sign-in" onClick={handleGoogleSignIn}>
            <FcGoogle className="google-icon" />
            <span>Sign in with Google</span>
          </button>
        </div>
        
        <div className="login-footer">
          <p>Validate your data quality with AI-powered analysis</p>
        </div>
      </div>
    </div>
  );
};

export default Login;