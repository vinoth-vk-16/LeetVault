# 🚀 LeetCode Fetch Service

Automated LeetCode sync service with Appwrite scheduled execution support.

## ✨ Features

- 🕐 **Appwrite Scheduled Execution**: Automatically triggered by Appwrite cron
- 🚀 **Parallel Processing**: Syncs ALL active repositories simultaneously
- 📊 **Progress Tracking**: Generates `LeetcodeProgress.md` with statistics
- 🗂️ **Organized Structure**: Creates problem folders with READMEs and solutions
- 🔐 **GitHub Integration**: Uses GitHub App for secure repository access
- 💾 **Appwrite Database**: Manages users, credentials, and active repos
- ⚡ **High Performance**: Can handle 1000+ users concurrently
- 🔄 **Dual Trigger**: Scheduled execution + manual trigger support
- 📧 **Email Notifications**: Sends beautiful HTML email reports after each sync

## 🧰 API Endpoints

### POST `/sync`

Manually trigger sync for active repositories.

**Request Body (optional):**
```json
{
  "user_email": "user@example.com"
}
```

**Response (all users):**
```json
{
  "message": "Parallel sync started for all active repositories",
  "status": "running",
  "user_email": null
}
```

**Response (specific user):**
```json
{
  "message": "Sync started for user user@example.com",
  "status": "running",
  "user_email": "user@example.com"
}
```

**Usage:**
```bash
# Sync all users
curl -X POST https://your-function-url/sync \
  -H "Content-Type: application/json"

# Sync specific user
curl -X POST https://your-function-url/sync \
  -H "Content-Type: application/json" \
  -d '{"user_email": "user@example.com"}'
```

### GET `/status`

Get the current status of the sync process.

**Response:**
```json
{
  "status": "completed",
  "message": "Synced 950/1000 repositories with 4523 problems",
  "last_fetch_time": "2025-12-22T18:20:00",
  "problems_processed": 4523
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

### GET `/`

Root endpoint with service information.

**Response:**
```json
{
  "service": "LeetCode Fetch Service",
  "version": "1.0.0",
  "endpoints": {
    "POST /sync": "Trigger sync (optionally with user_email)",
    "GET /status": "Get sync status",
    "GET /health": "Health check"
  }
}
```

## ⚙️ Appwrite Function Configuration

### Function Settings

| Setting           | Value                             |
| ----------------- | --------------------------------- |
| Runtime           | Python (3.9+)                     |
| Entrypoint        | `main.py`                         |
| Build Commands    | `pip install -r requirements.txt` |
| Permissions       | `any`                             |
| Timeout (Seconds) | 900 (15 minutes)                  |
| Execute Access    | `any` or `users`                  |

### Schedule Configuration (Optional)

To enable automatic scheduled syncing, configure in Appwrite Console:

**Appwrite Console → Functions → Your Function → Settings → Schedule**

| Setting           | Value                             |
| ----------------- | --------------------------------- |
| Schedule          | `20 18 * * *`                     |
| Description       | Daily sync at 6:20 PM UTC         |

**Cron Expression Examples:**
- `20 18 * * *` - Daily at 6:20 PM UTC
- `0 */6 * * *` - Every 6 hours
- `0 0,12 * * *` - Twice daily (midnight and noon)
- `0 2 * * *` - Daily at 2:00 AM UTC

**How it works:**
- Appwrite scheduler directly calls the `main()` function
- No HTTP endpoint needed - it's a direct function invocation
- The function will automatically sync all active repositories

## 🔒 Environment Variables

```env
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=your_database_id

# GitHub App Configuration
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY_PATH="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"

