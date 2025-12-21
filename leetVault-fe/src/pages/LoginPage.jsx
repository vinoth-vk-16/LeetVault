import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { SmokeyBackground, LoginFormComponent } from '../components/ui/login-form';
import { ArrowLeft } from 'lucide-react';

export default function LoginPage() {
  const navigate = useNavigate();
  const { signInWithGoogle } = useAuth();

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
      navigate('/home');
    } catch (error) {
      console.error('Failed to sign in:', error);
      alert('Failed to sign in. Please try again.');
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
        className="absolute top-6 left-6 z-20 flex items-center space-x-2 px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-lg text-white transition-all duration-300 border border-white/20"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back</span>
      </button>

      <div className="relative z-10 flex items-center justify-center w-full h-full p-4">
        <LoginFormComponent onGoogleSignIn={handleGoogleSignIn} />
      </div>
    </main>
  );
}

