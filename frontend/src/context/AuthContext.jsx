import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  signInWithPopup, 
  signOut, 
  onAuthStateChanged, 
  getIdToken 
} from 'firebase/auth';
import { auth, googleProvider } from '../services/firebase';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [firebaseToken, setFirebaseToken] = useState(null);

  const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      return result;
    } catch (error) {
      console.error("Error signing in with Google:", error);
      throw error;
    }
  };

  const userSignOut = () => {
    return signOut(auth);
  };

  // Set up authentication headers for API requests
  useEffect(() => {
    const getAndSetToken = async (user) => {
      if (user) {
        try {
          const token = await getIdToken(user);
          setFirebaseToken(token);
          
          // Set default auth header for axios
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Send token to backend for verification
          await axios.post(`${import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '')}/auth/firebase-login`, {
            idToken: token
          });
        } catch (error) {
          console.error("Error getting or verifying token:", error);
        }
      } else {
        setFirebaseToken(null);
        delete axios.defaults.headers.common['Authorization'];
      }
    };

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      getAndSetToken(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    firebaseToken,
    signInWithGoogle,
    userSignOut,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};