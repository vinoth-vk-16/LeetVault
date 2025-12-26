# LeetVault API Documentation

Complete API reference with request/response structures and curl commands.

## Base URL
```
https://69481ac30014e1672988.sgp.appwrite.run
```

## Quick Start

1. **Start Server**
```bash
python main.py
```

2. **Test Health**
```bash
curl https://69481ac30014e1672988.sgp.appwrite.run/health
```

3. **Note**: Interactive docs (Swagger UI/ReDoc) are not available in Appwrite Functions deployment

---

## API Endpoints

### 1. User Management

#### POST /api/users/check
Check if user exists, create if not. Returns complete user status including GitHub and repository activation.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Field Requirements:**
- `email` (required): Valid email address

**Response (New User):**
```json
{
  "success": true,
  "message": "User created successfully",
  "user_id": "user_example_com",
  "email": "user@example.com",
  "name": null,
  "created_at": "2024-12-17T12:00:00.000000Z",
  "updated_at": "2024-12-17T12:00:00.000000Z",
  "is_new_user": true,
  "github_status": false,
  "installation_id": null,
  "repo_activation": false,
  "activated_repo": null
}
```

**Response (Existing User with GitHub & Repo):**
```json
{
  "success": true,
  "message": "User already exists in database",
  "user_id": "user_example_com",
  "email": "user@example.com",
  "name": null,
  "created_at": "2024-12-17T12:00:00.000000Z",
  "updated_at": "2024-12-17T12:05:00.000000Z",
  "is_new_user": false,
  "github_status": true,
  "installation_id": "12345678",
  "repo_activation": true,
  "activated_repo": {
    "repo_full_name": "username/leetcode-solutions",
    "default_branch": "main",
    "is_active": true,
    "activated_at": "2024-12-17T12:03:00.000000Z",
    "last_sync_at": null
  }
}
```

