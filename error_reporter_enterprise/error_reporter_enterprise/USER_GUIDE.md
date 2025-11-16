# Error Reporter Module - User Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Navigating the Interface](#navigating-the-interface)
4. [Understanding Error Events](#understanding-error-events)
5. [Using Different Views](#using-different-views)
6. [Filtering and Searching](#filtering-and-searching)
7. [Analytics and Reporting](#analytics-and-reporting)
8. [Manual Error Reporting](#manual-error-reporting)
9. [Administration](#administration)
10. [Troubleshooting](#troubleshooting)

## Overview

The Error Reporter module provides centralized error tracking and monitoring for your Odoo system. It automatically captures errors from:
- **UI/Frontend**: JavaScript errors and unhandled promises
- **Server**: Python exceptions and server-side errors
- **Playwright Tests**: Automated testing failures

## Getting Started

### Accessing the Module

After installation, you can access the Error Reporter in two ways:

1. **Main Application**: Click on "Error Reporter" in the main menu bar
2. **Settings Menu**: Go to Settings → Technical → Error Events (for administrators)

### First Login
1. Navigate to the Error Reporter application
2. You'll see the main dashboard with error events
3. If no errors exist yet, you'll see a welcome message

## Navigating the Interface

### Main Menu Structure
```
Error Reporter (Main App)
├── Error Events (Main view of all errors)
└── Analytics (Charts and statistics)
```

### Quick Access
- **Today's Errors**: Default filter shows today's errors
- **Search Bar**: Global search across error messages
- **View Switcher**: Toggle between different view types

## Understanding Error Events

### Error Event Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Source** | Where the error originated | `odoo_ui`, `odoo_server`, `playwright` |
| **Severity** | Error importance level | `info`, `warning`, `error`, `critical` |
| **Message** | Error description | "TypeError: Cannot read property 'id' of undefined" |
| **Details** | Stack trace or additional info | Full JavaScript stack trace |
| **Date** | When the error occurred | "2025-11-07 14:30:25" |
| **Occurrences** | How many times this error happened | 5 |
| **Project** | Project/module name | "Sales Module" |
| **Scenario** | Specific operation/context | "Create Invoice" |
| **User Login** | User who experienced the error | "admin@company.com" |
| **URL** | Page where error occurred | "/web#action=account.action_move" |
| **Browser** | User agent string | "Chrome 119.0.0.0" |
| **Fingerprint** | Unique error identifier | "a1b2c3d4e5f6..." |

### Severity Levels

- 🔴 **Critical**: System-breaking errors requiring immediate attention
- 🟠 **Error**: Functional issues that prevent normal operation
- 🟡 **Warning**: Issues that might cause problems but don't break functionality
- 🔵 **Info**: Informational messages for debugging

## Using Different Views

### 1. Kanban View (Default)
- **Purpose**: Visual overview of errors grouped by severity
- **Best for**: Quick scanning and priority assessment
- **Features**: 
  - Color-coded cards by severity
  - Key information at a glance
  - Drag-and-drop organization

### 2. List View
- **Purpose**: Tabular view of all errors
- **Best for**: Detailed analysis and bulk operations
- **Features**:
  - Sortable columns
  - Multi-select for bulk actions
  - Inline editing

### 3. Form View
- **Purpose**: Detailed view of individual errors
- **Best for**: Deep investigation of specific issues
- **Features**:
  - Full error details
  - Action buttons (Open URL, Open Trace)
  - Related error information

### 4. Graph View
- **Purpose**: Visual charts and trends
- **Best for**: Understanding error patterns over time
- **Features**:
  - Time-based error trends
  - Source and severity breakdowns
  - Interactive filtering

### 5. Pivot View
- **Purpose**: Cross-tabulation analysis
- **Best for**: Advanced analytics and reporting
- **Features**:
  - Multi-dimensional analysis
  - Drill-down capabilities
  - Export to Excel

## Filtering and Searching

### Quick Filters
- **Today**: Errors from today only
- **This Week**: Errors from the last 7 days
- **Critical**: Only critical severity errors
- **Error**: Only error severity
- **Warning**: Only warning severity

### Source Filters
- **Odoo UI**: Frontend JavaScript errors
- **Odoo Server**: Backend Python errors
- **Playwright**: Test automation errors

### Advanced Search
1. Use the search bar for text search across error messages
2. Click "Filters" to access advanced filtering options
3. Use "Group By" to organize data by different criteria

### Custom Filters
Create custom filters by:
1. Applying desired filter criteria
2. Clicking "Favorites" → "Save current search"
3. Naming your filter for future use

## Analytics and Reporting

### Error Analytics Dashboard
Access via: Error Reporter → Analytics

#### Key Metrics
- **Error Trends**: Daily/weekly error patterns
- **Source Distribution**: Breakdown by error source
- **Severity Analysis**: Critical vs. non-critical ratios
- **User Impact**: Which users are most affected

#### Chart Types
- **Bar Charts**: Compare error counts across categories
- **Line Charts**: Track error trends over time
- **Pie Charts**: Show proportional breakdowns

#### Export Options
- **PDF Reports**: Printable analytics reports
- **Excel Export**: Raw data for further analysis
- **CSV Export**: Data for external tools

## Manual Error Reporting

### Frontend JavaScript
```javascript
// Report a custom error
window.QAErrorReporter.report(
    "Custom error message",
    "Additional details or stack trace",
    {
        source: 'odoo_ui',
        severity: 'error',
        project: 'My Project',
        scenario: 'Custom Operation'
    }
);
```

### Backend Python
```python
from odoo.addons.automatic_error_reporter.models.qa_error_event import log_server_exception

try:
    # Your code that might fail
    result = risky_operation()
except Exception as e:
    log_server_exception(env, e, context={
        'severity': 'error',
        'project': 'Inventory Module',
        'scenario': 'Stock Movement',
        'user_login': env.user.login,
    })
```

## Administration

### User Permissions

#### Error Reporter User
- View error events
- Create new error reports
- Access basic analytics

#### Error Reporter Admin
- All user permissions
- Delete error events
- Access advanced configuration
- Manage user permissions

### Configuration

#### API Token Setup
1. Go to Settings → Technical → Parameters → System Parameters
2. Find key: `qa.error.api_token`
3. Set a secure token value
4. Save changes

#### Security Groups
1. Go to Settings → Users & Companies → Groups
2. Find "Tools" category
3. Assign users to appropriate Error Reporter groups

### Maintenance

#### Regular Cleanup
Consider implementing regular cleanup of old error events:
- Archive errors older than 90 days
- Keep only critical errors for extended periods
- Export important error reports before cleanup

## Troubleshooting

### Common Issues

#### "Module not appearing in menu"
**Solution**: Check user permissions
1. Settings → Users → Edit your user
2. Access Rights tab → Tools section
3. Enable "Error Reporter User"

#### "No errors being captured"
**Possible causes**:
1. API token not configured
2. JavaScript errors in browser console
3. Module not properly installed

**Solution**:
1. Verify API token in System Parameters
2. Check browser console for JavaScript errors
3. Restart Odoo service if needed

#### "Permission denied errors"
**Solution**: Assign proper security groups
1. User needs "Error Reporter User" group minimum
2. Admin operations require "Error Reporter Admin" group

### Performance Optimization

#### For High-Volume Environments
1. **Rate Limiting**: Built-in 5-second deduplication
2. **Archiving**: Regularly archive old errors
3. **Indexing**: Database indexes on fingerprint and date fields
4. **Cleanup**: Automated cleanup of resolved errors

### Support and Help

#### Getting Help
1. Check this user guide first
2. Look at error details for clues
3. Contact your system administrator
4. Check Odoo logs for additional information

#### Reporting Module Issues
When reporting issues with the Error Reporter module itself:
1. Include error message and stack trace
2. Specify Odoo version and module version
3. Describe steps to reproduce
4. Include relevant configuration details

---

## Quick Reference

### Keyboard Shortcuts
- `Ctrl + K`: Global search
- `Ctrl + /`: Toggle filters
- `Ctrl + ,`: Settings (if admin)

### URL Patterns
- Error Events: `/web#action=automatic_error_reporter.action_qa_error_event`
- Analytics: `/web#action=automatic_error_reporter.action_qa_error_event_graph`

### API Endpoints
- Get Token: `GET /qa/errors/token`
- Submit Error: `POST /qa/errors/ingest`

---

*For additional help or advanced configuration, contact your system administrator or refer to the technical documentation.*