# FileMetadata class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 172 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/filemetadata

## Description

Terrasoft.File.Abstractions.Metadata namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File.Abstractions.Metadata` namespace.

The `Terrasoft.File.Abstractions.Metadata.FileMetadata` abstract class provides
the properties of file metadata and methods for metadata management,

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full list of the methods, properties, base classes, and
implemented interfaces of the `FileMetadata` class.

## Properties​

    Name string

File name.

    Length long

The file size in bytes.

    CreatedOn DateTime

Date and time the file was created.

    ModifiedOn DateTime

Date and time the file was modified.

    FileContentStorageId Guid

The identifier of the file storage.

    StoringState FileStoringState

The state of the file ("New," "Modified," "Unmodified," "Deleted").

## Methods​

    abstract void SetAttribute<TValue>(string name, TValue value)

Set the additional `name` file attribute to the specified `value`.

    abstract TValue GetAttribute<TValue>(string name, TValue defaultValue)

Returns the specified value or the `defaultValue` of the additional `name`
attribute.

    void SetStoringState(FileStoringState newState)

Sets the file state to `FileStoringState.Modified` if the previous file state is
not `FileStoringState.New`.

- Properties
- Methods
