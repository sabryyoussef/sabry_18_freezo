# KeyError: 'event' Troubleshooting Log

**Date:** October 26, 2025  
**Issue:** Module loading freezoner_custom failed: file freezoner_custom/security/ir.model.access.csv could not be processed: Unknown error during import: <class 'KeyError'>: 'event'

## Problem Analysis
- Error occurs during CSV import but CSV file contains no 'event' references
- Issue likely caused by dependency module trying to access 'event' module that doesn't exist on Odoo.sh
- Odoo.sh environment may be missing 'event' or 'calendar' modules

## Trial Results

### Trial 1: Remove Survey Dependency
**Status:** 🔄 In Progress  
**Hypothesis:** Survey module might require event/calendar functionality  
**Actions Taken:**
- [ ] Remove `"survey"` from depends list
- [ ] Comment out `"data/survey_mail.xml"`
- [ ] Create git commit: "Trial 1: Remove survey dependency"
- [ ] Push to staging1 branch
- [ ] Test installation on Odoo.sh

**Result:** Pending  
**Notes:** 

### Trial 2: Remove Mass Mailing Dependency
**Status:** ⏳ Pending  
**Hypothesis:** Mass mailing might have event/calendar integration  
**Actions Taken:**
- [ ] Remove `"mass_mailing"` from depends list
- [ ] Create git commit: "Trial 2: Remove mass_mailing dependency"
- [ ] Push to staging1 branch
- [ ] Test installation on Odoo.sh

**Result:** Pending  
**Notes:** 

### Trial 3: Isolate Documents Dependency
**Status:** ⏳ Pending  
**Hypothesis:** Documents module migration script references event  
**Actions Taken:**
- [ ] Check documents module dependencies
- [ ] Remove `"documents"` from depends
- [ ] Comment out document-related views
- [ ] Create git commit: "Trial 3: Isolate documents dependency"
- [ ] Push and test

**Result:** Pending  
**Notes:** Diagnostic step - documents is likely required

### Trial 4: Minimal Dependency Test
**Status:** ⏳ Pending  
**Hypothesis:** Identify which dependency causes the issue  
**Actions Taken:**
- [ ] Create minimal manifest with core dependencies only
- [ ] Comment out all data files except security
- [ ] Create git commit: "Trial 4: Minimal dependency test"
- [ ] Push and test
- [ ] Gradually add back dependencies one by one

**Result:** Pending  
**Notes:** 

### Trial 5: Check Client Documents Module
**Status:** ⏳ Pending  
**Hypothesis:** client_documents might have event references  
**Actions Taken:**
- [ ] Check `/phase_2/client_documents/__manifest__.py`
- [ ] Remove `"client_documents"` from depends
- [ ] Create git commit: "Trial 5: Remove client_documents dependency"
- [ ] Push and test

**Result:** Pending  
**Notes:** 

### Trial 6: Check Cabinet Directory Module
**Status:** ⏳ Pending  
**Hypothesis:** cabinet_directory might reference calendar/event  
**Actions Taken:**
- [ ] Check `/phase_2/cabinet_directory/__manifest__.py`
- [ ] Remove `"cabinet_directory"` from depends
- [ ] Create git commit: "Trial 6: Remove cabinet_directory dependency"
- [ ] Push and test

**Result:** Pending  
**Notes:** 

## Alternative Solutions

### Alternative 1: Create Stub Event Module
**Status:** ⏳ Pending  
**Description:** Create minimal stub module that provides event model placeholder  
**Actions:**
- [ ] Create stub module
- [ ] Add as dependency before freezoner_custom
- [ ] Test CSV import

### Alternative 2: Modify CSV Import
**Status:** ⏳ Pending  
**Description:** Split CSV into multiple files to identify problematic line  
**Actions:**
- [ ] Split `ir.model.access.csv` into multiple files
- [ ] Load incrementally
- [ ] Create separate CSV for each model access rule

### Alternative 3: Contact Odoo.sh Support
**Status:** ⏳ Pending  
**Description:** Document all trials and create support ticket  
**Actions:**
- [ ] Document all trials and results
- [ ] Create support ticket with Odoo.sh
- [ ] Request information about available modules

## Current Dependencies (Before Trials)
```python
"depends": [
    "base",
    "mail",
    "account",
    "documents",
    "sale",
    "sale_project",
    "web",
    "client_documents",
    "hr_expense",
    "project",
    "crm",
    "cabinet_directory",
    "mass_mailing",
    "survey",
]
```

## Next Steps
1. Execute Trial 1 (Remove Survey Dependency)
2. Test on Odoo.sh staging environment
3. Document results and proceed to next trial if needed

---
**Last Updated:** October 26, 2025  
**Maintained By:** Freezoner Team
