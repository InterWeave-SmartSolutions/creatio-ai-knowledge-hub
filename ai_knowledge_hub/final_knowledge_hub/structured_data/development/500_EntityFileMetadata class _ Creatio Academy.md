# EntityFileMetadata class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 156 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/entityfilemetadata

## Description

Terrasoft.File namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File` namespace.

The `Terrasoft.File.EntityFileMetadata` class implements the
Terrasoft.File.Abstractions.Metadata.FileMetadata abstract class. This class
describes the file metadata in the [Attachments] object and provide the methods
to manage them.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full list of the methods, properties, base classes, and
implemented interfaces of the `EntityFileMetadata` class.

## Constructors​

    EntityFileMetadata(EntityFileLocator fileLocator)

Creates an `EntityFileMetadata` instance for a given `fileLocator`.

## Properties​

    Attributes IReadOnlyDictionary<string, object>

Collection of attribute values.

    RecordId Guid

File ID.

    EntitySchemaName string

The name of the object that stores the file.

## Methods​

    override void SetAttribute<TValue>(string name, TValue value)

Set the additional `name` file attribute to the specified `value`.

    override TValue GetAttribute<TValue>(string name, TValue defaultValue)

Returns the specified value or the `defaultValue` of the additional `name`
attribute.

- Constructors
- Properties
- Methods
