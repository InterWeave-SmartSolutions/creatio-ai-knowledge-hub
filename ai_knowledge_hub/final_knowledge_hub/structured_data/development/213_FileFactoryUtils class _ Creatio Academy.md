# FileFactoryUtils class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 293 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/filefactoryutils

## Description

Terrasoft.File namespace.

## Key Concepts

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File` namespace.

The `Terrasoft.File.FileFactoryUtils` class provides extension methods for the
`UserConnection` class and factory class that implements the
`Terrasoft.File.AbstractionsIFileFactory` interface. This way, the class
provides access to the factory for creating new or getting existing files.
Therefore, an instance of `UserConnection` or `SystemUserConnection` is required
for file management.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full list of the methods, properties, base classes, and
implemented interfaces of the `FileFactoryUtils` class.

## Methods​

    static IFileFactory GetFileFactory(this UserConnection source)

An extension method for the `UserConnection` class that returns an instance of
the class that implements the `IFileFactory` interface.

    static IFile GetFile(this UserConnection source, IFileLocator fileLocator)

An extension method for the `UserConnection` class that returns an instance of
the class that implements the `IFile` interface from a given `fileLocator`.

    static IFile CreateFile(this UserConnection source, IFileLocator fileLocator)

An extension method for the `UserConnection` class that creates an instance of
the class that implements the `IFile` interface from a given `fileLocator`.

    static IFile Get(this IFileFactory source, IFileLocator fileLocator)

An extension method for the class that implements the `IFileFactory` interface.
Returns an instance of the class that implements the `IFile` interface for a
given `fileLocator`.

    static IFile Create(this IFileFactory source, IFileLocator fileLocator)

An extension method for the class that implements the `IFileFactory` interface.
Creates an instance of the class that implements the `IFile` interface for a
given `fileLocator`.

    static IFileFactory WithRightsDisabled(this IFileFactory source)

An extension method for the class that implements the `IFileFactory` interface.
Returns an instance of the class that implements the `IFileFactory` interface
configured without the access permissions of the user.

- Methods
