import { createContext, useContext, useEffect, useState } from 'react';
import { 
  signInWithPopup, 
  signOut, 
  onAuthStateChanged 
} from 'firebase/auth';
import { auth, googleProvider } from '../config/firebase';

const AuthContext = createContext();
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL_CRUD;

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [creatingUser, setCreatingUser] = useState(false);

  const signInWithGoogle = async () => {
    try {
      setCreatingUser(true);
      const result = await signInWithPopup(auth, googleProvider);
      
      // After successful Firebase auth, create user in backend
      try {
        const response = await fetch(`${API_BASE_URL}/api/users/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: result.user.email
          })
        });

        if (response.ok) {
          console.log('✅ User created successfully in backend');
        } else if (response.status === 409) {
          // User already exists - this is fine
          console.log('ℹ️ User already exists in backend');
        } else {
          console.error('⚠️ Failed to create user in backend, but continuing...');
        }
      } catch (backendError) {
        console.error('⚠️ Backend user creation error:', backendError);
        // Don't throw - allow user to proceed even if backend fails
      }
      
      setCreatingUser(false);
      return result.user;
    } catch (error) {
      setCreatingUser(false);
      console.error('Error signing in with Google:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Error signing out:', error);
      throw error;
    }
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    signInWithGoogle,
    logout,
    loading,
    creatingUser
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

