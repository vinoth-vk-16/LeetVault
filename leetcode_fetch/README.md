# LeetCode Fetch Service

A FastAPI service that automatically fetches LeetCode submissions and syncs them to GitHub repositories.

## Features

- 🔄 **Automatic Sync**: Automatically syncs LeetCode submissions to active GitHub repositories
- 📊 **Progress Tracking**: Generates `LeetcodeProgress.md` with problem statistics
- 🗂️ **Organized Structure**: Creates organized folder structure for problems and submissions
- 🔐 **GitHub App Integration**: Uses GitHub App for secure repository access
- 💾 **Appwrite Integration**: Stores user data and repository configurations
- 📝 **Multi-Language Support**: Supports multiple programming languages

## Architecture

The service integrates with:
- **LeetCode API**: Fetches submissions and problem data
- **GitHub API**: Pushes code to repositories
- **Appwrite Database**: Manages users, credentials, and active repositories

## API Endpoints

### POST `/sync`

Trigger sync for all active repositories or a specific user's repository.

**Request Body:**
```json
{
  "user_id": "optional_user_id"  // If omitted, syncs all active repos
}
```

**Response:**
```json
{
  "message": "Sync started successfully",
  "status": "running",
  "user_id": null
}
```

### GET `/status`

Get the current status of the sync process.

**Response:**
```json
{
  "status": "completed",
  "message": "Synced 1 repositories with 5 problems",
  "last_fetch_time": "2025-12-21T12:00:00",
  "problems_processed": 5,
  "submissions_downloaded": null
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "LeetCode Fetch Service"
}
```

## How It Works

1. **Fetch Active Repositories**: Queries Appwrite database for all active repositories
2. **Get User Credentials**: Retrieves LeetCode session cookies for each user
3. **Fetch Submissions**: Gets accepted submissions from the last 48 hours
4. **Process Problems**: For each problem:
   - Creates problem README with description
   - Saves solution template
   - Saves all submissions organized by language
5. **Update Progress**: Generates/updates `LeetcodeProgress.md` at repository root
6. **Push to GitHub**: Commits all changes directly to the main branch

## Repository Structure

When synced, the GitHub repository will have this structure:

```
repository/
├── LeetcodeProgress.md              # Main progress file (root)
└── leetcode/
    ├── easy-problems.md             # List of easy problems
    ├── medium-problems.md           # List of medium problems
    ├── hard-problems.md             # List of hard problems
    └── two-sum/                     # Problem folder
        ├── README.md                # Problem description
        ├── solutiontemplate.py      # Solution template
        └── submissions/
            └── python3/
                ├── 1234567890_approach_123.py
                └── 1234567891_approach_124.py
```

## Environment Variables

Create a `.env` file with the following variables:

```bash
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id

# GitHub App Configuration
GITHUB_APP_ID=1034567
GITHUB_PRIVATE_KEY_PATH="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"

# LeetCode API (optional)
GRAPHQL_URL=https://leetcode.com/graphql
```

## Database Schema

### activated_repos Collection

| Field | Type | Description |
|-------|------|-------------|
| userId | string | User identifier |
| installationId | string | GitHub App installation ID |
| repoFullName | string | Full repository name (owner/repo) |
| defaultBranch | string | Default branch (usually "main") |
| isActive | boolean | Whether the repo is active |
| activatedAt | datetime | When the repo was activated |
| lastSyncAt | datetime | Last sync timestamp |

### leetcode_credentials Collection

| Field | Type | Description |
|-------|------|-------------|
| userId | string | User identifier |
| sessionCookie | string | LeetCode session cookie |
| csrfToken | string | LeetCode CSRF token |
| leetcodeUsername | string | LeetCode username |

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` file with required environment variables

3. Run the service:

```bash
python main.py
```

The service will start on `http://0.0.0.0:8001`

## Usage

### Sync All Active Repositories

```bash
curl -X POST http://localhost:8001/sync \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Sync Specific User's Repository

```bash
curl -X POST http://localhost:8001/sync \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_email_com"}'
```

### Check Sync Status

```bash
curl http://localhost:8001/status
```

## Deployment on Appwrite

This service can be deployed as an Appwrite Function:

1. Create a new function in Appwrite
2. Set the runtime to Python 3.11
3. Upload the code
4. Configure environment variables
5. Set up a cron job or webhook to trigger `/sync` endpoint

## Features in Detail

### Automatic Problem Detection

- Only fetches submissions from the last 48 hours
- Filters for "Accepted" submissions only
- Avoids duplicate submissions

### Smart File Management

- Checks if files exist before creating/updating
- Uses file SHAs for updates to prevent conflicts
- Commits each problem separately for better git history

### Progress Tracking

- Generates beautiful markdown with statistics
- Separates problems by difficulty
- Links to individual problem folders
- Updates timestamp on each sync

## Troubleshooting

### JWT Token Errors

If you see "A JSON web token could not be decoded":
1. Verify your GitHub App ID is correct
2. Generate a new private key from GitHub App settings
3. Format the key properly with `\n` for newlines

### No Submissions Found

- Ensure LeetCode session cookie is valid
- Check that submissions are from the last 48 hours
- Verify submissions are marked as "Accepted"

### GitHub API Errors

- Check installation ID is correct
- Verify the GitHub App has write permissions
- Ensure the repository exists and is accessible

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
