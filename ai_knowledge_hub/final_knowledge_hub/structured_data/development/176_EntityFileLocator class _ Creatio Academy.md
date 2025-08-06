# EntityFileLocator class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 103 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/entityfilelocator

## Description

Terrasoft.File namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File` namespace.

The class implements the `IFileLocator` interface for the current Creatio file
storage.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full list of the methods, properties, base classes, and
implemented interfaces of the `EntityFileLocator` class.

## Constructors​

    EntityFileLocator()

Creates a new `EntityFileLocator` instance.

    EntityFileLocator(string entitySchemaName, Guid recordId)

Creates a new `EntityFileLocator` instance for the specified `recordId` file
bound to the `entitySchemaName` object schema.

## Properties​

    EntitySchemaName string

Metadata – the name of the object that stores the file.

    RecordId Guid

Metadata – the file ID

- Constructors
- Properties
