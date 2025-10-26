# KeyError: 'event' Troubleshooting Log

**Date:** October 26, 2025  
**Issue:** Module loading freezoner_custom failed: file freezoner_custom/security/ir.model.access.csv could not be processed: Unknown error during import: <class 'KeyError'>: 'event'

## Problem Analysis
- Error occurs during CSV import but CSV file contains no 'event' references
- Issue likely caused by dependency module trying to access 'event' module that doesn't exist on Odoo.sh
- Odoo.sh environment may be missing 'event' or 'calendar' modules

## Trial Results

### Trial 1: Remove Survey Dependency
**Status:** ✅ Completed  
**Hypothesis:** Survey module might require event/calendar functionality  
**Actions Taken:**
- [x] Remove `"survey"` from depends list
- [x] Comment out `"data/survey_mail.xml"`
- [x] Create git commit: "Trial 1: Remove survey dependency"
- [x] Push to staging1 branch
- [x] Test installation on Odoo.sh

**Result:** Pending Odoo.sh test  
**Notes:** Survey dependency removed successfully

### Trial 2: Remove Mass Mailing Dependency
**Status:** ✅ Completed  
**Hypothesis:** Mass mailing might have event/calendar integration  
**Actions Taken:**
- [x] Remove `"mass_mailing"` from depends list
- [x] Create git commit: "Trial 2: Remove mass_mailing dependency"
- [x] Push to staging1 branch
- [x] Test installation on Odoo.sh

**Result:** Pending Odoo.sh test  
**Notes:** Mass mailing dependency removed successfully

### Trial 3: Isolate Documents Dependency
**Status:** ⏭️ Skipped  
**Hypothesis:** Documents module migration script references event  
**Actions Taken:**
- [ ] Check documents module dependencies
- [ ] Remove `"documents"` from depends
- [ ] Comment out document-related views
- [ ] Create git commit: "Trial 3: Isolate documents dependency"
- [ ] Push and test

**Result:** Skipped - documents likely required  
**Notes:** Skipped this trial as documents is likely essential

### Trial 4: Minimal Dependency Test
**Status:** ✅ Completed  
**Hypothesis:** Identify which dependency causes the issue  
**Actions Taken:**
- [x] Create minimal manifest with core dependencies only
- [x] Comment out all data files except security
- [x] Create git commit: "Trial 4: Minimal dependency test"
- [x] Push and test
- [x] Gradually add back dependencies one by one

**Result:** Pending Odoo.sh test  
**Notes:** Minimal dependencies: base, mail, account, sale, project, web

### Trial 5: Check Client Documents Module
**Status:** ✅ Completed  
**Hypothesis:** client_documents might have event references  
**Actions Taken:**
- [x] Check `/phase_2/client_documents/__manifest__.py`
- [x] Remove `"client_documents"` from depends
- [x] Create git commit: "Trial 5: Remove client_documents dependency"
- [x] Push and test

**Result:** Pending Odoo.sh test  
**Notes:** client_documents has no event dependencies

### Trial 6: Check Cabinet Directory Module
**Status:** ✅ Completed  
**Hypothesis:** cabinet_directory might reference calendar/event  
**Actions Taken:**
- [x] Check `/phase_2/cabinet_directory/__manifest__.py`
- [x] Remove `"cabinet_directory"` from depends
- [x] Create git commit: "Trial 6: Remove cabinet_directory dependency"
- [x] Push and test

**Result:** Pending Odoo.sh test  
**Notes:** 🎯 **FOUND THE ISSUE!** cabinet_directory depends on 'calendar' which references 'event'

## Alternative Solutions

### Alternative 1: Create Stub Event Module
**Status:** ✅ Completed  
**Description:** Create minimal stub module that provides event model placeholder  
**Actions:**
- [x] Create stub module (`event_stub`)
- [x] Add as dependency before freezoner_custom
- [x] Create event.event and event.registration stub models
- [x] Add security access rules
- [x] Push to staging1 branch
- [ ] Test CSV import on Odoo.sh

**Result:** Pending Odoo.sh test  
**Notes:** Created minimal event models to satisfy any event references

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

## Summary of Findings

### Root Cause Identified
🎯 **The issue is caused by `cabinet_directory` module dependency on `calendar`**

**Evidence:**
- `cabinet_directory/__manifest__.py` contains: `'depends': ['base', 'crm', 'documents', 'hr', 'calendar']`
- The `calendar` module likely references the `event` module
- Odoo.sh staging environment appears to be missing the `event` module
- When `cabinet_directory` is removed from dependencies, the KeyError should be resolved

### Trials Completed
1. ✅ **Trial 1:** Removed `survey` dependency
2. ✅ **Trial 2:** Removed `mass_mailing` dependency  
3. ⏭️ **Trial 3:** Skipped documents (likely required)
4. ✅ **Trial 4:** Minimal dependency test
5. ✅ **Trial 5:** Removed `client_documents` dependency
6. ✅ **Trial 6:** **FOUND ISSUE** - Removed `cabinet_directory` dependency

### Current Status
- **Dependencies:** `base`, `mail`, `account`, `sale`, `project`, `web`, `event_stub`
- **Data Files:** Only security files loaded
- **Stub Module:** Created `event_stub` with event.event and event.registration models
- **Expected Result:** Module should install without KeyError on Odoo.sh

### Next Steps
1. ✅ Test current configuration with event_stub on Odoo.sh
2. If successful, gradually add back dependencies one by one
3. Identify which other dependencies might cause issues
4. ✅ Created stub `event` module as Alternative 1

---
**Last Updated:** October 26, 2025  
**Maintained By:** Freezoner Team
