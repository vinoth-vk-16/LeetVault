# leetcode_fetch API Documentation

## Base URL

```
https://69481b400019e83f08ad.sgp.appwrite.run
```

---

## Endpoints

### 1. POST `/sync`

Trigger parallel sync for active repositories.

**Description**: Fetches LeetCode submissions for users with active repositories and pushes the data to their GitHub repos in parallel. Can sync all users or a specific user.

**Request Body** (optional):
```json
{
  "user_email": "user@example.com"  // Optional: sync only this user
}
```

**Examples**:

**Sync All Users:**
```bash
curl -X POST https://69481b400019e83f08ad.sgp.appwrite.run/sync \
  -H "Content-Type: application/json"
```

**Sync Specific User:**
```bash
curl -X POST https://69481b400019e83f08ad.sgp.appwrite.run/sync \
  -H "Content-Type: application/json" \
  -d '{"user_email": "imvinothvk521@gmail.com"}'
```

**Response (All Users)** (200 OK):
```json
{
  "message": "Parallel sync started for all active repositories",
  "status": "running",
  "user_email": null
}
```

**Response (Specific User)** (200 OK):
```json
{
  "message": "Sync started for user user@example.com",
  "status": "running",
  "user_email": "user@example.com"
}
```

**Error Response** (409 Conflict):
```json
{
  "detail": "Sync already in progress"
}
```

**Parameters**:
- `user_email` (optional): Email address of the user to sync. If omitted, syncs all active repositories.

**Notes**:
- Processes repositories concurrently using `asyncio.gather()`
- Returns immediately and runs sync in background
- Check `/status` endpoint for progress
- User email is converted to `userId` format internally (e.g., `user@example.com` → `user_example_com`)
- **Sends email notification** to each user after their sync completes with progress summary

---

### 2. GET `/status`

Get current sync status and statistics.

**Request**:
```bash
curl https://69481b400019e83f08ad.sgp.appwrite.run/status
```

**Response** (200 OK):

When idle:
```json
{
  "status": "idle",
  "message": "No sync in progress",
  "last_fetch_time": null,
  "problems_processed": 0,
  "submissions_downloaded": null
}
```

When running:
```json
{
  "status": "running",
  "message": "Syncing active repositories...",
  "last_fetch_time": "2025-12-22T12:00:00",
  "problems_processed": 0,
  "submissions_downloaded": null
}
```

When completed:
```json
{
  "status": "completed",
  "message": "Synced 950/1000 repositories with 4523 problems",
  "last_fetch_time": "2025-12-22T12:05:30",
  "problems_processed": 4523,
  "submissions_downloaded": null
}
```

**Status Values**:
- `idle` - No sync in progress
- `running` - Sync currently executing
- `completed` - Last sync finished successfully
- `error` - Last sync encountered errors

---

### 3. GET `/health`

Health check endpoint.

**Request**:
```bash
curl -X GET https://69481b400019e83f08ad.sgp.appwrite.run/health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "LeetCode Fetch Service"
}
```



## Sync Process Flow

```
1. POST /sync
   ↓
2. Fetch ALL active repositories from Appwrite
   ↓
3. For each repository, get user's LeetCode credentials
   ↓
4. Create async tasks for each repository
   ↓
5. Execute all tasks in parallel (asyncio.gather)
   ↓
6. For each repository (concurrent):
   - Fetch LeetCode submissions (GraphQL)
   - Generate markdown files
   - Push to GitHub (main branch)
   - Update lastSyncAt in database
   ↓
7. Return results with success/failure counts
```

---

## Generated Files Structure

When sync completes, each repository will contain:

```
repository-root/
├── LeetcodeProgress.md           # Main progress report
├── easy-problems.md              # All easy problems list
├── medium-problems.md            # All medium problems list
├── hard-problems.md              # All hard problems list
└── leetcode/
    ├── two-sum/
    │   ├── README.md             # Problem description & metadata
    │   └── solution.py           # User's solution code
    ├── reverse-linked-list/
    │   ├── README.md
    │   └── solution.cpp
    └── ...
```

