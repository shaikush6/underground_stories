# Configuration Directory

## Required Files

### `youtube-credentials.json`
OAuth 2.0 credentials downloaded from Google Cloud Console.

**Setup Instructions:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop application)
4. Download JSON file and save here as `youtube-credentials.json`

### `youtube-token.pickle` (Auto-generated)
Authentication token created after first successful OAuth flow.

## Security

⚠️ **Never commit credential files to version control!**

These files are already excluded in `.gitignore`:
- `youtube-credentials.json`
- `youtube-token.pickle`
- `google-cloud-credentials.json`