**Curl Command:**
```bash
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/users/check" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

---

#### GET /api/users/{email}
Get user information by email.

**URL Parameters:**
- `email` (required): User's email address

**Response:**
```json
{
  "success": true,
    "user": {
    "user_id": "user_example_com",
      "email": "user@example.com",
    "name": null,
    "created_at": "2024-12-17T12:00:00.000000Z",
    "updated_at": "2024-12-17T12:00:00.000000Z",
    "github_status": false,
    "repo_activation": false
  }
}
```

**Error (404):**
```json
{
  "detail": "User with email 'user@example.com' not found"
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/users/user@example.com"
```

---

### 2. LeetCode Credentials Management

#### POST /api/leetcode/credentials
Store or update LeetCode credentials for a user. User must exist before storing credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "session_cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTIzNDU2In0...",
  "csrf_token": "abcdef1234567890abcdef1234567890",
  "leetcode_username": "my_leetcode_username"
}
```

**Field Requirements:**
- `email` (required): User's email address (must exist in users table)
- `session_cookie` (required): LeetCode session cookie (LEETCODE_SESSION)
- `csrf_token` (required): LeetCode CSRF token
- `leetcode_username` (optional): LeetCode username

**Response (New Credentials):**
```json
{
  "success": true,
  "message": "LeetCode credentials stored successfully",
  "email": "user@example.com",
  "session_cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "csrf_token": "abcdef1234567890abcdef1234567890",
  "leetcode_username": "my_leetcode_username",
  "is_valid": true,
  "created_at": "2024-12-17T12:00:00.000000Z",
  "updated_at": "2024-12-17T12:00:00.000000Z"
}
```

**Response (Updated Credentials):**
```json
{
  "success": true,
  "message": "LeetCode credentials updated successfully",
  "email": "user@example.com",
  "session_cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "csrf_token": "abcdef1234567890abcdef1234567890",
  "leetcode_username": "my_leetcode_username",
  "is_valid": true,
  "created_at": "2024-12-17T12:00:00.000000Z",
  "updated_at": "2024-12-17T12:05:00.000000Z"
}
```

**Error (404 - User Not Found):**
```json
{
  "detail": "User with email 'user@example.com' not found. Please create user first using /api/users/check endpoint."
}
```

**Curl Command:**
```bash
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/leetcode/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "session_cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "csrf_token": "abcdef1234567890",
    "leetcode_username": "my_username"
  }'
```

---

#### GET /api/leetcode/credentials/{email}
Get LeetCode credentials for a user by email.

**URL Parameters:**
- `email` (required): User's email address

**Response:**
```json
{
  "success": true,
  "message": "LeetCode credentials retrieved successfully",
  "email": "user@example.com",
  "session_cookie": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "csrf_token": "abcdef1234567890abcdef1234567890",
  "leetcode_username": "my_leetcode_username",
  "is_valid": true,
  "created_at": "2024-12-17T12:00:00.000000Z",
  "updated_at": "2024-12-17T12:00:00.000000Z"
}
```

**Error (404):**
```json
{
  "detail": "LeetCode credentials not found for user 'user@example.com'. Please store credentials first using POST /api/leetcode/credentials."
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/leetcode/credentials/user@example.com"
```

---

### 3. GitHub App Installation

#### GET /api/auth/github/install
Get GitHub App installation URL for a user.

**Query Parameters:**
- `email` (required): User's email address

**Response:**
```json
{
  "installation_url": "https://github.com/apps/leetvault/installations/new?state=user_example_com",
  "user_id": "user_example_com"
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/auth/github/install?email=user@example.com"
```

**Usage Flow:**
1. Call this endpoint to get installation URL
2. User opens URL in browser
3. User installs GitHub App and selects repositories
4. GitHub redirects to callback URL automatically

---

#### GET /api/auth/github/installation/callback
Handle GitHub App installation callback. Called automatically by GitHub after installation.

**Query Parameters (sent by GitHub):**
- `installation_id` (required): GitHub installation ID
- `setup_action` (required): Action performed (install/update/cancel)
- `state` (required): User ID (email-based)
- `code` (optional): Authorization code

**Behavior:**
1. Receives installation details from GitHub
2. Generates JWT for GitHub API authentication
3. Fetches installation access token
4. Retrieves GitHub username
5. Stores installation in `github_installations` collection
6. Updates user's `Github_status` to `true`
7. Redirects to frontend with installation details

**Redirect URL:**
```
{FRONTEND_URL}/connect-repo?user_id={user_id}&installation_id={installation_id}&github_username={github_username}
```

**Note:** This endpoint is called automatically by GitHub. You don't need to call it manually.

---

#### GET /api/github/installations/{installation_id}/repositories
Get repositories accessible by a GitHub installation.

**URL Parameters:**
- `installation_id` (required): GitHub installation ID

**Response:**
```json
{
  "success": true,
  "repositories": [
    {
      "id": 123456789,
      "name": "leetcode-solutions",
      "full_name": "username/leetcode-solutions",
      "private": false,
      "html_url": "https://github.com/username/leetcode-solutions",
      "description": "My LeetCode solutions",
      "default_branch": "main"
    },
    {
      "id": 987654321,
      "name": "coding-practice",
      "full_name": "username/coding-practice",
      "private": true,
      "html_url": "https://github.com/username/coding-practice",
      "description": "Coding practice repository",
      "default_branch": "master"
    }
  ],
  "total_count": 2
}
```

**Error (500):**
```json
{
  "detail": "Failed to fetch repositories: [error message]"
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/github/installations/12345678/repositories"
```

---

### 4. Repository Activation

#### POST /api/repos/activate
Activate a repository for LeetCode submissions sync. Only one repository can be activated per user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "installation_id": "12345678",
  "repo_name": "username/leetcode-solutions",
  "default_branch": "main"
}
```

**Field Requirements:**
- `email` (required): User's email address (must exist)
- `installation_id` (required): GitHub installation ID
- `repo_name` (required): Repository full name (format: username/repo)
- `default_branch` (optional): Default branch name (default: "main")

**Response (New Activation):**
```json
{
  "success": true,
  "message": "Repository activated successfully",
  "email": "user@example.com",
  "repo_full_name": "username/leetcode-solutions",
  "default_branch": "main",
  "installation_id": "12345678",
  "activated_at": "2024-12-17T12:00:00.000000Z",
  "is_active": true
}
```

**Response (Updated Activation):**
```json
{
  "success": true,
  "message": "Repository updated successfully",
  "email": "user@example.com",
  "repo_full_name": "username/new-repo",
  "default_branch": "main",
  "installation_id": "12345678",
  "activated_at": "2024-12-17T12:05:00.000000Z",
  "is_active": true
}
```

**Error (404 - User Not Found):**
```json
{
  "detail": "User with email 'user@example.com' not found. Please create user first."
}
```

**Behavior:**
1. Checks if user exists
2. If user already has activated repo → Updates to new repo
3. If user has no activated repo → Creates new activation
4. Updates user's `Repo_activation` to `true`
5. Only ONE repository per user (enforced)

**Curl Command:**
```bash
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/repos/activate" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "installation_id": "12345678",
    "repo_name": "username/leetcode-solutions",
    "default_branch": "main"
  }'
