# IFileFactory interface | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 127 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/ifilefactory

## Description

Terrasoft.File.Abstractions namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File.Abstractions` namespace.

The `Terrasoft.File.Abstractions.IFileFactory` interface provides a set of
methods to get or create an instance of the class that implements the
`Terrasoft.File.Abstractions.IFile` interface.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full description of the `IFileFactory` interface.

## Properties​

    UseRights bool

Determines if the permissions of the user are considered when creating a file.

## Methods​

    IFile Get(IFileLocator fileLocator, FileOptions options)

Returns an instance of the class that implements the `IFile` interface with the
specified `options` parameters from a given `fileLocator`.

    IFile Create(IFileLocator fileLocator, FileOptions options)

Creates an instance of the class that implements the IFile interface with the
specified `options` parameters for a given `fileLocator`.

- Properties
- Methods