---

## LeetcodeProgress.md Format

```markdown
# LeetCode Progress

## Statistics

- **Total Problems Solved**: 150
- **Easy**: 50
- **Medium**: 75
- **Hard**: 25

## Recent Submissions

| Problem | Difficulty | Language | Status | Date |
|---------|-----------|----------|--------|------|
| Two Sum | Easy | Python3 | Accepted | 2025-12-22 |
| ...

## Problems by Difficulty

### Easy (50)
- [Two Sum](./leetcode/two-sum/)
- ...

### Medium (75)
- [Add Two Numbers](./leetcode/add-two-numbers/)
- ...

### Hard (25)
- [Median of Two Sorted Arrays](./leetcode/median-of-two-sorted-arrays/)
- ...
```

---

## Error Handling

### Common Errors

#### 1. No LeetCode Credentials
```
⚠️ No LeetCode credentials found for user {user_id}
```

**Solution**: User needs to add LeetCode session cookie and CSRF token via frontend.

#### 2. Expired Session Cookie
```
❌ Failed to refresh session cookie. Please update your LeetCode credentials.
```

**Solution**: User needs to update their LeetCode credentials in the database.

#### 3. GitHub API 403
```
❌ Failed to create/update file: {"message":"Resource not accessible by integration"}
```

**Solution**: GitHub App needs "Contents: Read and write" permission.

#### 4. GitHub API 404
```
❌ Repository not found or not accessible
```

**Solution**: Check if repository exists and GitHub App is installed.

---

## Performance Metrics

### Sync Times (Approximate)

| Active Repos | Sequential | Parallel | Speed-up |
|--------------|-----------|----------|----------|
| 1            | 5-10s     | 5-10s    | 1x       |
| 10           | 50-100s   | 5-10s    | 10x      |
| 100          | 500-1000s | 5-15s    | 100x     |
| 1000         | 5000s+    | 10-20s   | 500x+    |

**Note**: Times vary based on:
- Number of submissions per user
- LeetCode API response time
- GitHub API rate limits
- Network latency

### Resource Usage

- **CPU**: High during parallel processing
- **Memory**: ~50MB per concurrent task
- **Network**: Depends on number of submissions
- **Appwrite API Calls**: 2-5 per repository
- **GitHub API Calls**: 5-20 per repository

---

## Rate Limits

### LeetCode API
- No official rate limit
- Recommended: Max 1000 concurrent requests
- Use session cookies for authentication

### GitHub API
- 5000 requests/hour per installation
- Parallel processing respects rate limits
- Automatic retry with exponential backoff

### Appwrite API
- Free tier: 1M requests/month
- Recommended: Index frequently queried fields
- Use pagination for large result sets

---

## Monitoring

### Check Sync Progress

Poll the `/status` endpoint:

```bash
while true; do
  curl -s https://69481b400019e83f08ad.sgp.appwrite.run/status | jq '.status, .message'
  sleep 5
done
```

### View Logs

Check Appwrite Functions console for detailed logs:
- Successful syncs: `✅ Successfully synced {repo}`
- Failed syncs: `❌ Failed to sync {repo}: {error}`
- Progress: `📊 Found {count} active repositories`

---

## Scheduling

### Appwrite Native Scheduler (Recommended)

The function automatically detects and handles scheduled execution from Appwrite.

**How to Configure:**

1. **Go to Appwrite Console** → Your Function → Settings
2. **Enable "Schedule"**
3. **Set Cron Expression**: `20 18 * * *` (6:20 PM UTC daily)
4. **Save**

**Cron Expression Examples:**

| Expression | Description |
|------------|-------------|
| `20 18 * * *` | Daily at 6:20 PM UTC |
| `0 */6 * * *` | Every 6 hours |
| `0 0,12 * * *` | Twice daily (midnight and noon) |
| `0 2 * * *` | Daily at 2:00 AM UTC |
| `0 0 * * 0` | Weekly on Sunday at midnight |

