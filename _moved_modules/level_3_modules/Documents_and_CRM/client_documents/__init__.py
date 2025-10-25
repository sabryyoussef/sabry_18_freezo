from . import models, wizard

def post_init_hook(cr, registry=None):
    """
    Post-installation hook to check and prevent demo data corruption
    """
    from odoo import api, SUPERUSER_ID
    
    # Handle both old and new calling conventions
    if registry is None:
        # If registry is not provided, try to get it from cr
        try:
            from odoo.modules.registry import Registry
            registry = Registry(cr.dbname)
        except Exception:
            print("⚠️ Could not get registry for post_init_hook")
            return
    
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Fix cron job issue with numbercall field
    try:
        cron_job = env['ir.cron'].search([('id', '=', 'client_documents.client_documents_expiration_check')])
        if cron_job:
            print(f"🔧 Found cron job: {cron_job.name}")
            
            # Check if it has the problematic numbercall field
            if hasattr(cron_job, 'numbercall'):
                print("❌ Cron job has numbercall field - removing it")
                # Remove the numbercall field from the record
                cron_job.write({'numbercall': False})
                print("✅ Removed numbercall field")
            else:
                print("✅ Cron job doesn't have numbercall field")
                
            # Update the cron job with correct fields
            cron_job.write({
                'name': 'Check For Client\'s Expired Documents',
                'model_id': env.ref('client_documents.model_res_partner_document').id,
                'state': 'code',
                'active': True,
                'code': 'model.check_for_expiration()',
                'interval_number': 1,
                'interval_type': 'days',
                'priority': 5,
            })
            print("✅ Updated cron job with correct fields")
        else:
            print("📝 Cron job not found - will be created during data loading")
    except Exception as e:
        print(f"⚠️ Error fixing cron job: {e}")
    
    # Check if demo data installation is tracked
    demo_installed_param = env['ir.config_parameter'].sudo().search([
        ('key', '=', 'client_documents.demo_data_installed')
    ])
    
    if demo_installed_param:
        print("✅ Demo data installation already tracked - skipping demo data check")
        return
    
    # Check if demo data already exists
    existing_categories = env['res.partner.document.category'].search_count([])
    existing_types = env['res.partner.document.type'].search_count([])
    existing_docs = env['res.partner.document'].search_count([])
    
    # Check for demo partners
    demo_partners = env['res.partner'].search_count([
        ('name', 'in', ['ACME Corporation', 'John Doe', 'Tech Solutions Inc.', 'Jane Smith'])
    ])
    
    if existing_categories > 0 or existing_types > 0 or existing_docs > 0 or demo_partners > 0:
        print("⚠️  Demo data already exists - marking as installed to prevent corruption")
        env['ir.config_parameter'].sudo().set_param('client_documents.demo_data_installed', 'true')
    else:
        print("📝 No existing demo data found - ready for demo data installation")
