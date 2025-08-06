# IFileContentStorage interface | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 91 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/ifilecontentstorage

## Description

Terrasoft.File.Abstractions namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File.Abstractions` namespace.

The `Terrasoft.File.Abstractions.IFileContentStorage` interface provides the
essential methods for file storage management.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full description of the `IFileContentStorage` interface.

## Methods​

    Task<Stream> ReadAsync(IFileContentReadContext context)

Reads the file content.

    Task WriteAsync(IFileContentWriteContext context)

Writes the file content.

    Task DeleteAsync(IFileContentDeleteContext context)

Deletes the file content.

    Task CopyAsync(IFileContentCopyMoveContext context)

Copies the file content.

    Task MoveAsync(IFileContentCopyMoveContext context)

Moves the file content.

- Methods
