#!/usr/bin/env python3
"""
Demo Data Loader for Error Reporter Module
This script creates realistic error data with proper timestamps
"""

import xmlrpc.client
import datetime
import random

# Odoo connection settings
ODOO_URL = 'http://localhost:8025'
ODOO_DB = 'edu_demo'
ODOO_USERNAME = 'admin'
ODOO_PASSWORD = 'admin'

def connect_odoo():
    """Connect to Odoo and return common and models objects"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return uid, models

def create_demo_errors(uid, models):
    """Create realistic demo error data"""
    
    # Generate timestamps for the last 30 days
    now = datetime.datetime.now()
    demo_errors = []
    
    # Recent critical errors (last 2 days)
    for i in range(3):
        error_time = now - datetime.timedelta(days=random.uniform(0, 2))
        demo_errors.append({
            'source': 'odoo_server',
            'severity': 'critical',
            'project': 'Database Module',
            'scenario': 'Backup Process',
            'user_login': 'system',
            'url': '/web#action=base.action_server_object_lines',
            'browser': 'System Process',
            'message': f'Database backup failed - disk space insufficient',
            'details': f'''DatabaseError: Backup operation failed at {error_time.strftime("%Y-%m-%d %H:%M:%S")}
Available disk space: 2.1 GB
Required space: 15.7 GB
Location: /opt/odoo/backups/
Process ID: {random.randint(1000, 9999)}''',
            'tags': 'backup,disk-space,critical',
            'occurrences': random.randint(1, 3),
            'date': error_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # UI errors from the last week
    ui_scenarios = [
        ('Sales Module', 'Product Catalog', '/shop/products'),
        ('Inventory Module', 'Stock Moves', '/web#action=stock.action_move'),
        ('Accounting Module', 'Journal Entries', '/web#action=account.action_move_journal_line'),
        ('CRM Module', 'Lead Management', '/web#action=crm.crm_lead_action_pipeline'),
        ('Website Module', 'Contact Form', '/contactus')
    ]
    
    for i in range(10):
        project, scenario, url = random.choice(ui_scenarios)
        error_time = now - datetime.timedelta(days=random.uniform(0, 7))
        severity = random.choice(['error', 'warning', 'error', 'warning', 'critical'])
        
        demo_errors.append({
            'source': 'odoo_ui',
            'severity': severity,
            'project': project,
            'scenario': scenario,
            'user_login': random.choice(['admin', 'sales.user', 'stock.user', 'demo']),
            'url': url,
            'browser': random.choice([
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
            ]),
            'message': random.choice([
                f'TypeError: Cannot read properties of undefined (reading \'id\') in {scenario.lower()}',
                f'RPC_ERROR: Failed to load {scenario.lower()} data',
                f'NetworkError: Failed to fetch {scenario.lower()} information',
                f'ValidationError: Invalid data format in {scenario.lower()} form',
                f'TimeoutError: Request timeout while loading {scenario.lower()}'
            ]),
            'details': f'''Error occurred in {project} - {scenario}
Timestamp: {error_time.strftime("%Y-%m-%d %H:%M:%S")}
User Agent: {random.choice(['Chrome 119', 'Firefox 119', 'Safari 17'])}
Session ID: {random.randint(100000, 999999)}
Stack trace available in browser console''',
            'tags': f'{project.lower().replace(" ", "-")},{scenario.lower().replace(" ", "-")},frontend',
            'occurrences': random.randint(1, 8),
            'date': error_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Server errors from the last 2 weeks
    server_scenarios = [
        ('Email Module', 'Mail Sending', 'SMTP connection failed'),
        ('Report Module', 'PDF Generation', 'Wkhtmltopdf process crashed'),
        ('Integration Module', 'API Sync', 'External API rate limit exceeded'),
        ('Security Module', 'User Authentication', 'LDAP connection timeout'),
        ('Backup Module', 'Scheduled Backup', 'Permission denied on backup directory')
    ]
    
    for i in range(8):
        project, scenario, base_message = random.choice(server_scenarios)
        error_time = now - datetime.timedelta(days=random.uniform(0, 14))
        severity = random.choice(['error', 'warning', 'error'])
        
        demo_errors.append({
            'source': 'odoo_server',
            'severity': severity,
            'project': project,
            'scenario': scenario,
            'user_login': random.choice(['admin', 'system', 'integration.user']),
            'url': f'/web#action={project.lower().replace(" ", "_")}.action',
            'browser': 'Server Process',
            'message': base_message,
            'details': f'''{base_message}
Error occurred at: {error_time.strftime("%Y-%m-%d %H:%M:%S")}
Process: {random.choice(['cron', 'web', 'longpolling'])}
PID: {random.randint(1000, 9999)}
Memory usage: {random.randint(50, 200)}MB
Server load: {random.uniform(0.1, 2.5):.2f}''',
            'tags': f'{project.lower().replace(" ", "-")},{scenario.lower().replace(" ", "-")},server',
            'occurrences': random.randint(1, 15),
            'date': error_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Playwright test errors from the last month
    test_scenarios = [
        ('E-commerce Tests', 'Product Search', 'Search results not loading'),
        ('Authentication Tests', 'User Login', 'Login form submission failed'),
        ('Checkout Tests', 'Payment Process', 'Payment gateway timeout'),
        ('Performance Tests', 'Page Load Speed', 'Page load time exceeded threshold'),
        ('Mobile Tests', 'Responsive Layout', 'Element not visible on mobile')
    ]
    
    for i in range(6):
        project, scenario, base_message = random.choice(test_scenarios)
        error_time = now - datetime.timedelta(days=random.uniform(0, 30))
        severity = random.choice(['error', 'warning', 'info'])
        
        demo_errors.append({
            'source': 'playwright',
            'severity': severity,
            'project': project,
            'scenario': scenario,
            'user_login': 'test.automation',
            'url': random.choice(['/shop', '/web/login', '/shop/checkout', '/contactus']),
            'browser': f'Playwright/{random.choice(["1.40.0", "1.39.0"])} Chromium/{random.choice(["119.0.6045.9", "118.0.5993.88"])}',
            'message': base_message,
            'details': f'''{base_message}
Test file: /home/tests/e2e/{scenario.lower().replace(" ", "_")}.spec.js
Test duration: {random.randint(5, 45)} seconds
Screenshot: available
Video: recorded
Trace: https://trace.playwright.dev/{random.randint(100000, 999999)}''',
            'trace_url': f'https://trace.playwright.dev/trace_{random.randint(100000, 999999)}',
            'tags': f'{project.lower().replace(" ", "-")},{scenario.lower().replace(" ", "-")},automation',
            'occurrences': random.randint(1, 5),
            'date': error_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Create the error records
    created_count = 0
    for error_data in demo_errors:
        try:
            error_id = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                'qa.error.event', 'create',
                [error_data]
            )
            created_count += 1
            print(f"✓ Created error {created_count}: {error_data['message'][:50]}...")
        except Exception as e:
            print(f"✗ Failed to create error: {e}")
    
    print(f"\n🎉 Successfully created {created_count} demo error records!")
    return created_count

def main():
    """Main function to load demo data"""
    print("🚀 Loading Error Reporter Demo Data...")
    print(f"Connecting to Odoo at {ODOO_URL}...")
    
    try:
        uid, models = connect_odoo()
        print(f"✓ Connected successfully as user ID: {uid}")
        
        # Check if the module is installed
        module_ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'ir.module.module', 'search',
            [[('name', '=', 'automatic_error_reporter'), ('state', '=', 'installed')]]
        )
        
        if not module_ids:
            print("❌ Error Reporter module is not installed!")
            return
        
        print("✓ Error Reporter module is installed")
        
        # Create demo data
        created_count = create_demo_errors(uid, models)
        
        # Print summary
        print(f"\n📊 Demo Data Summary:")
        print(f"   • Total errors created: {created_count}")
        print(f"   • Time range: Last 30 days")
        print(f"   • Sources: UI, Server, Playwright")
        print(f"   • Severities: Critical, Error, Warning, Info")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Go to Error Reporter → Error Events")
        print(f"   2. Try different views (Kanban, List, Graph, Pivot)")
        print(f"   3. Use filters to explore the data")
        print(f"   4. Check out Error Reporter → Analytics")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()