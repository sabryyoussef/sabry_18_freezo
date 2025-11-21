# Base Business Structure

## Overview

This module provides the core business structure and shareholder management functionality for the Freezoner platform. It serves as a base module to break circular dependencies between Level 3 modules.

## Features

- **Business Structure Management**: Define organizational structure types (LLC, Corporation, etc.)
- **Business Relationships**: Define relationship types between business entities
- **Shareholder Tracking**: Comprehensive shareholder information management
- **UBO Management**: Ultimate Beneficial Owner tracking for compliance

## Models

### business.structure
Define types of business organizational structures with:
- Name and code
- Related business relationships
- Active flag for archiving

### business.relationships
Relationship types between business entities with:
- Name and description
- Code for identification
- Active flag

### res.partner.ubo
Ultimate Beneficial Owner types for compliance with:
- Name and description
- Code and active flag

### res.partner.business.shareholder
Comprehensive shareholder management with:
- Project and partner associations
- Shareholding percentage tracking
- Individual and corporate shareholder information
- Document references (passport, visa, trade license, etc.)
- Contact information
- Nationality and gender tracking
- License and incorporation details

## Partner Extension

Extends `res.partner` with:
- `compliance_shareholder_ids`: One2many field for shareholder records
- `business_structure_id`: Many2one field for business structure type
- Auto-population of shareholder lines based on parent partners

## Usage

This is a base module that should be installed before:
- compliance_cycle
- project_custom
- Any module requiring shareholder management

## Dependencies

- base
- contacts
- project
- partner_organization
- base_document_types

## Installation Order

Install at Level 0 after `partner_organization` and `base_document_types`.

## Version

18.0.1.0.0

## License

LGPL-3