# Email Configuration (for sync notifications)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# Optional
GRAPHQL_URL=https://leetcode.com/graphql
```

### Setting Up Gmail App Password

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password
6. Add it to your environment variables as `GMAIL_APP_PASSWORD`

## 🕐 How Scheduled Execution Works

### Appwrite Scheduled Trigger

When Appwrite's scheduler triggers the function (e.g., `20 18 * * *`):

1. **Appwrite calls the function** with minimal context (no real HTTP request)
2. **Function detects scheduled execution**:
   - Path is `/`
   - Method is `GET`
   - No headers present
3. **Runs sync directly**: Calls `sync_all_active_repos()` immediately
4. **Returns results**: JSON response with sync statistics

**Detection Logic:**
```python
is_scheduled = (
    path == "/" and 
    method == "GET" and 
    (not hasattr(req, 'headers') or not req.headers or len(dict(req.headers)) == 0)
)
```

### Manual Trigger

You can also trigger sync manually anytime:

```bash
curl -X POST https://your-function-url/sync
```

This routes through FastAPI and runs sync synchronously (waits for completion before returning).

## 📧 Email Notifications

After each successful sync, users receive a beautiful HTML email with:

- **LeetVault branding** with gradient header
- **Total problems synced**
- **Breakdown by difficulty** (Easy, Medium, Hard)
- **Repository name**
- **Sync timestamp**
- **Professional white theme** with Times New Roman font

**Email Preview:**
- Clean, professional design
- Mobile-responsive layout
- Color-coded difficulty stats (Green for Easy, Yellow for Medium, Red for Hard)
- Motivational footer message

**Note**: Email notifications require Gmail credentials in environment variables. If not configured, sync will continue without sending emails.

## 📊 Generated Repository Structure

```
repository/
├── LeetcodeProgress.md              # Main progress file
├── easy-problems.md                 # Easy problems list
├── medium-problems.md               # Medium problems list
├── hard-problems.md                 # Hard problems list
└── leetcode/
    └── two-sum/
        ├── README.md                # Problem description
        ├── solutiontemplate.py      # Solution template
        └── submissions/
            └── python3/
                └── 1234567890_approach_123.py
```

## 🚀 Deployment to Appwrite Functions

### Step 1: Create Function

1. Go to Appwrite Console → Functions
2. Click "Create Function"
3. Choose "Python 3.9" runtime
4. Name it "leetcode_fetch"

### Step 2: Configure Settings

**Execution Settings:**
- Timeout: `900` seconds (15 minutes)
- Execute Access: `any`
- Entrypoint: `main.py`

**Schedule Settings:**
- Enable "Schedule"
- Cron Expression: `20 18 * * *` (6:20 PM UTC)

### Step 3: Set Environment Variables

Add all required environment variables (see section above)

### Step 4: Deploy Code

Upload your code or connect to Git repository

### Step 5: Activate

Enable the function and the schedule

**That's it!** Appwrite will now call your function daily at 6:20 PM UTC.

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with required variables
# Add all environment variables

# Run the service
python main.py
```

The service will start on `http://0.0.0.0:8001`.

## 📈 Performance

| Active Repos | Sync Time | Speed vs Sequential |
|--------------|-----------|---------------------|
| 1            | ~5-10s    | 1x                  |
| 100          | ~5-15s    | 100x                |
| 1000         | ~10-20s   | 500x+               |

## 🐛 Troubleshooting

### Schedule Not Triggering

1. **Check Schedule is Enabled** in Appwrite Console
2. **Verify Cron Expression** is correct
3. **Check Function Logs** in Appwrite Console for execution history
4. **Test Manually**: `curl -X POST https://your-function-url/sync`

### Sync Failures

- Verify LeetCode credentials are valid in database
- Check GitHub App has "Contents: Read and write" permission
- Review Appwrite Functions logs for detailed errors
- Check timeout is sufficient (900 seconds recommended)

### Function Timeout

If sync takes too long:
- Increase timeout in Appwrite settings (max 900s)
- Reduce number of active repositories
- Check for slow LeetCode API responses

### Manual Test

```bash
# Trigger sync manually
curl -X POST https://your-function-url/sync

# Check status
curl https://your-function-url/status
```

## 📝 License

MIT
