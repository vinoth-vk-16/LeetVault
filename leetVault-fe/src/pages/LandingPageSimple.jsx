import { useNavigate } from 'react-router-dom';
import { Github, Code2, TrendingUp, ArrowRight } from 'lucide-react';

export default function LandingPageSimple() {
  const navigate = useNavigate();

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      <div className="flex flex-col items-center justify-center min-h-screen space-y-8 px-4 py-12">
        {/* Logo/Brand */}
        <div className="flex items-center space-x-3 mb-4">
          <Code2 className="w-12 h-12 md:w-16 md:h-16 text-blue-500" />
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold text-white">
            LeetVault
          </h1>
        </div>

        {/* Tagline */}
        <p className="text-xl md:text-2xl lg:text-3xl text-gray-200 text-center max-w-3xl font-light">
          Automate your LeetCode progress tracking through seamless GitHub integration
        </p>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 max-w-4xl w-full">
          <div className="flex flex-col items-center space-y-3 p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
            <Github className="w-10 h-10 text-blue-400" />
            <h3 className="text-lg font-semibold text-white">GitHub Sync</h3>
            <p className="text-sm text-gray-300 text-center">
              Automatically sync your solutions to GitHub
            </p>
          </div>

          <div className="flex flex-col items-center space-y-3 p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
            <TrendingUp className="w-10 h-10 text-green-400" />
            <h3 className="text-lg font-semibold text-white">Track Progress</h3>
            <p className="text-sm text-gray-300 text-center">
              Monitor your coding journey with detailed analytics
            </p>
          </div>

          <div className="flex flex-col items-center space-y-3 p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
            <Code2 className="w-10 h-10 text-purple-400" />
            <h3 className="text-lg font-semibold text-white">Organize Solutions</h3>
            <p className="text-sm text-gray-300 text-center">
              Keep all your solutions organized and accessible
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={() => navigate('/login')}
          className="group mt-12 flex items-center space-x-2 px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-xl text-white font-semibold text-lg transition-all duration-300 shadow-lg hover:shadow-blue-500/50 transform hover:scale-105"
        >
          <span>Get Started</span>
          <ArrowRight className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
        </button>

        {/* Additional Info */}
        <p className="text-sm text-gray-400 mt-8">
          Free forever • No credit card required • Open source
        </p>
      </div>
    </div>
  );
}

