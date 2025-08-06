# EntitySchemaQueryOptions class | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 165 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/data-operations-back-end/orm/references/entityschemaqueryoptions

## Description

The Terrasoft.Core.Entities namespace.

## Key Concepts

entity schema

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

The `Terrasoft.Core.Entities` namespace.

The `Terrasoft.Core.Entities.EntitySchemaQueryOptions` class configures entity
schema queries.

note

View the entire list of methods and properties of the `EntitySchemaQueryOptions`
class, its parent classes, as well as the interfaces it implements, in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Entities.EntitySchemaQueryOptions.html).

## Constructors​

    EntitySchemaQueryOptions

Initializes a class instance. By default, the `PageableRowCount` property is set
to 14 in the constructor.

## Properties​

    PageableRowCount int

The number of page records in the resulting dataset that the query returns.

    PageableDirection Terrasoft.Core.DB.PageableSelectDirection

The direction of paged output.

Available values (`Terrasoft.Core.DB.PageableSelectDirection`)

| Prior | Previous page. | First | First page. | Current | Current page. | Next | Next page. |
| ----- | -------------- | ----- | ----------- | ------- | ------------- | ---- | ---------- |

    PageableConditionValues Dictionary<string, object>

The values of the paged output conditions.

    HierarchicalMaxDepth int

The maximum nesting level of a hierarchical query.

    HierarchicalColumnName string

The name of the column by which to build a hierarchical query.

    HierarchicalColumnValue Guid

The hierarchical column's seed value from which to build the hierarchy.

- Constructors
- Properties
