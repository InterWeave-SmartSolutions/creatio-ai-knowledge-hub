# FileUtils class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 221 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/references/fileutils

## Description

Terrasoft.File.Abstractions namespace.

## Key Concepts

## Use Cases

## Content

Version: 8.3

On this page

Level: intermediate

`Terrasoft.File.Abstractions` namespace.

The `Terrasoft.File.Abstractions.FileUtils` class provides extension methods for
file management.

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/index.html)
to access the full list of the methods, properties, base classes, and
implemented interfaces of the `FileUtils` class.

## Methods​

    static void SetAttributes(this IFile source, IReadOnlyDictionary<string, object> attributes)

Sets the file attributes to the values passed in the `attributes` collection.

    static void Save(this IFile source)

Saves the metadata of the file.

    static Stream Read(this IFile source)

Reads the content of the file.

    static void Write(this IFile source, Stream stream, FileWriteOptions writeOptions) static void Write(this IFile source, byte[] content)

Writes the content of the file.

Parameters

| source | The file whose contents is to be written | stream | The stream that provides the file content. | writeOptions | Parameters for writing the file. | content | The file content as an array of bytes. |
| ------ | ---------------------------------------- | ------ | ------------------------------------------ | ------------ | -------------------------------- | ------- | -------------------------------------- |

    static void Delete(this IFile source)

Deletes the specified file.

    static void Copy(this IFile source, IFile target)

Copies the existing `source` file to the new `target` file.

    static void Move(this IFile source, IFile target)

Moves the existing `source` file to the new `target` destination.

- Methods
