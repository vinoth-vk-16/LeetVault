import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { SmokeyBackground, LoginFormComponent } from '../components/ui/login-form';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { useState } from 'react';

export default function LoginPage() {
  const navigate = useNavigate();
  const { signInWithGoogle, creatingUser } = useAuth();
  const [signingIn, setSigningIn] = useState(false);

  const handleGoogleSignIn = async () => {
    try {
      setSigningIn(true);
      await signInWithGoogle();
      navigate('/home');
    } catch (error) {
      console.error('Failed to sign in:', error);
      alert('Failed to sign in. Please try again.');
    } finally {
      setSigningIn(false);
    }
  };

  return (
    <main className="relative w-screen h-screen bg-black">
      <SmokeyBackground 
        className="absolute inset-0" 
        color="#000000"
        backdropBlurAmount="sm"
      />
      
      {/* Back button */}
      <button
        onClick={() => navigate('/')}
        disabled={signingIn || creatingUser}
        className="absolute top-6 left-6 z-20 flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-lg text-white transition-all duration-300 border border-white/20 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back</span>
      </button>

      {/* Loading overlay */}
      {(signingIn || creatingUser) && (
        <div className="absolute inset-0 z-30 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-8 flex flex-col items-center space-y-4">
            <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
            <p className="text-white text-lg font-semibold">
              {creatingUser ? 'Creating your account...' : 'Signing in...'}
            </p>
            <p className="text-gray-400 text-sm">Please wait a moment</p>
          </div>
        </div>
      )}

      <div className="relative z-10 flex items-center justify-center w-full h-full p-4">
        <LoginFormComponent onGoogleSignIn={handleGoogleSignIn} />
      </div>
    </main>
  );
}

