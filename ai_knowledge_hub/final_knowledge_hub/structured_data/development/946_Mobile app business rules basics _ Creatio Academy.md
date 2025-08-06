# Mobile app business rules basics | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 142 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/mobile-development/mobile-basics/business-rules/overview

## Description

Business rules represent a Creatio mechanism that enables setting up the
behavior of record edit page fields. You can use business rules to, e.g., set up
visible or required fields, make fields enabled, etc.

## Key Concepts

mobile app, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.2

Level: advanced

**Business rules** represent a Creatio mechanism that enables setting up the
behavior of record edit page fields. You can use business rules to, e.g., set up
visible or required fields, make fields enabled, etc.

Important

Business rules work only on record edit and view pages.

Adding business rules to a page is performed via the
`Terrasoft.sdk.Model.addBusinessRule(name, config)` method, where

- `name` – is the name of the model, bound to the edit page, e.g., "Contact."
- `config` – is the object defining business rule properties. The list of
  properties depends on a specific business rule type.

In the mobile application you can add business rule that implements custom logic
(custom business rule). The `Terrasoft.RuleTypes.Custom` method is provided for
this type of business rules.