```

---

#### DELETE /api/repos/deactivate/{email}
Deactivate the currently activated repository for a user.

**URL Parameters:**
- `email` (required): User's email address

**Response:**
```json
{
  "success": true,
  "message": "Repository deactivated successfully",
  "email": "user@example.com",
  "deactivated_repo": "username/leetcode-solutions"
}
```

**Error (404 - User Not Found):**
```json
{
  "detail": "User with email 'user@example.com' not found"
}
```

**Error (404 - No Activated Repo):**
```json
{
  "detail": "No activated repository found for user 'user@example.com'"
}
```

**Behavior:**
1. Finds activated repository record
2. Deletes the record from `activated_repos` collection
3. Updates user's `Repo_activation` to `false`

**Curl Command:**
```bash
curl -X DELETE "https://69481ac30014e1672988.sgp.appwrite.run/api/repos/deactivate/user@example.com"
```

---

### 5. System Endpoints

#### GET /health
Health check endpoint with database connectivity test.

**Response (Healthy):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-12-17T12:00:00.000000Z"
}
```

**Response (Unhealthy):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "Connection error details",
  "timestamp": "2024-12-17T12:00:00.000000Z"
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/health"
```

---

#### GET /
API information endpoint.

**Response:**
```json
{
  "message": "LeetVault API is running",
  "version": "1.0.0",
  "status": "healthy"
}
```

**Curl Command:**
```bash
curl "https://69481ac30014e1672988.sgp.appwrite.run/"
```

---

## Complete User Flow

### Step-by-Step Integration

```bash
# 1. Create User
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/users/check" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'

# Response: user_id, github_status=false, repo_activation=false

# 2. Get GitHub Installation URL
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/auth/github/install?email=user@example.com"

# Response: installation_url

# 3. User Opens URL in Browser
# - Installs GitHub App
# - Selects repositories
# - GitHub redirects to callback (automatic)
# - Callback stores installation, sets github_status=true

# 4. Get Available Repositories
curl "https://69481ac30014e1672988.sgp.appwrite.run/api/github/installations/YOUR_INSTALLATION_ID/repositories"

# Response: List of repositories

# 5. Activate Repository
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/repos/activate" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "installation_id": "YOUR_INSTALLATION_ID",
    "repo_name": "username/leetcode-solutions",
    "default_branch": "main"
  }'

# Response: Repository activated, repo_activation=true

# 6. Store LeetCode Credentials
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/leetcode/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "session_cookie": "YOUR_SESSION_COOKIE",
    "csrf_token": "YOUR_CSRF_TOKEN"
  }'

# Response: Credentials stored

# 7. Check Complete User Status
curl -X POST "https://69481ac30014e1672988.sgp.appwrite.run/api/users/check" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'

# Response: Complete user info with github_status=true, repo_activation=true, activated_repo details

# 8. (Optional) Deactivate Repository
curl -X DELETE "https://69481ac30014e1672988.sgp.appwrite.run/api/repos/deactivate/user@example.com"

# Response: Repository deactivated, repo_activation=false
```

---

## How to Get LeetCode Credentials

1. **Login to LeetCode** at https://leetcode.com
2. **Open Developer Tools** (F12 or Right-click → Inspect)
3. **Go to Application tab** (Chrome) or Storage tab (Firefox)
4. **Navigate to Cookies** → `https://leetcode.com`
5. **Copy these values:**
   - `LEETCODE_SESSION` → This is your `session_cookie`
   - `csrftoken` → This is your `csrf_token`

**Example Values:**
```
session_cookie: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTIzNDU2Ii...
csrf_token: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## Error Responses

### 400 Bad Request
Invalid request format or missing required fields.

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Database error: [error message]"
}
```

---

## Key Features & Constraints

### User ID System
- **Email**: `user@example.com`
- **User ID**: `user_example_com`
- Ensures uniqueness and valid Appwrite document IDs

### Constraints
- ✅ One user per email (enforced by document ID)
- ✅ One GitHub installation per user (enforced by unique userId index)
- ✅ One activated repository per user (enforced by unique userId index)
- ✅ One set of LeetCode credentials per user (enforced by unique userId index)

### Status Fields
- `github_status`: Boolean indicating if GitHub App is connected
- `repo_activation`: Boolean indicating if a repository is activated
- Both default to `false` on user creation
- Automatically updated when actions are performed

### Timestamps
- All timestamps in ISO 8601 format with 'Z' suffix
- Example: `2024-12-17T12:00:00.000000Z`

---

## Testing

### Health Check
```bash
curl https://69481ac30014e1672988.sgp.appwrite.run/health
```

### Note
Interactive documentation (Swagger UI/ReDoc) is not available in Appwrite Functions deployment.

### Test All Endpoints
Use the complete user flow above to test the entire integration.

---

## Notes

- All email addresses are normalized to lowercase
- Repository names must be in format: `username/repository`
- Default branch defaults to "main" if not specified
- Credentials can be updated by calling POST again
- Only one repository can be activated at a time per user
- Deactivating a repository removes it from activated_repos collection
