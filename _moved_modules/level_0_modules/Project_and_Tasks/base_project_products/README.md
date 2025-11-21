# Base Project Products

## Overview

This module provides the core project-product relationship management functionality for the Freezoner platform. It serves as a base module to break circular dependencies between Level 3 modules.

## Features

- **Project Product Association**: Link products to projects with tracking
- **Product Remarks**: Track remarks and notes for project-product combinations
- **Partner Integration**: Automatic partner association from projects
- **Activity Tracking**: Full mail thread and activity support

## Models

### project.project.products
Core model for project-product associations with:
- Project and product references
- Partner (customer) link
- Remarks tracking
- Active flag for archiving
- Computed display name

### project.project.products.remarks
Remarks for project products with:
- Remark text and description
- User and date tracking
- Multiple project-product associations
- Active flag

## Partner Extension

Extends `res.partner` with:
- `project_product_ids`: One2many field for project products

## Usage

This is a base module that should be installed before:
- freezoner_custom
- compliance_cycle
- project_custom

## Dependencies

- base
- project
- product
- mail

## Installation Order

Install at Level 0 before any modules that manage project-product relationships.

## Version

18.0.1.0.0

## License

LGPL-3
