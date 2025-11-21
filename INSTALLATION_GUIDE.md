# Quick Installation Guide - Circular Dependency Fix

## Overview
This guide provides step-by-step instructions for deploying the circular dependency fixes to your Odoo.sh instance.

## Prerequisites
- Access to Odoo.sh project: https://www.odoo.sh/project/freezoner/branches/oddo_fix_1/upgrade
- Git access to the repository
- Database backup (recommended)

## Implementation Summary
✅ Created 3 new Level 0 base modules
✅ Updated 5 Level 3 modules to use base modules
✅ Eliminated all circular dependencies
✅ Zero data loss approach

## Installation Steps

### Step 1: Commit and Push Changes
```bash
git add _moved_modules/level_0_modules/Partner_and_Customer/base_document_types/
git add _moved_modules/level_0_modules/Partner_and_Customer/base_business_structure/
git add _moved_modules/level_0_modules/Project_and_Tasks/base_project_products/
git add _moved_modules/level_3_modules/Documents_and_CRM/client_documents/
git add _moved_modules/level_3_modules/Documents_and_CRM/crm_log/
git add _moved_modules/level_3_modules/Compliance_and_Governance/compliance_cycle/
git add _moved_modules/level_3_modules/Freezoner_Customizations/freezoner_custom/
git add _moved_modules/level_3_modules/Project_Customizations/project_custom/
git add CIRCULAR_DEPENDENCY_RESOLUTION.md

git commit -m "Fix: Break circular dependencies by extracting base modules

- Created base_document_types (Level 0)
- Created base_business_structure (Level 0)
- Created base_project_products (Level 0)
- Updated all Level 3 modules to depend on base modules
- Eliminated circular dependencies between compliance_cycle, freezoner_custom, project_custom
- Consolidated duplicate res.partner.document.type definition
- Zero data loss - only code reorganization"

git push origin main
```

### Step 2: Install Base Modules in Odoo.sh

Navigate to: Apps → Update Apps List

#### Install in this order:
1. **base_document_types**
   - Search: "Base Document Types"
   - Click: Install
   - Wait for completion

2. **base_business_structure**
   - Search: "Base Business Structure"
   - Click: Install
   - Wait for completion

3. **base_project_products**
   - Search: "Base Project Products"
   - Click: Install
   - Wait for completion

### Step 3: Upgrade Level 3 Modules

Navigate to: Apps → Filter by "Installed"

#### Upgrade in this order:
1. **client_documents**
   - Click: Upgrade
   - Wait for completion

2. **crm_log**
   - Click: Upgrade
   - Wait for completion

3. **compliance_cycle**
   - Click: Upgrade
   - Wait for completion

4. **freezoner_custom**
   - Click: Upgrade
   - Wait for completion

5. **project_custom**
   - Click: Upgrade
   - Wait for completion

### Step 4: Verify Installation

#### Check Module Dependencies
Go to: Settings → Technical → Modules → Modules

For each Level 3 module, verify dependencies show base modules:
- compliance_cycle should show: base_document_types, base_business_structure, base_project_products
- freezoner_custom should show: base_document_types, base_project_products
- project_custom should show: base_document_types, base_business_structure, base_project_products

#### Check for Errors
Go to: Settings → Technical → Database Structure → Models

Search for:
- `res.partner.document.type` - should exist
- `business.structure` - should exist
- `project.project.products` - should exist

#### Test Functionality
1. Create a new document type
2. Create a new business structure
3. Associate a product with a project
4. Create a new shareholder
5. Verify all views load without errors

## Expected Results

### Before Fix
```
Error: Circular dependency detected
- compliance_cycle depends on freezoner_custom
- freezoner_custom depends on client_documents
- project_custom depends on compliance_cycle
```

### After Fix
```
✅ No circular dependencies
Level 0 modules installed independently
Level 3 modules installed successfully
All functionality preserved
```

## Troubleshooting

### Issue: "Module not found"
**Solution**: Run "Update Apps List" in Odoo.sh

### Issue: "Dependency not met"
**Solution**: Ensure base modules installed first in correct order

### Issue: "Model already exists"
**Solution**: This shouldn't happen. Check if old modules still installed. Uninstall and reinstall.

### Issue: "View not found"
**Solution**: Clear browser cache and refresh. Check server logs for XML errors.

## Rollback Plan

If critical issues occur:

1. **Immediate Rollback**:
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **Database Restore** (if needed):
   - Go to Odoo.sh → Branches → oddo_fix_1 → Backups
   - Restore latest backup before upgrade
   - Redeploy previous version

## Verification Checklist

- [ ] All base modules installed
- [ ] All Level 3 modules upgraded
- [ ] No errors in server logs
- [ ] Document types accessible
- [ ] Business structures accessible
- [ ] Project products accessible
- [ ] Shareholder management working
- [ ] All views rendering correctly
- [ ] No circular dependency errors
- [ ] Data integrity maintained

## Support

If you encounter issues:
1. Check the detailed documentation: `CIRCULAR_DEPENDENCY_RESOLUTION.md`
2. Review server logs in Odoo.sh
3. Check the testing checklist in the main document

## Success Indicators

✅ Installation completes without errors
✅ All modules show "Installed" status
✅ No circular dependency warnings
✅ All existing data accessible
✅ All views render properly
✅ Business workflows function normally

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Status**: Ready for Deployment
