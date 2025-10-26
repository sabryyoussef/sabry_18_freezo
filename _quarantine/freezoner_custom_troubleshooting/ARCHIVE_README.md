# freezoner_custom Troubleshooting Archive

## Archive Information
- **Date Archived:** October 26, 2025
- **Reason:** KeyError: 'event' during module loading on Odoo.sh staging
- **Commit Hash:** 1af4600 (Update troubleshooting log: Trial 7 - Remove event_stub and res_groups)
- **Git Branch:** troubleshooting-keyerror-event

## Error Details
```
Exception: Module loading freezoner_custom failed: file freezoner_custom/security/ir.model.access.csv could not be processed: Unknown error during import: <class 'KeyError'>: 'event'
```

## Troubleshooting Trials Attempted

### Trial 1: Remove Survey Dependency
- **Status:** ❌ Failed
- **Action:** Removed `survey` from dependencies
- **Result:** KeyError persisted

### Trial 2: Remove Mass Mailing Dependency  
- **Status:** ❌ Failed
- **Action:** Removed `mass_mailing` from dependencies
- **Result:** KeyError persisted

### Trial 4: Minimal Dependency Test
- **Status:** ❌ Failed
- **Action:** Reduced to core dependencies: `base`, `mail`, `account`, `sale`, `project`, `web`
- **Result:** KeyError persisted

### Trial 5: Remove Client Documents
- **Status:** ❌ Failed
- **Action:** Removed `client_documents` dependency
- **Result:** KeyError persisted

### Trial 6: Remove Cabinet Directory
- **Status:** ❌ Failed
- **Action:** Removed `cabinet_directory` dependency (depends on calendar which references event)
- **Result:** KeyError persisted

### Alternative 1: Create Event Stub Module
- **Status:** ❌ Failed
- **Action:** Created `event_stub` module with event.event and event.registration models
- **Result:** KeyError persisted

### Alternative 2: Modify CSV Import
- **Status:** ❌ Failed
- **Action:** Split CSV file and used minimal content
- **Result:** KeyError persisted

### Trial 7: Remove Event Stub and Res Groups
- **Status:** ❌ Failed
- **Action:** Removed `event_stub` dependency and `res_groups.xml`
- **Result:** KeyError persisted

## Current Configuration (At Time of Archive)
- **Dependencies:** `base`, `mail`, `account`, `sale`, `project`, `web`
- **Data Files:** Only `security/ir.model.access.csv` (minimal content)
- **No event references:** All event-related code commented out or removed

## Next Steps
- Incremental rebuild approach starting from working version (commit e0ce089)
- Test each dependency and data file individually
- Identify exact point where KeyError occurs

## Files in Archive
- Complete `freezoner_custom` module directory
- All model files, view files, data files
- Troubleshooting log and documentation
- Git history preserved in branch `troubleshooting-keyerror-event`

---
**Archived By:** AI Assistant  
**Purpose:** Preserve troubleshooting work for reference during incremental rebuild
