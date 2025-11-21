# Base Document Types

## Overview

This module provides the core document type management functionality for the Freezoner platform. It serves as a base module to break circular dependencies between Level 3 modules.

## Features

- **Partner Document Types**: Define and manage document types that can be associated with partners
- **Document Categories**: Organize document types into logical categories
- **Task Document Required Lines**: Manage mandatory documents for project tasks

## Models

### res.partner.document.type
Core model for defining document types with:
- Name and code
- Category association
- Active flag for archiving
- Description field

### res.partner.document.category
Categories for organizing document types with:
- Name and description
- Active flag
- Related document types

### task.document.required.lines
Task document requirements with:
- Document type association
- Project and task links
- Expiration and verification tracking
- Attachment management

## Usage

This is a base module that should be installed before:
- client_documents
- crm_log
- freezoner_custom
- compliance_cycle
- project_custom

## Dependencies

- base
- contacts
- documents
- project

## Installation Order

Install at Level 0 before any modules that depend on document type functionality.

## Version

18.0.1.0.0

## License

LGPL-3
