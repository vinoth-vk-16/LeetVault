import { useNavigate } from 'react-router-dom';
import { Github, Code2, TrendingUp, ArrowRight, Zap, Shield, Sparkles } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="w-full min-h-screen bg-black relative overflow-hidden">
      {/* Gradient Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      </div>

      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)] bg-[size:100px_100px]"></div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen space-y-12 px-4 py-12">
        
        {/* Hero Section */}
        <div className="text-center space-y-6 max-w-5xl">
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full text-blue-400 text-sm font-medium backdrop-blur-sm">
            <Sparkles className="w-4 h-4" />
            <span>Automate Your Coding Journey</span>
          </div>

          {/* Logo/Brand */}
          <div className="flex items-center justify-center space-x-4 mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-blue-500 blur-xl opacity-50"></div>
              <Code2 className="relative w-16 h-16 md:w-20 md:h-20 text-blue-500" />
            </div>
            <h1 className="text-6xl md:text-8xl lg:text-9xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400">
              LeetVault
            </h1>
          </div>

          {/* Tagline */}
          <p className="text-2xl md:text-3xl lg:text-4xl text-gray-300 font-light leading-relaxed">
            Automate your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 font-semibold">LeetCode</span> progress tracking
            <br />
            through seamless <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 font-semibold">GitHub</span> integration
          </p>

          {/* CTA Button */}
          <div className="pt-8">
            <button
              onClick={() => navigate('/login')}
              className="group relative inline-flex items-center space-x-3 px-10 py-5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-2xl text-white font-bold text-xl transition-all duration-300 shadow-2xl shadow-blue-500/50 hover:shadow-blue-500/70 transform hover:scale-105"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-6 h-6 transform group-hover:translate-x-2 transition-transform" />
              <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-2xl blur-xl opacity-0 group-hover:opacity-50 transition-opacity -z-10"></div>
            </button>
          </div>

          {/* Additional Info */}
          <p className="text-sm text-gray-500 pt-4">
            No credit card required • Free forever • Open source
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 max-w-6xl w-full">
          {/* Feature 1 */}
          <div className="group relative p-8 bg-gradient-to-br from-gray-900/50 to-gray-800/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-blue-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="w-14 h-14 bg-blue-500/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-500/20 transition-colors">
                <Github className="w-7 h-7 text-blue-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">GitHub Sync</h3>
              <p className="text-gray-400 leading-relaxed">
                Automatically sync your LeetCode solutions to GitHub repositories with zero manual effort
              </p>
            </div>
          </div>

          {/* Feature 2 */}
          <div className="group relative p-8 bg-gradient-to-br from-gray-900/50 to-gray-800/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 hover:border-green-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div className="absolute inset-0 bg-gradient-to-br from-green-500/0 to-green-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="w-14 h-14 bg-green-500/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-green-500/20 transition-colors">
                <TrendingUp className="w-7 h-7 text-green-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Track Progress</h3>
              <p className="text-gray-400 leading-relaxed">
                Monitor your coding journey with detailed analytics and visualize your improvement over time
              </p>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="group relative p-8 bg-gradient-to-br from-gray-900/50 to-gray-800/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:scale-105">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-purple-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div className="relative">
              <div className="w-14 h-14 bg-purple-500/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-purple-500/20 transition-colors">
                <Code2 className="w-7 h-7 text-purple-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Organize Solutions</h3>
              <p className="text-gray-400 leading-relaxed">
                Keep all your solutions organized, searchable, and accessible in one centralized location
              </p>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-3 gap-8 mt-16 max-w-3xl w-full">
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 mb-2">
              100%
            </div>
            <div className="text-gray-400 text-sm">Automated</div>
          </div>
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-400 mb-2">
              24/7
            </div>
            <div className="text-gray-400 text-sm">Syncing</div>
          </div>
          <div className="text-center">
            <div className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400 mb-2">
              Free
            </div>
            <div className="text-gray-400 text-sm">Forever</div>
          </div>
        </div>

      </div>
    </div>
  );
}
