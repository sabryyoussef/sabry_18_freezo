# Error Reporter Module - Quick Start Guide

## 🚀 Getting Started

### 1. Install the Module
1. Go to **Apps** in your Odoo interface
2. Search for "Error Reporter" 
3. Click **Install**

### 2. Access the Module
After installation, you can access Error Reporter in two ways:
- **Main App**: Look for "Error Reporter" in the main menu bar
- **Settings**: Go to Settings → Technical → Error Events

### 3. View Demo Data
The module comes with sample error data that demonstrates various error types:
- **Critical Errors**: Database issues, system failures
- **Errors**: Validation problems, access denied
- **Warnings**: Deprecated methods, missing data
- **Info**: Performance notices, rate limiting

## 📊 Exploring the Interface

### View Types
1. **Kanban View** (Default): Visual cards grouped by severity
2. **List View**: Tabular data with sortable columns  
3. **Graph View**: Charts and trends over time
4. **Pivot View**: Cross-tabulation analysis
5. **Form View**: Detailed individual error inspection

### Quick Actions
- **Filter Today**: See only today's errors
- **Search**: Type in the search bar to find specific errors
- **Group By**: Organize data by Source, Severity, Project, etc.

## 🔍 Understanding Error Data

### Error Sources
- **Odoo UI**: Frontend JavaScript errors
- **Odoo Server**: Backend Python exceptions  
- **Playwright**: Automated testing failures

### Severity Levels
- 🔴 **Critical**: Immediate attention required
- 🟠 **Error**: Functional issues
- 🟡 **Warning**: Potential problems
- 🔵 **Info**: Informational messages

### Key Fields
- **Message**: Main error description
- **Details**: Stack trace and technical info
- **Occurrences**: How many times this error happened
- **Fingerprint**: Unique identifier for grouping similar errors
- **Project/Scenario**: Context where error occurred

## 🛠 Manual Error Reporting

### From JavaScript (Frontend)
```javascript
// Report a custom error
window.QAErrorReporter.report(
    "My custom error message",
    "Additional details here",
    {
        source: 'odoo_ui',
        severity: 'error',
        project: 'My Module'
    }
);
```

### From Python (Backend)
```python
from odoo.addons.automatic_error_reporter.models.qa_error_event import log_server_exception

try:
    # Your risky code here
    pass
except Exception as e:
    log_server_exception(env, e, context={
        'severity': 'error',
        'project': 'My Project',
        'scenario': 'Data Processing'
    })
```

## 📈 Analytics Features

### Error Analytics Dashboard
Go to **Error Reporter → Analytics** to see:
- Error trends over time
- Breakdown by source and severity
- Project-wise error distribution
- User impact analysis

### Filters and Grouping
- **Time Filters**: Today, This Week, Custom ranges
- **Severity Filters**: Critical, Error, Warning, Info
- **Source Filters**: UI, Server, Playwright
- **Custom Grouping**: By project, user, date, etc.

## ⚙️ Configuration

### API Token (Important!)
1. Go to **Settings → Technical → Parameters → System Parameters**
2. Find key: `qa.error.api_token`  
3. Change the value from default to a secure token
4. This is required for error reporting to work

### User Permissions
**Error Reporter User**: Can view and report errors
**Error Reporter Admin**: Can manage all error data

Assign users to these groups in Settings → Users → [User] → Access Rights

## 🎯 Best Practices

### For Users
1. **Check daily**: Review today's errors regularly
2. **Use filters**: Focus on critical and error severity first
3. **Group by project**: See which modules need attention
4. **Monitor trends**: Use Analytics to spot patterns

### For Administrators  
1. **Set up proper permissions**: Assign appropriate groups
2. **Configure API token**: Use a secure, unique token
3. **Regular cleanup**: Archive old resolved errors
4. **Monitor critical errors**: Set up alerts for critical issues

### For Developers
1. **Use manual reporting**: Add error reporting to your custom modules
2. **Provide context**: Include project and scenario information
3. **Handle errors gracefully**: Don't let errors break user experience
4. **Monitor your modules**: Check for errors in your custom code

## 🔧 Troubleshooting

### Common Issues

**"Module not appearing"**
- Check user has "Error Reporter User" permission
- Refresh browser or clear cache

**"Permission denied"**  
- Assign "Error Reporter User" group to user
- Contact administrator for access

**"No errors showing"**
- Check if API token is configured
- Verify module is properly installed
- Look for JavaScript errors in browser console

## 📞 Support

For technical issues:
1. Check the error details and stack trace
2. Verify configuration (API token, permissions)  
3. Contact your system administrator
4. Check Odoo server logs for additional info

---

**Happy Error Tracking! 🐛→📊**