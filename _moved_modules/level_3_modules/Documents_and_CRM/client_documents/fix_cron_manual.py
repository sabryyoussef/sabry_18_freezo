#!/usr/bin/env python3
"""
Manual fix script for the cron job issue
Run this from the Odoo shell: exec(open('/path/to/fix_cron_manual.py').read())
"""

def manual_fix_cron():
    """
    Manual fix for the cron job issue
    """
    try:
        # Get the cron job record
        cron_job = env['ir.cron'].search([('id', '=', 'client_documents.client_documents_expiration_check')])
        
        if cron_job:
            print(f"Found cron job: {cron_job.name}")
            
            # Delete the problematic cron job
            cron_job.unlink()
            print("✅ Deleted problematic cron job")
            
            # Create a new one with correct fields
            new_cron = env['ir.cron'].create({
                'name': 'Check For Client\'s Expired Documents',
                'model_id': env.ref('client_documents.model_res_partner_document').id,
                'state': 'code',
                'active': True,
                'code': 'model.check_for_expiration()',
                'interval_number': 1,
                'interval_type': 'days',
                'priority': 5,
            })
            print(f"✅ Created new cron job with ID: {new_cron.id}")
        else:
            print("❌ Cron job not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the fix
manual_fix_cron() 