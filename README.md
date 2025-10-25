# Freezoners 18 Enterprise - Custom Modules (Phase 2)

Odoo 18 Enterprise custom modules for the Freezoner project.
# Freezoner - Custom Odoo Modules

**Odoo Version:** 17.0  
**Total Modules:** 59  
**Status:** ✅ Successfully migrated from 16.0

---

## 📦 About

This directory contains custom Odoo modules for the Freezoner project. All modules have been successfully migrated from Odoo 16.0 to 17.0.

---

## 📁 Directory Structure

```
Freezoner/
├── README.md (this file)
├── Freezoner_Dependencies_Analysis.md
└── [59 module directories]
```

---

## 📚 Documentation

### Migration Documentation
- **Location:** `/odoo_migration_playbook/docs/freezoner_specific/`
- **Contents:** Migration guides, validation reports, issue tracking, dependencies analysis
- **Tools:** `/odoo_migration_playbook/tools/`
- **Note:** All migration docs and tools have been moved to the playbook for better organization

---

## 🔧 Module Configuration

**Odoo Configuration Path:**
```
addons_path = [...]/custom_addons/Freezoner
```

All 59 modules are accessible to Odoo from this single directory.

---

## ✅ Migration Status

- **From:** Odoo 16.0
- **To:** Odoo 17.0
- **Date:** October 2025
- **Status:** ✅ Complete
- **Success Rate:** 100%

---

## 📊 Module Statistics

| Metric | Value |
|--------|-------|
| **Total Modules** | 59 |
| **Successfully Migrated** | 59 |
| **Files Modified** | 100+ |
| **Lines Changed** | 5000+ |
| **Known Issues** | Documented in playbook |

---

## � Modules that declare a price

The following modules include a `price` field in their manifest (`__manifest__.py`). Prices are shown as found and normalized to numeric values where possible.

| Module | Manifest path (relative) | Price |
| --- | --- | ---: |
| bi_hr_equipment_asset_management | `bi_hr_equipment_asset_management/__manifest__.py` | 25 |
| bi_user_audit_management | `_quarantine/bi_user_audit_management/__manifest__.py` | 20 |
| hr_attendance_geofence | `_quarantine/hr_attendance_geofence/__manifest__.py` | 150.0 |
| hr_attendance_photo_geolocation | `_quarantine/hr_attendance_photo_geolocation/__manifest__.py` | 48.0 |
| hr_salary_certificate | `hr_salary_certificate/__manifest__.py` | 5 |
| ks_curved_backend_theme_enter | `_quarantine/ks_curved_backend_theme_enter/__manifest__.py` | 98.25 |
| partner_statement_knk | `_quarantine/partner_statement_knk/__manifest__.py` | 30 |
| payment_stripe_checkout | `_quarantine/payment_stripe_checkout/__manifest__.py` | 89.0 |
| stripe_fee_extension | `stripe_fee_extension/__manifest__.py` | 39.99 |

Notes:
- Several priced modules live in the `_quarantine/` folder.
- Values were parsed from `__manifest__.py` files and normalized to numbers where possible.

## 🧭 Module dependency levels

Below are modules grouped by dependency level within this repository. Prices were excluded (modules listed in the "Modules that declare a price" section are omitted from the graph).

<!-- Badges make the levels more scannable -->

