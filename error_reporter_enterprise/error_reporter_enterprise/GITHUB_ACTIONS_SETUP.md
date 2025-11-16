# GitHub Actions Setup - Convert Issues to Files

This guide shows you how to set up a GitHub Action that automatically converts your Odoo error issues into organized files and folders in your repository.

## 🎯 What This Does

The GitHub Action will:
- ✅ **Find all issues** with the `auto-export` label (created by Odoo)
- ✅ **Convert each issue** into a markdown file
- ✅ **Organize files by date** in folders like `errors/2025-11-07/`
- ✅ **Create README files** for each date with summaries
- ✅ **Generate an index** with overview of all errors
- ✅ **Run automatically** when new issues are created

## 📁 File Structure Created

```
your-repo/
├── errors/
│   ├── index.md                    ← Main overview
│   ├── 2025-11-07/                 ← Date folder
│   │   ├── README.md               ← Daily summary
│   │   ├── issue_1_critical_database_connection_lost.md
│   │   ├── issue_2_error_validation_failed.md
│   │   └── issue_3_critical_ui_crash.md
│   ├── 2025-11-06/                 ← Another date
│   │   ├── README.md
│   │   └── issue_4_error_api_timeout.md
│   └── ...
```

## 🚀 Setup Instructions

### Step 1: Create the Workflow Directory
In your GitHub repository, create this folder structure:
```
.github/
└── workflows/
```

### Step 2: Add the Workflow File
1. **Go to your repository**: https://github.com/sabryyoussef/error_reporting_test
2. **Click "Create new file"**
3. **Name it**: `.github/workflows/convert-issues-to-files.yml`
4. **Copy the content** from: `custom_addons/automatic_error_reporter/github_workflows/convert-issues-to-files.yml`
5. **Commit the file**

### Step 3: Test the Action
1. **Go to Actions tab** in your repository
2. **Find "Convert Issues to Files"** workflow
3. **Click "Run workflow"** to test it manually
4. **Check the results** in the `errors/` folder

## ⚙️ How It Works

### Automatic Triggers
- **New Issue Created**: Runs when Odoo creates a new issue
- **Issue Updated**: Runs when an issue is modified  
- **Scheduled**: Runs every 6 hours to catch any missed issues
- **Manual**: You can trigger it manually from Actions tab

### File Naming Convention
Issues are converted to files with this pattern:
```
issue_{number}_{severity}_{safe_title}.md
```

Examples:
- `issue_1_critical_database_connection_lost.md`
- `issue_2_error_validation_failed_in_sales.md`
- `issue_3_warning_deprecated_method_used.md`

### Content Structure
Each file contains:
- ✅ **Original issue information** (number, dates, labels, URL)
- ✅ **Complete error details** (from issue body)
- ✅ **Link back to GitHub issue**
- ✅ **Metadata** (when converted, by whom)

## 📊 Generated Reports

### Daily README Files
Each date folder gets a `README.md` with:
- Issue count for that date
- Table of all issues with links
- List of generated files
- Severity breakdown

### Main Index File
The `errors/index.md` provides:
- Overview of all dates
- Total issue counts
- Quick stats by severity
- Navigation links

## 🔧 Customization Options

### Change Schedule
Edit the cron expression in the workflow:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 0 * * *'    # Daily at midnight
  - cron: '0 */1 * * *'  # Every hour
```

### Filter Different Labels
Change which issues to process:
```yaml
labels: 'auto-export,odoo-error'  # Multiple labels
labels: 'bug'                     # Different label
```

### Modify File Structure
Edit the date folder format:
```javascript
const dateKey = createdDate.toISOString().split('T')[0]; // YYYY-MM-DD
// Or use:
const dateKey = `${createdDate.getFullYear()}-${String(createdDate.getMonth() + 1).padStart(2, '0')}`;  // YYYY-MM
```

## 🎉 Benefits

1. **Organized Structure**: Easy to browse errors by date
2. **Searchable Files**: Use GitHub's search to find specific errors
3. **Version Control**: Track changes to error reports over time
4. **IDE Friendly**: Clone repo and browse errors in your favorite editor
5. **Automated**: No manual work needed after setup
6. **Backup**: Issues are preserved as files even if GitHub issues are deleted

## 🔍 Monitoring

### Check Action Status
1. Go to **Actions** tab in your repository
2. Look for **"Convert Issues to Files"** runs
3. Click on runs to see logs and debug any issues

### Verify Results
After the action runs, check:
- `errors/` folder exists
- Date folders are created (e.g., `errors/2025-11-07/`)
- Files are generated for each issue
- README files contain correct summaries

## 🚨 Troubleshooting

### Action Fails
- Check the **Actions** tab for error logs
- Verify repository has **write permissions** for the action
- Ensure issues have the correct labels (`auto-export`)

### No Files Created
- Verify issues exist with `auto-export` label
- Check if action has permission to write files
- Look at action logs for specific errors

### Files Not Updated
- Action might be cached - try manual trigger
- Check if issues were actually modified
- Verify cron schedule is correct

---

## 🎯 Next Steps

1. **Set up the workflow** following the instructions above
2. **Test it manually** to see it working
3. **Create new issues from Odoo** to see automatic conversion
4. **Customize** the structure to fit your needs

The result will be a beautifully organized file structure that makes it easy to browse, search, and analyze your Odoo errors directly in your IDE! 🚀
