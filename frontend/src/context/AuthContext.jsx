import { createContext, useContext, useState, useEffect } from 'react';
import { auth } from '../services/firebase';
import { signOut } from 'firebase/auth';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      setUser(user || null);
      if (user) {
        try {
          const token = await user.getIdToken();
          setToken(token);
        } catch (error) {
          console.error("Token error:", error);
        }
      }
      setLoading(false);
    });
    
    return () => unsubscribe();
  }, []);

  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setToken(null);
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};