Level summary: ![Level 0](https://img.shields.io/badge/Level%200-44-blue) ![Level 1](https://img.shields.io/badge/Level%201-8-green) ![Level 2](https://img.shields.io/badge/Level%202-1-yellow) ![Level 3](https://img.shields.io/badge/Level%203-1-lightgrey)

<details>
<summary><strong>Level 0</strong> — modules with no dependencies on other custom modules (they depend only on core/external modules)</summary>

The Level 0 modules are grouped by functional area for easier scanning. Each table shows module name, manifest path (relative), and declared `depends`.

### Accounting & Payments
| Module | Manifest path | Depends |
| --- | --- | --- |
| account_invoice_report | `account_invoice_report/__manifest__.py` | ['account','base','l10n_ae','sale'] |
| payment_status_in_sale | `payment_status_in_sale/__manifest__.py` | ['account','sale_management'] |
| payment_validation | `_quarantine/payment_validation/__manifest__.py` | ['account','base','project','sale'] |
| product_restriction | `product_restriction/__manifest__.py` | ['base','sale_management'] |

### CRM & Sales
| Module | Manifest path | Depends |
| --- | --- | --- |
| crm_assignation | `crm_assignation/__manifest__.py` | ['base','crm'] |
| crm_controller | `crm_controller/__manifest__.py` | ['base','crm'] |
| crm_lead_heat | `crm_lead_heat/__manifest__.py` | ['base','crm','sale'] |
| multiproject_saleorder | `multiproject_saleorder/__manifest__.py` | ['analytic','base','project','sale','sale_project'] |
| sales_person_customer_access | `sales_person_customer_access/__manifest__.py` | ['sale_management'] |
| bwa_f360_commission | `_quarantine/bwa_f360_commission/__manifest__.py` | ['base','sale','stock'] |

### HR & Attendance
| Module | Manifest path | Depends |
| --- | --- | --- |
| activity_dashboard_mngmnt | `activity_dashboard_mngmnt/__manifest__.py` | ['mail'] |
| discipline_system | `discipline_system/__manifest__.py` | ['base','hr_payroll','resource'] |
| employee_salesperson_task | `employee_salesperson_task/__manifest__.py` | ['base','hr'] |
| hr_attendance_ip_mac | `hr_attendance_ip_mac/__manifest__.py` | ['base','hr','hr_attendance'] |
| hr_attendance_location | `hr_attendance_location/__manifest__.py` | ['base','hr_attendance'] |
| hr_employee_custom | `hr_employee_custom/__manifest__.py` | ['base','hr','hr_attendance','hr_holidays','hr_payroll'] |
| hr_expense_custom | `hr_expense_custom/__manifest__.py` | ['base','hr_expense'] |
| hr_leave_custom | `hr_leave_custom/__manifest__.py` | ['base','hr','hr_holidays'] |
| leaves_check | `leaves_check/__manifest__.py` | ['base','hr_holidays'] |

### Project & Tasks
| Module | Manifest path | Depends |
| --- | --- | --- |
| kw_project_assign_wizard | `kw_project_assign_wizard/__manifest__.py` | ['project'] |
| project_by_client | `project_by_client/__manifest__.py` | ['base','project'] |
| project_partner_fields | `project_partner_fields/__manifest__.py` | ['base'] |
| task_update | `task_update/__manifest__.py` | ['base','project','sale'] |

### Partner & Customer
| Module | Manifest path | Depends |
| --- | --- | --- |
| client_birthday | `client_birthday/__manifest__.py` | ['base','contacts'] |
| client_categorisation | `client_categorisation/__manifest__.py` | ['base','contacts'] |
| client_documents | `client_documents/__manifest__.py` | ['base','contacts','project','sale_subscription','stock'] |
| partner_custom | `partner_custom/__manifest__.py` | ['base','documents','product'] |
| partner_fname_lname | `partner_fname_lname/__manifest__.py` | ['account','base','sale'] |
| partner_organization | `partner_organization/__manifest__.py` | ['base'] |
| partner_risk_assessment | `partner_risk_assessment/__manifest__.py` | ['base','crm'] |

### Reporting & Data
| Module | Manifest path | Depends |
| --- | --- | --- |
| report_xlsx | `report_xlsx/__manifest__.py` | ['base','web'] |
| ms_query | `ms_query/__manifest__.py` | ['base','mail'] |
| query_deluxe | `_quarantine/query_deluxe/__manifest__.py` | ['base','mail'] |

### Utilities & Admin
| Module | Manifest path | Depends |
| --- | --- | --- |
| database_cleanup | `database_cleanup/__manifest__.py` | ['base'] |
| hide_any_menu | `hide_any_menu/__manifest__.py` | ['base'] |
| premigration_hook | `premigration_hook/__manifest__.py` | [] |
| remove_studio_field | `remove_studio_field/__manifest__.py` | ['base','web','web_studio'] |
| freezoner_field_migration | `_quarantine/freezoner_field_migration/__manifest__.py` | ['base','hr_expense','project'] |
| freezoner_custom | `freezoner_custom/__manifest__.py` | ['base','documents_project','hr','hr_expense','mail','mass_mailing','product','project','sale','sale_project','stock','utm'] |
| freezoner_password | `freezoner_password/__manifest__.py` | ['approvals','base','project','sale'] |

### Integrations & Communication
| Module | Manifest path | Depends |
| --- | --- | --- |
| bwa_email_conf | `bwa_email_conf/__manifest__.py` | ['base','mail'] |
| odoo_whatsapp_integration | `_quarantine/odoo_whatsapp_integration/__manifest__.py` | ['account','base','contacts','purchase','sale','stock','web'] |
| odoo_attendance_user_location | `_quarantine/odoo_attendance_user_location/__manifest__.py` | ['base','hr','hr_attendance'] |
| prt_email_from | `prt_email_from/__manifest__.py` | ['mail'] |

</details>


<details>
<summary><strong>Level 1</strong> — modules that depend (directly) on Level 0 modules</summary>

The Level 1 modules are grouped functionally to clarify why they require Level 0 building blocks.

### HR & Attendance
| Module | Manifest path | Depends |
| --- | --- | --- |
| attendance_detection | `attendance_detection/__manifest__.py` | ['base','discipline_system','hr_attendance','hr_holidays','resource'] |

### Surveys & Portal
| Module | Manifest path | Depends |
| --- | --- | --- |
| bwa_survey | `bwa_survey/__manifest__.py` | ['base','freezoner_custom','portal','project','website'] |

### Documents & CRM
| Module | Manifest path | Depends |
| --- | --- | --- |
| cabinet_directory | `cabinet_directory/__manifest__.py` | ['base','client_documents','crm'] |
| crm_log | `crm_log/__manifest__.py` | ['base','client_documents','crm','sale','sale_crm','sales_team'] |
| crm_report | `crm_report/__manifest__.py` | ['base','crm','report_xlsx'] |

### Sales, Approvals & Finance
| Module | Manifest path | Depends |
| --- | --- | --- |
| freezoner_sale_approval | `freezoner_sale_approval/__manifest__.py` | ['approvals','base','freezoner_custom','project','sale'] |
| sales_commission | `sales_commission/__manifest__.py` | ['account_budget','analytic','base','crm','freezoner_custom','hr_payroll','sale','sale_management'] |

### Partner & Field Extensions
| Module | Manifest path | Depends |
| --- | --- | --- |
| partner_custom_fields | `partner_custom_fields/__manifest__.py` | ['base','hr','partner_risk_assessment'] |

</details>

<details>
<summary><strong>Level 2</strong> — modules that depend on Level 1 (or earlier) modules</summary>

### Compliance & Governance
| Module | Manifest path | Depends |
| --- | --- | --- |
| compliance_cycle | `compliance_cycle/__manifest__.py` | ['base','crm','crm_log','documents','freezoner_custom','partner_organization'] |

</details>

<details>
<summary><strong>Level 3</strong> — deeper dependency</summary>

### Project Customizations
| Module | Manifest path | Depends |
| --- | --- | --- |
| project_custom | `project_custom/__manifest__.py` | ['base','client_documents','compliance_cycle','freezoner_custom','partner_custom','partner_custom_fields'] |

</details>

> Notes:
> - Priced modules were excluded from the dependency graph and do not appear in these levels.
> - Level 0 modules depend only on core/external modules (no repo-local custom modules).
> - If you would like me to treat additional Odoo modules as "core" (for example `mail`, `sale`, or `account`) or to include priced modules in the graph, I can re-run and update this section.
## �🔗 Related Documentation

**Migration Playbook:**
- `/odoo_migration_playbook/` - Complete migration toolkit
- `/odoo_migration_playbook/docs/freezoner_specific/` - Freezoner-specific migration docs

**Dependencies:**
- `Freezoner_Dependencies_Analysis.md` - Module dependency analysis

---

## 📝 Notes

- All modules are configured with `auto_install: False`
- Module versions updated to 17.0
- Known issues documented in migration playbook
- For deployment strategies, see migration playbook

---

**Last Updated:** October 2025  
**Maintained By:** Freezoner Team  
**Odoo Version:** 17.0
