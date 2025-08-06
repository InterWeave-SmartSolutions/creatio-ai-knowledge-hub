# IFile interface | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 255 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/ifile

## Description

Terrasoft.File.Abstractions namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File.Abstractions` namespace.

The `Terrasoft.File.Abstractions.IFile` interface provides essential file
management methods applicable in any file storage. The methods of this interface
are used for asynchronous file management. Synchronous file management methods
are available in the `Terrasoft.File.Abstractions.FileUtils` derived class.

note

Use the
[.NET classes reference](https://academy.creatio.com/documents?ver=8.3&id=15293)
to access the full description of the `IFile` interface.

## Properties​

    FileLocator IFileLocator

The file locator connected to the current instance of the class that implements
the `IFile` interface.

    Name string

File name.

    Length long

The size of the current file in bytes.

    CreatedOn DateTime

Date and time the file was created.

    ModifiedOn DateTime

Date and time the file was modified.

    Exists bool

Checks if the current file exists.

## Methods​

    Task CopyAsync(IFile target)

Copies the current file to the new `target` asynchronously.

    Task MoveAsync(IFile target)

Moves the current file to the new `target` asynchronously.

    Task DeleteAsync()

Deletes the current file asynchrously.

    Task WriteAsync(Stream stream, FileWriteOptions writeOptions)

Writes the contents of the current file to the `stream` asynchronously.

    Task<Stream> ReadAsync()

Reads the contents of the current file asynchronously.

    Task SaveAsync()

Saves the metadata of the current file asynchronously.

    void SetAttribute<TValue>(string name, TValue value)

Sets `value` of the `name` attribute for the current file.

    TValue GetAttribute<TValue>(string name, TValue defaultValue)

Returns the attribute value or the default value for the current file.

- Properties
- Methods
