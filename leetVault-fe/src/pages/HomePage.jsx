import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, Code2, Home, Settings, Edit2, Save, X, Github, ExternalLink, Search } from 'lucide-react';
import { useState, useEffect } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL_CRUD;

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
  const [searchQuery, setSearchQuery] = useState('');

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
                  // Show repository selection list
                  <div>
                    <h4 className="text-xl font-semibold text-white mb-6">Connect Git repository</h4>
                    
                    {loadingRepos ? (
                      <div className="text-center py-12">
                        <div className="text-gray-400">Loading repositories...</div>
                      </div>
                    ) : repositories.length === 0 ? (
                      <div className="text-center py-12">
                        <p className="text-gray-400 mb-4">No repositories found. Please make sure you have granted access to at least one repository.</p>
                        <button
                          onClick={handleConnectGitHub}
                          className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200"
                        >
                          <span>Adjust GitHub Permissions</span>
                        </button>
                      </div>
                    ) : (
                      <div>
                        {/* User/Organization Selector and Search */}
                        <div className="flex items-center gap-4 mb-6">
                          <select className="px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 min-w-[200px]">
                            <option>{repositories[0]?.full_name.split('/')[0] || 'vinoth-vk-16'}</option>
                          </select>
                          
                          <div className="flex-1 relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                              type="text"
                              placeholder="Search repositories"
                              value={searchQuery}
                              onChange={(e) => setSearchQuery(e.target.value)}
                              className="w-full pl-10 pr-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                        </div>

                        {/* Repository List */}
                        <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
                          {repositories
                            .filter(repo => 
                              repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                              repo.full_name.toLowerCase().includes(searchQuery.toLowerCase())
                            )
                            .map((repo, index) => (
                            <div 
                              key={repo.id}
                              className={`flex items-center justify-between p-4 hover:bg-gray-750 transition-colors ${
                                index !== repositories.length - 1 ? 'border-b border-gray-700' : ''
                              }`}
                            >
                              <div className="flex items-center space-x-4 flex-1">
                                <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                  {repo.language === 'Python' ? (
                                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                      <path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z"/>
                                    </svg>
                                  ) : repo.language === 'Flutter' ? (
                                    <svg className="w-5 h-5 text-blue-400" viewBox="0 0 24 24" fill="currentColor">
                                      <path d="M14.314 0L2.3 12 6 15.7 21.684.013h-7.357zm.014 11.072L7.857 17.53l6.47 6.47H21.7l-6.46-6.468 6.46-6.46h-7.37z"/>
                                    </svg>
                                  ) : (
                                    <Github className="w-5 h-5 text-white" />
                                  )}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <h4 className="text-white font-medium">{repo.name}</h4>
                                  <p className="text-sm text-gray-400 truncate">{repo.updated_at ? new Date(repo.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + ' ago' : 'Recently updated'}</p>
                                </div>
                              </div>
                              <button
                                onClick={() => handleActivateRepo(repo.full_name, repo.default_branch)}
                                disabled={connectingRepo === repo.full_name}
                                className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                              >
                                {connectingRepo === repo.full_name ? 'Connecting...' : 'Connect'}
                              </button>
                            </div>
                          ))}
                        </div>

                        {/* Pagination Footer */}
                        <div className="mt-4 flex items-center justify-between text-sm text-gray-400">
                          <span>Total results: {repositories.filter(repo => 
                            repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                            repo.full_name.toLowerCase().includes(searchQuery.toLowerCase())
                          ).length}</span>
                          <div className="flex items-center gap-4">
                            <button className="hover:text-white transition-colors disabled:opacity-50" disabled>
                              Prev
                            </button>
                            <button className="hover:text-white transition-colors disabled:opacity-50" disabled>
                              Next
                            </button>
                          </div>
                        </div>
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
