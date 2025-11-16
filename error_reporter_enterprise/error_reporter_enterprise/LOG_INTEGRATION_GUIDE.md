# Log File Integration Guide

## Overview

The Error Reporter module now includes powerful log file integration capabilities that automatically capture and link server errors from Odoo logs. This feature works across different deployment environments including local development, dedicated servers, and Odoo.sh.

## Features

### Automatic Log Capture
- **Real-time monitoring**: Automatically captures WARNING, ERROR, and CRITICAL level log entries
- **Smart filtering**: Only captures relevant errors to avoid noise
- **Log file linking**: Associates errors with their source log files
- **Line number tracking**: Records the exact line number where errors occur

### Multi-Environment Support
- **Local Development**: Direct file path access (`/var/log/odoo/odoo.log`)
- **Dedicated Servers**: Full path with remote access capabilities
- **Odoo.sh**: URL-based log access integration

## Configuration

### 1. Enable Log Capture

Navigate to **QA Tools → Error Events → Log Capture Settings** and use the server actions:

- **Enable Log Capture**: Registers the log handler to start automatic capture
- **Test Log Capture**: Generates sample log entries for testing
- **Disable Log Capture**: Stops automatic log capture

### 2. Log File Field Configuration

Each error event can include:

| Field | Description | Example |
|-------|-------------|---------|
| `log_file_path` | Full system path to log file | `/var/log/odoo/odoo.log` |
| `log_file_url` | URL for remote log access | `https://www.odoo.sh/my/projects/12345/logs` |
| `log_line_number` | Exact line number in log file | `1543` |
| `log_level` | Original log level from server | `ERROR`, `WARNING`, `CRITICAL` |

## Usage Examples

### Development Environment
```python
# Error automatically captured with:
log_file_path: "/home/user/odoo/odoo.log"
log_line_number: 1234
log_level: "ERROR"
```

### Production Server
```python
# Error automatically captured with:
log_file_path: "/var/log/odoo/odoo-server.log"
log_file_url: "https://server.company.com/logs/odoo.log"
log_line_number: 5678
log_level: "CRITICAL"
```

### Odoo.sh Environment
```python
# Error automatically captured with:
log_file_url: "https://www.odoo.sh/my/projects/12345/logs"
log_line_number: 9876
log_level: "WARNING"
```

## Manual Error Reporting with Log Context

You can also manually create errors with log context:

```python
# From server code
env['qa.error.event'].create({
    'source': 'server',
    'scenario': 'custom_operation',
    'severity': 'error',
    'message': 'Custom operation failed',
    'log_file_path': '/var/log/odoo/odoo.log',
    'log_line_number': 1234,
    'log_level': 'ERROR'
})
```

## Integration with Existing Systems

### Log Rotation Compatibility
The system handles log rotation gracefully:
- Tracks current log file automatically
- Updates paths when logs rotate
- Maintains historical references

### Performance Considerations
- **Efficient filtering**: Only processes WARNING+ level messages
- **Async processing**: Log capture doesn't block server operations
- **Rate limiting**: Prevents log spam from creating duplicate errors

## Troubleshooting

### Common Issues

1. **Log handler not registering**
   - Check server permissions for log file access
   - Verify user has admin rights in Error Reporter module

2. **Missing log file paths**
   - Check `ODOO_LOG_FILE` environment variable
   - Verify log file exists and is readable

3. **Line numbers incorrect**
   - Log rotation may affect line numbers
   - Numbers are estimated for performance reasons

### Debug Mode

Enable debug logging to see log handler activity:
```bash
# In odoo.conf
log_level = debug
log_handler = :DEBUG,werkzeug:CRITICAL,odoo.addons.automatic_error_reporter:DEBUG
```

## Best Practices

### Development
- Enable log capture during development for comprehensive error tracking
- Use test log generation to verify setup
- Configure local log file paths correctly

### Production
- Set up log file URLs for remote access
- Configure log rotation policies
- Monitor error patterns through the dashboard

### Odoo.sh
- Use URL-based log access exclusively
- Monitor project logs through Odoo.sh interface
- Set up alerts for critical errors

## API Reference

### Log Handler Manager

```python
# Register log handler
env['qa.log.handler.manager'].register_log_handler()

# Test log capture
env['qa.log.handler.manager'].test_log_capture()

# Unregister handler
env['qa.log.handler.manager'].unregister_log_handler()
```

### Error Event Model

```python
# Register handler from error event model
env['qa.error.event'].register_log_handler()

# Create error with log context
env['qa.error.event'].create({
    'message': 'Error message',
    'log_file_path': '/path/to/log',
    'log_line_number': 123,
    'log_level': 'ERROR'
})
```

## Security Notes

- Log file access requires appropriate system permissions
- URL-based log access should use secure connections (HTTPS)
- Log handler registration requires Error Reporter Admin rights
- Log file paths are stored but not directly accessible through UI for security

## Future Enhancements

- Real-time log streaming integration
- Advanced log parsing for structured data
- Integration with external log management systems
- Automated error pattern recognition
- Log-based alerting and notifications