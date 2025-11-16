# GitHub Integration Guide

The Automatic Error Reporter now supports exporting errors as GitHub issues for better issue tracking and collaboration.

## Setup Instructions

### 1. Create a GitHub Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Odoo Error Reporter"
4. Select the **`repo`** scope (Full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't be able to see it again)

### 2. Configure in Odoo

1. Go to **Automatic Error Reporter > ⚙️ GitHub Settings**
2. Enter your GitHub repository in format: `username/repository-name`
3. Paste your Personal Access Token
4. Click **"Test Connection"** to verify the setup
5. Click **"Save Configuration"**

### 3. Export Errors

You can export errors in two ways:

#### Method 1: From the Menu
- Go to **Automatic Error Reporter > 📤 Export to GitHub**
- This will export all critical and error severity errors

#### Method 2: From the List View
- Go to **Automatic Error Reporter > All Errors**
- Use the **Action** menu and select **"📤 Export to GitHub Issues"**

## What Gets Exported

- **Only Critical and Error severity** errors are exported (to avoid spam)
- **Limited to 20 errors per export** (to respect GitHub API rate limits)
- Each error becomes a **GitHub issue** with:
  - Descriptive title with severity and source
  - Complete error details in markdown format
  - Proper labels for filtering (`severity:critical`, `source:frontend`, etc.)
  - All context information (user, URL, browser, etc.)
  - Technical details (fingerprint, logs, traces)

## GitHub Issue Format

Each exported error creates an issue like this:

```
Title: [CRITICAL] frontend: TypeError: Cannot read property 'id' of undefined

Labels: severity:critical, source:frontend, auto-export, odoo-error

Body:
## Error Details
**ID:** 123
**Date:** 2025-11-07 10:30:00
**Source:** frontend
**Severity:** critical
**Occurrences:** 5

## Message
TypeError: Cannot read property 'id' of undefined

## Details
Stack trace and error details...

## Context
- **Project:** MyProject
- **User:** admin
- **URL:** /web/action/123
- **Browser:** Chrome 119.0.0.0

## Technical
- **Fingerprint:** abc123def456
- **Tags:** javascript,ui
```

## Security Notes

- GitHub tokens are stored securely in Odoo system parameters
- Only administrators can configure GitHub integration
- Tokens are never displayed in the UI after being saved
- All API calls use HTTPS encryption

## Troubleshooting

### "Configuration Missing" Error
- Ensure both GitHub token and repository are configured
- Check that the repository format is correct: `username/repo-name`

### "Connection Failed" Error
- Verify your token has `repo` permissions
- Ensure the repository exists and is accessible
- Check that the repository name format is correct

### "No Errors to Export" Message
- Only Critical and Error severity errors are exported
- Check if you have any errors with these severity levels

### API Rate Limits
- GitHub allows 5,000 API requests per hour for authenticated users
- The export is limited to 20 errors per run to stay within limits
- If you hit rate limits, wait an hour before trying again

## Repository Setup Tips

1. **Create a dedicated repository** for error tracking (e.g., `mycompany-odoo-errors`)
2. **Set up issue templates** in your repository for consistent formatting
3. **Use GitHub Projects** to organize and prioritize error issues
4. **Set up notifications** to alert your development team of new errors
5. **Create labels** that match your workflow (e.g., `bug`, `frontend`, `backend`)

## Integration Benefits

- **Centralized Issue Tracking**: All errors in one place with your code
- **Team Collaboration**: Assign, comment, and track resolution progress
- **Integration with Development**: Link issues to pull requests and commits
- **Automated Workflows**: Use GitHub Actions to automate responses
- **Historical Tracking**: Keep a permanent record of all errors and fixes