**How It Works:**

When Appwrite scheduler triggers the function:
1. Function detects scheduled execution (no headers, GET to `/`)
2. Runs `sync_all_active_repos()` directly
3. Returns JSON with results and timestamp

**Scheduled Response:**
```json
{
  "scheduled_sync": true,
  "results": [...],
  "executed_at": "2025-12-22T18:20:00",
  "message": "Scheduled sync completed successfully"
}
```

### Manual Trigger

For immediate sync or testing:

```bash
curl -X POST https://69481b400019e83f08ad.sgp.appwrite.run/sync
```

This triggers the sync via FastAPI endpoint (runs in background).

### Verify Schedule

Check **Appwrite Console** → Your Function → **Executions** to see scheduled runs.

---

## Testing

### Test Single Sync

```bash
# Trigger sync
curl -X POST https://69481b400019e83f08ad.sgp.appwrite.run/sync

# Wait a few seconds
sleep 10

# Check status
curl https://69481b400019e83f08ad.sgp.appwrite.run/status
```

### Test with Multiple Users

1. Create multiple test users in Appwrite
2. Activate repositories for each user
3. Add LeetCode credentials for each user
4. Trigger sync
5. Verify all repositories are updated

---

## Troubleshooting

### Sync Stuck in "running" State

**Cause**: Function crashed or timed out

**Solution**:
1. Check Appwrite Functions logs
2. Restart the function
3. Trigger sync again

### Some Repositories Not Syncing

**Cause**: Missing credentials or invalid sessions

**Solution**:
1. Check `leetcode_credentials` table
2. Verify session cookies are valid
3. Update expired credentials

### GitHub Push Failures

**Cause**: Permission issues or rate limits

**Solution**:
1. Verify GitHub App has "Contents: Read and write"
2. Check GitHub API rate limits
3. Review Appwrite logs for specific errors

---

## Email Notifications

### Overview

After each successful sync, the service automatically sends a beautiful HTML email to the user with their progress summary.

### Email Content

- **Subject**: `🎉 LeetVault Sync Complete - X Problems Synced`
- **Design**: Professional white theme with Times New Roman font
- **Branding**: LeetVault logo and gradient header
- **Content**:
  - Total problems synced
  - Easy problems count (green)
  - Medium problems count (yellow)
  - Hard problems count (red)
  - Repository name
  - Sync timestamp

### Configuration

Requires Gmail credentials in environment variables:

```env
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
```

**How to get Gmail App Password:**
1. Go to Google Account → Security → 2-Step Verification
2. Scroll to "App passwords"
3. Generate new app password for "Mail"
4. Copy the 16-character password

### Behavior

- ✅ If credentials configured: Sends email after each user's sync
- ⚠️ If credentials missing: Logs warning and continues without email
- ❌ If email fails: Logs error but doesn't fail the sync

---

## Security

### Authentication

- No authentication required for `/sync` endpoint
- Recommended: Add API key or webhook secret
- Deploy behind Appwrite Functions authentication

### Data Privacy

- LeetCode session cookies stored encrypted in Appwrite
- GitHub tokens generated per-request (not stored)
- User data isolated by `userId`
- Email credentials stored securely in environment variables

### Best Practices

1. Rotate Appwrite API keys regularly
2. Use environment variables for secrets
3. Enable Appwrite Functions logging
4. Monitor for suspicious activity
5. Implement rate limiting on public endpoints
6. Use Gmail App Password (not regular password)

---

## Support

For issues or questions:
- Check Appwrite Functions logs
- Review `README.md` for setup instructions
- Test endpoints using provided curl commands
- Check `DEPLOYMENT.md` for deployment guide

---

## Changelog

### v1.0.0 (2025-12-22)
- ✅ Parallel processing for all active repositories
- ✅ Automatic session refresh using CSRF token
- ✅ Improved error handling and logging
- ✅ Performance optimizations
- ✅ Comprehensive documentation

