import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FiUser, FiLogOut } from 'react-icons/fi';
import './Navbar.css';

const Navbar = () => {
  const { currentUser, userSignOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      await userSignOut();
      navigate('/login');
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>Data Quality Analyzer</h1>
      </div>
      
      {currentUser && (
        <div className="navbar-user">
          <div className="user-info">
            {currentUser.photoURL ? (
              <img 
                src={currentUser.photoURL} 
                alt="User profile" 
                className="user-avatar" 
              />
            ) : (
              <FiUser className="user-icon" />
            )}
            <span className="user-name">{currentUser.displayName || currentUser.email}</span>
          </div>
          <button className="logout-button" onClick={handleSignOut}>
            <FiLogOut className="logout-icon" />
            <span className="logout-text">Logout</span>
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;