import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, Code2, Home, Settings, Edit2, Save, X, Github, ExternalLink } from 'lucide-react';
import { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:8000';

export default function HomePage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { currentUser, logout } = useAuth();
  
  // Existing state
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null);
  const [credentials, setCredentials] = useState({
    session_cookie: '',
    csrf_token: '',
    leetcode_username: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  // GitHub-related state
  const [githubStatus, setGithubStatus] = useState(false);
  const [installationId, setInstallationId] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [loadingRepos, setLoadingRepos] = useState(false);
  const [activatedRepo, setActivatedRepo] = useState(null);
  const [connectingRepo, setConnectingRepo] = useState(null);
  const [disconnecting, setDisconnecting] = useState(false);

  // Check if returning from GitHub installation callback
  useEffect(() => {
    const installationIdParam = searchParams.get('installation_id');
    if (installationIdParam) {
      // Clear URL params and refresh user data
      window.history.replaceState({}, '', '/home');
    }
  }, [searchParams]);

  // Check/Create user and fetch credentials on mount
  useEffect(() => {
    if (currentUser?.email) {
      checkAndFetchUser();
    }
  }, [currentUser]);

  const checkAndFetchUser = async () => {
    try {
      setLoading(true);
      
      // Step 1: Check/Create user
      const userResponse = await fetch(`${API_BASE_URL}/api/users/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: currentUser.email
        })
      });

      if (!userResponse.ok) {
        throw new Error('Failed to check user');
      }

      const data = await userResponse.json();
      setUserData(data);

      // Extract GitHub-related data
      setGithubStatus(data.github_status || false);
      setInstallationId(data.installation_id || null);
      
      // Set activated repo if exists
      if (data.repo_activation && data.activated_repo) {
        setActivatedRepo(data.activated_repo);
      } else {
        setActivatedRepo(null);
      }

      // If GitHub is connected and no repo activated, fetch available repositories
      if (data.github_status && data.installation_id && !data.repo_activation) {
        await fetchRepositories(data.installation_id);
      }

      // Step 2: Fetch LeetCode credentials if user exists
      if (!data.is_new_user) {
        await fetchCredentials();
      } else {
        // New user - show empty form in edit mode
        setIsEditing(true);
      }
    } catch (error) {
      console.error('Error checking user:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCredentials = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/leetcode/credentials/${encodeURIComponent(currentUser.email)}`);
      
      if (response.ok) {
        const data = await response.json();
        
        if (data.configured) {
          // Credentials exist - populate form
          setCredentials({
            session_cookie: data.session_cookie || '',
            csrf_token: data.csrf_token || '',
            leetcode_username: data.leetcode_username || ''
          });
        } else {
          // No credentials configured - show empty form in edit mode
          setIsEditing(true);
        }
      }
    } catch (error) {
      console.error('Error fetching credentials:', error);
      // On error, show empty form in edit mode
      setIsEditing(true);
    }
  };

  const fetchRepositories = async (instId) => {
    try {
      setLoadingRepos(true);
      const response = await fetch(`${API_BASE_URL}/api/github/installations/${instId}/repositories`);
      
      if (response.ok) {
        const data = await response.json();
        setRepositories(data.repositories || []);
      } else {
        console.error('Failed to fetch repositories');
        setRepositories([]);
      }
    } catch (error) {
      console.error('Error fetching repositories:', error);
      setRepositories([]);
    } finally {
      setLoadingRepos(false);
    }
  };

  const handleConnectGitHub = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/github/install?email=${encodeURIComponent(currentUser.email)}`);
      
      if (response.ok) {
        const data = await response.json();
        // Redirect to GitHub installation page
        window.location.href = data.installation_url;
      } else {
        alert('Failed to get GitHub installation URL. Please try again.');
      }
    } catch (error) {
      console.error('Error getting GitHub install URL:', error);
      alert('Failed to connect to GitHub. Please try again.');
    }
  };

  const handleActivateRepo = async (repoFullName, defaultBranch) => {
    try {
      setConnectingRepo(repoFullName);
      
      const response = await fetch(`${API_BASE_URL}/api/repos/activate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: currentUser.email,
          installation_id: installationId,
          repo_name: repoFullName,
          default_branch: defaultBranch || 'main'
        })
      });

      if (response.ok) {
        const data = await response.json();
        setActivatedRepo({
          repo_full_name: data.repo_full_name,
          default_branch: data.default_branch,
          is_active: data.is_active,
          activated_at: data.activated_at
        });
        // Clear repositories list as we now have an activated repo
        setRepositories([]);
      } else {
        const errorData = await response.json().catch(() => ({}));
        alert(errorData.detail || 'Failed to activate repository. Please try again.');
      }
    } catch (error) {
      console.error('Error activating repository:', error);
      alert('Failed to activate repository. Please try again.');
    } finally {
      setConnectingRepo(null);
    }
  };

  const handleDeactivateRepo = async () => {
    try {
      setDisconnecting(true);
      
      const response = await fetch(`${API_BASE_URL}/api/repos/deactivate/${encodeURIComponent(currentUser.email)}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setActivatedRepo(null);
        // Refetch repositories
        if (installationId) {
          await fetchRepositories(installationId);
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        alert(errorData.detail || 'Failed to deactivate repository. Please try again.');
      }
    } catch (error) {
      console.error('Error deactivating repository:', error);
      alert('Failed to deactivate repository. Please try again.');
    } finally {
      setDisconnecting(false);
    }
  };

  const handleSaveCredentials = async () => {
    try {
      setSaving(true);
      
      const response = await fetch(`${API_BASE_URL}/api/leetcode/credentials`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: currentUser.email,
          session_cookie: credentials.session_cookie,
          csrf_token: credentials.csrf_token,
          leetcode_username: credentials.leetcode_username
        })
      });

      if (!response.ok) {
        throw new Error('Failed to save credentials');
      }

      const data = await response.json();
      setCredentials({
        session_cookie: data.session_cookie || '',
        csrf_token: data.csrf_token || '',
        leetcode_username: data.leetcode_username || ''
      });
      setIsEditing(false);
      
      // Show success message
      alert('LeetCode credentials saved successfully!');
    } catch (error) {
      console.error('Error saving credentials:', error);
      alert('Failed to save credentials. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  const handleInputChange = (field, value) => {
    setCredentials(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    // Refetch to reset form
    fetchCredentials();
  };

  return (
    <div className="flex min-h-screen bg-black">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900/50 border-r border-gray-800 flex flex-col">
        {/* Logo at top */}
        <div className="p-6 border-b border-gray-800">
          <div className="flex items-center space-x-3">
            <Code2 className="w-8 h-8 text-white" />
            <h1 className="text-xl font-bold text-white">LeetVault</h1>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          <button className="w-full flex items-center space-x-3 px-4 py-3 text-white bg-gray-800 rounded-lg hover:bg-gray-700 transition-all duration-200">
            <Home className="w-5 h-5" />
            <span>Home</span>
          </button>
          
          <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-all duration-200">
            <Settings className="w-5 h-5" />
            <span>Settings</span>
          </button>
        </nav>

        {/* Logout button at bottom */}
        <div className="p-4 border-t border-gray-800">
          <button
            onClick={handleLogout}
            className="w-full flex items-center space-x-3 px-4 py-3 text-red-400 hover:text-red-300 hover:bg-red-950/30 rounded-lg transition-all duration-200"
          >
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-gray-400">Loading...</div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* User Info */}
              <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
                <h2 className="text-xl font-semibold text-white mb-2">Welcome back!</h2>
                <p className="text-gray-400">{currentUser?.email}</p>
                {userData?.is_new_user && (
                  <p className="text-sm text-blue-400 mt-2">New user - Please add your LeetCode credentials below to get started</p>
                )}
                {!userData?.is_new_user && isEditing && !credentials.session_cookie && (
                  <p className="text-sm text-yellow-400 mt-2">No credentials found - Please add your LeetCode credentials below</p>
                )}
              </div>

              {/* LeetCode Credentials Box */}
              <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-white">LeetCode Credentials</h3>
                  {!isEditing ? (
                    <button
                      onClick={() => setIsEditing(true)}
                      className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200"
                    >
                      <Edit2 className="w-4 h-4" />
                      <span>Edit</span>
                    </button>
                  ) : (
                    <div className="flex space-x-2">
                      <button
                        onClick={handleCancelEdit}
                        disabled={saving}
                        className="flex items-center space-x-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all duration-200 disabled:opacity-50"
                      >
                        <X className="w-4 h-4" />
                        <span>Cancel</span>
                      </button>
                      <button
                        onClick={handleSaveCredentials}
                        disabled={saving}
                        className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-200 disabled:opacity-50"
                      >
                        <Save className="w-4 h-4" />
                        <span>{saving ? 'Saving...' : 'Save'}</span>
                      </button>
                    </div>
                  )}
                </div>

                <div className="space-y-4">
                  {/* LeetCode Username */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      LeetCode Username
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={credentials.leetcode_username}
                        onChange={(e) => handleInputChange('leetcode_username', e.target.value)}
                        placeholder="your_leetcode_username"
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    ) : (
                      <div className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white">
                        {credentials.leetcode_username || 'Not set'}
                      </div>
                    )}
                  </div>

                  {/* Session Cookie */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Session Cookie (LEETCODE_SESSION)
                    </label>
                    {isEditing ? (
                      <textarea
                        value={credentials.session_cookie}
                        onChange={(e) => handleInputChange('session_cookie', e.target.value)}
                        placeholder="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        rows={3}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                      />
                    ) : (
                      <div className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white font-mono text-sm break-all">
                        {credentials.session_cookie ? `${credentials.session_cookie.substring(0, 50)}...` : 'Not set'}
                      </div>
                    )}
                  </div>

                  {/* CSRF Token */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      CSRF Token
                    </label>
                    {isEditing ? (
                      <input
                        type="text"
                        value={credentials.csrf_token}
                        onChange={(e) => handleInputChange('csrf_token', e.target.value)}
                        placeholder="abcdef1234567890abcdef1234567890"
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                      />
                    ) : (
                      <div className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white font-mono text-sm">
                        {credentials.csrf_token || 'Not set'}
                      </div>
                    )}
                  </div>
                </div>

                {/* Help Text */}
                <div className="mt-6 p-4 bg-blue-950/30 border border-blue-800/50 rounded-lg">
                  <p className="text-sm text-blue-300">
                    <strong>How to get your credentials:</strong>
                  </p>
                  <ol className="text-sm text-blue-200 mt-2 space-y-1 list-decimal list-inside">
                    <li>Log in to LeetCode in your browser</li>
                    <li>Open Developer Tools (F12)</li>
                    <li>Go to Application/Storage → Cookies</li>
                    <li>Find LEETCODE_SESSION and csrftoken</li>
                    <li>Copy and paste the values here</li>
                  </ol>
                </div>
              </div>

              {/* GitHub Integration Section */}
              <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
                <div className="flex items-center space-x-3 mb-6">
                  <Github className="w-6 h-6 text-white" />
                  <h3 className="text-lg font-semibold text-white">GitHub Integration</h3>
                </div>

                {!githubStatus ? (
                  // Show Connect GitHub button
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Github className="w-8 h-8 text-gray-400" />
                    </div>
                    <p className="text-gray-400 mb-6">Connect your GitHub account to sync your LeetCode solutions automatically</p>
                    <button
                      onClick={handleConnectGitHub}
                      className="inline-flex items-center space-x-2 px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-all duration-200 border border-gray-700"
                    >
                      <Github className="w-5 h-5" />
                      <span>Connect GitHub</span>
                    </button>
                  </div>
                ) : activatedRepo ? (
                  // Show connected repository
                  <div className="p-4 bg-gray-800 rounded-lg border border-green-500/50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center">
                          <Github className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <h4 className="text-white font-semibold">{activatedRepo.repo_full_name}</h4>
                            <a 
                              href={`https://github.com/${activatedRepo.repo_full_name}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-gray-400 hover:text-white"
                            >
                              <ExternalLink className="w-4 h-4" />
                            </a>
                          </div>
                          <p className="text-sm text-green-400">Connected</p>
                          <p className="text-xs text-gray-500">Branch: {activatedRepo.default_branch}</p>
                        </div>
                      </div>
                      <button
                        onClick={handleDeactivateRepo}
                        disabled={disconnecting}
                        className="px-4 py-2 bg-gray-700 hover:bg-red-600 text-white rounded-lg transition-all duration-200 disabled:opacity-50"
                      >
                        {disconnecting ? 'Disconnecting...' : 'Disconnect'}
                      </button>
                    </div>
                  </div>
                ) : (
                  // Show repository selection cards
                  <div>
                    <p className="text-gray-400 mb-4">Select a repository to sync your LeetCode solutions:</p>
                    {loadingRepos ? (
                      <div className="text-center py-8">
                        <div className="text-gray-400">Loading repositories...</div>
                      </div>
                    ) : repositories.length === 0 ? (
                      <div className="text-center py-8">
                        <p className="text-gray-400 mb-4">No repositories found. Please make sure you have granted access to at least one repository.</p>
                        <button
                          onClick={handleConnectGitHub}
                          className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200"
                        >
                          <span>Adjust GitHub Permissions</span>
                        </button>
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {repositories.map(repo => (
                          <div 
                            key={repo.id} 
                            className="p-4 bg-gray-800 rounded-lg border border-gray-700 hover:border-gray-600 transition-all duration-200"
                          >
                            <div className="flex items-start justify-between">
                              <div className="flex items-start space-x-3">
                                <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                  <Github className="w-5 h-5 text-white" />
                                </div>
                                <div>
                                  <h4 className="text-white font-semibold">{repo.name}</h4>
                                  <p className="text-sm text-gray-400">{repo.full_name}</p>
                                  {repo.description && (
                                    <p className="text-xs text-gray-500 mt-1 line-clamp-2">{repo.description}</p>
                                  )}
                                  <div className="flex items-center space-x-2 mt-2">
                                    <span className={`text-xs px-2 py-0.5 rounded ${repo.private ? 'bg-yellow-900/50 text-yellow-400' : 'bg-green-900/50 text-green-400'}`}>
                                      {repo.private ? 'Private' : 'Public'}
                                    </span>
                                    <span className="text-xs text-gray-500">
                                      Branch: {repo.default_branch}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <button
                              onClick={() => handleActivateRepo(repo.full_name, repo.default_branch)}
                              disabled={connectingRepo === repo.full_name}
                              className="w-full mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              {connectingRepo === repo.full_name ? 'Connecting...' : 'Connect'}
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
