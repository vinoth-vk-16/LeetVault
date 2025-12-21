import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBoGIB4eJr-yQsP29lz_8P_Yoxluvp1kO8",
  authDomain: "leetvault.firebaseapp.com",
  projectId: "leetvault",
  storageBucket: "leetvault.firebasestorage.app",
  messagingSenderId: "936596808008",
  appId: "1:936596808008:web:91481674f3a9476bc3d37d"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export default app;

