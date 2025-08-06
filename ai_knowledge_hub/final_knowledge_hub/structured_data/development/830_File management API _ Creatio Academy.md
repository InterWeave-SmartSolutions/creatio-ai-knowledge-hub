# File management API | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 2225
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/back-end-development/api-for-file-management/overview

## Description

View a list of namespaces for file management API in the table below.

## Key Concepts

configuration, lookup, database, operation, contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/api-for-file-management/overview)**
(8.3).

Version: 8.0

On this page

Level: intermediate

View a list of namespaces for file management API in the table below.

| Namespace | Description | Terrasoft.File.Abstractions | Determines the file management logic in Creatio. | Terrasoft.File | Implements the abstractions used in Creatio. |
| --------- | ----------- | --------------------------- | ------------------------------------------------ | -------------- | -------------------------------------------- |

## File locators​

A **file locator** determines the file location and implements the
`Terrasoft.File.Abstractions.IFileLocator` interface. A file locator must
contain a unique file identifier: `RecordId`.

Creatio lets you create different file locators for different file storages.
Depending on the file storage, the file locator might have extra properties to
identify the file location. For example, the `Terrasoft.File.EntityFileLocator`
class implements the file locator for the current file storage. View the
properties of the `EntityFileLocator` object in the table below.

| Property | Description | RecordId | Includes a unique file identifier. | EntitySchemaName | Includes the name of the object schema where the file is stored. For example, "ActivityFile," "CaseFile." |
| -------- | ----------- | -------- | ---------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------- |

## File structure​

**File** in Creatio implements the `Terrasoft.File.Abstractions.IFile` interface
whose methods let you manage files asynchronously, regardless of the file
storage type. The `Terrasoft.File.Abstractions.FileUtils` class implements
methods to manage files synchronously.

View the file structure supported by Creatio in the table below.

| Structure element | Description | Storage | Metadata | File metadata includes file properties, such as file name, file size in bytes, file creation date. File metadata is based on the `Terrasoft.File.Abstractions.Metadata.FileMetadata` abstract class. For example, the `Terrasoft.File.Metadata.EntityFileMetadata` class implements the file metadata for files uploaded to the file storage. | The storage that implements the `Terrasoft.File.Abstractions.Metadata.IFileMetadataStorage` interface. | Content | File content. | The storage that implements the `Terrasoft.File.Abstractions.Metadata.IFileContentStorage` interface. |
| ----------------- | ----------- | ------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------- | ------------- | ----------------------------------------------------------------------------------------------------- |

The implementations of the
`Terrasoft.File.Abstractions.Metadata.IFileMetadataStorage` and
`Terrasoft.File.Abstractions.Metadata.IFileContentStorage` interfaces include
specific features to interact with different file storages, such as server's
file system, S3 file storage, Azure Blob file storage, Google Drive, etc.

## Operations with files​

### Access an existing file and create a new file​

The `Terrasoft.File.Abstractions.IFileFactory` interface implements methods to
create and retrieve objects of a class that implements the
`Terrasoft.File.Abstractions.IFile` interface. To access the
`Terrasoft.File.Abstractions.IFileFactory` interface, use the methods of the
`Terrasoft.File.File.FileFactoryUtils` class that extends the `UserConnection`
class. Therefore, file management requires an instance of the `UserConnection`
or `SystemUserConnection` class.

Since the file locator determines the file location, specify the `RecordId` file
identifier to **access an existing file**.

View the examples that access existing files below.

- Access the existing file (option 1)
- Access the existing file (option 2)

  /_ Retrieve the instance of the file factory. _/  
  IFileFactory fileFactory = UserConnection.GetFileFactory();

  /_ Create the "EntityFileLocator" instance identified by "recordId" and stored
  in the "ActivityFile" database table. _/  
  var fileLocator = new EntityFileLocator("ActivityFile", recordId);

  /_ Pass the created locator to the factory method. _/  
  IFile file = fileFactory.Get(fileLocator);

  /_ Implement the business logic that works with the file and its contents
  using instance of a class that implements the "IFile" interface. _/  
  ...;

  /_ Create the "EntityFileLocator" instance identified by "recordId" and stored
  in the "ActivityFile" database table. _/  
  var fileLocator = new EntityFileLocator("ActivityFile", recordId);

  /_ Pass the created locator to the method of the "UserConnection" class. _/  
  IFile file = UserConnection.GetFile(fileLocator);

  /_ Implement the business logic that works with the file and its contents
  using instance of a class that implements the "IFile" interface. _/  
  ...;

To **create a new file** :

1. **Create a** `RecordId` **file identifier**.
2. **Specify the file identifier** in the method that creates the file locator.

View the examples that create new files below.

- Create a new file (option 1)
- Create a new file (option 2)

  /_ Retrieve the instance of the file factory. _/  
  IFileFactory fileFactory = UserConnection.GetFileFactory();

  /_ Create a unique ID for the new file. _/  
  Guid recordId = Guid.NewGuid();

  /_ Create the "EntityFileLocator" instance identified by "recordId" and stored
  in the "ActivityFile" database table. _/  
  var fileLocator = new EntityFileLocator("ActivityFile", recordId);

  /_ Pass the created locator to the factory method. _/  
  IFile file = fileFactory.Create(fileLocator);

  /_ Implement the business logic that works with the file and its contents
  using instance of a class that implements the "IFile" interface. _/  
  ...;

  /_ Create a unique ID for the new file. _/  
  Guid recordId = Guid.NewGuid();

  /_ Create the "EntityFileLocator" instance identified by "recordId" and stored
  in the "ActivityFile" database table. _/  
  var fileLocator = new EntityFileLocator("ActivityFile", recordId);

  /_ Pass the created locator to the method of the "UserConnection" class. _/  
  IFile file = UserConnection.CreateFile(fileLocator);

  /_ Implement the business logic that works with the file and its contents
  using instance of a class that implements the "IFile" interface. _/  
  ...;

View the examples that execute CRUD operations with the files below.

Create a new file bound to a single activity

    /* Create a unique ID for the new file. */
    Guid recordId = Guid.NewGuid();

    /* Create the "EntityFileLocator" instance identified by "recordId" and stored in the "ActivityFile" database table. */
    var fileLocator= new EntityFileLocator("ActivityFile", recordId);

    /* Pass the created locator to the method of the "UserConnection" class. */
    IFile file = UserConnection.CreateFile(fileLocator);

    /* Specify the file name to determine the file in the file storage. */
    file.Name = "Some name of a new";

    /* Bind the file to a single activity using "activityId." */
    file.SetAttribute("ActivityId", activityId);

    /* Save the file metadata before saving the file content. */
    file.Save();

    /* Specify the file content. */
    var content = new byte[] {0x12, 0x34, 0x56};

    using (var stream = new MemoryStream(content)) {

        /* Save the file content to the database. Specify "FileWriteOptions.SinglePart" to save the content without breaking it into multiple parts. */
        file.Write(stream, FileWriteOptions.SinglePart);
    }

Retrieve the file content

    /* The file content. */
    var content = new byte[]();

    /* Create a unique ID for the new file. */
    Guid recordId = Guid.NewGuid();

    /* Create the "EntityFileLocator" instance identified by "recordId" and stored in the "ActivityFile" database table. */
    var fileLocator = new EntityFileLocator("ActivityFile", recordId);

    /* Pass the created locator to the method of the "UserConnection" class. */
    IFile file = UserConnection.GetFile(fileLocator);

    using (Stream stream = file.Read()) {

        /* Retrieve the file content and save it to the array. */
        content = stream.ReadToEnd();
    }

Copy a file from the original file storage, paste the file to a new file
storage, and delete the file from the original file storage

    /* The file content. */
    var content = new byte[]();

    /* Create the "EntityFileLocator" instance identified by "recordId" and stored in the "ActivityFile" database table. */
    var fileLocator = new EntityFileLocator("ActivityFile", recordId);

    /* Pass the created locator to the method of the "UserConnection" class. */
    IFile file = UserConnection.GetFile(fileLocator);

    /* Retrieve the file content and save it to the array. */
    using (Stream stream = file.Read()) {
        content = stream.ReadToEnd();
    }

    /* Create a unique ID to copy the current file. */
    Guid copyFileId = Guid.NewGuid();

    /* Create the "EntityFileLocator" instance identified by "copyFileId" and stored in the "ActivityFile" database table. */
    var copyFileLocator = new EntityFileLocator("ActivityFile", copyFileId);

    /* Pass the created locator to the method of the "UserConnection" class. */
    IFile copyFile = UserConnection.CreateFile(copyFileLocator);

    /* Specify the file name to determine the file in a new file storage. */
    copyFile.Name = file.Name + " - Copy";

    /* Save the file metadata before saving the file content. */
    copyFile.Save();

    /* Copy the file content from the original file using one of the options.
    Option 1. Specify "FileWriteOptions.SinglePart" to save the content without breaking it into multiple parts. */
    copyFile.Write(new MemoryStream(content), FileWriteOptions.SinglePart);

    /* Option 2. */
    file.Copy(copyFile); */
     
    /* Create a unique ID to paste the copied file. */
    Guid moveFileId = Guid.NewGuid();

    /* Create the "EntityFileLocator" instance identified by "moveFileId" and stored in the "ContactFile" database table. */
    var moveFileLocator = new EntityFileLocator("ContactFile", moveFileId);

    /* Pass the created locator to the method of the "UserConnection" class. */
    IFile moveFile = UserConnection.CreateFile(moveFileLocator);

    /* Save the file metadata before saving the file content. */
    moveFile.Save();
     
    /* Paste the copied file to a new file storage. */
    file.Move(moveFile);
     
    /* Delete the file from original file storage. */
    file.Delete();

### Implement a custom file storage​

Implement custom file storage if the current file metadata storage is
insufficient for your business goals. To do this:

1. **Implement the** `Terrasoft.File.Abstractions.Content.IFileContentStorage`
   **interface** that describes the API required for working with the file
   storage.
2. **Implement a custom metadata storage** that implements the
   `Terrasoft.File.Abstractions.Metadata.IFileMetadataStorage` interface.
3. **Inherit the metadata class** from the
   `Terrasoft.File.Abstractions.Metadata.FileMetadata` class.
4. **Implement a custom file locator** that implements the
   `Terrasoft.File.Abstractions.IFileLocator` interface.
5. **Register a custom metadata storage** in the **SysFileMetadataStorage**
   lookup.
6. **Register a custom content storage** in the **SysFileContentStorage**
   lookup.

View the example that creates file content storage in the file system below.

FsFileBlobStorage

    namespace Terrasoft.Configuration {
        using System.IO;
        using System.Threading.Tasks;
        using Terrasoft.File.Abstractions;
        using Terrasoft.File.Abstractions.Content;
        using Terrasoft.File.Abstractions.Metadata;
        using Terrasoft.File.Metadata;

        /* Class that implements the "IFileContentStorage" interface. */
        public class FsFileBlobStorage: IFileContentStorage {

            /* A root path to the storage. */
            private const string BaseFsPath = "C:\\FsStore\\";

            private static string GetPath(FileMetadata fileMetadata) {
                var md = (EntityFileMetadata)fileMetadata;
                string key = $"{md.EntitySchemaName}\\{md.RecordId}_{fileMetadata.Name}";
                return Path.Combine(BaseFsPath, key);
            }

            public Task<Stream> ReadAsync(IFileContentReadContext context) {
                string filePath = GetPath(context.FileMetadata);
                Stream stream = System.IO.File.OpenRead(filePath);
                return Task.FromResult(stream);
            }

            public async Task WriteAsync(IFileContentWriteContext context) {
                string filePath = GetPath(context.FileMetadata);
                FileMode flags = context.WriteOptions != FileWriteOptions.SinglePart
                    ? FileMode.Append
                    : FileMode.OpenOrCreate;
                string dirPath = Path.GetDirectoryName(filePath);
                if (!Directory.Exists(dirPath)) {
                    Directory.CreateDirectory(dirPath);
                }
                using (var fileStream = System.IO.File.Open(filePath, flags)) {
                    context.Stream.CopyToAsync(fileStream);
                }
            }

            public Task DeleteAsync(IFileContentDeleteContext context) {
                string filePath = GetPath(context.FileMetadata);
                System.IO.File.Delete(filePath);
                return Task.CompletedTask;
            }

            public Task CopyAsync(IFileContentCopyMoveContext context) {
                string sourceFilePath = GetPath(context.SourceMetadata);
                string targetFilePath = GetPath(context.TargetMetadata);
                System.IO.File.Copy(sourceFilePath, targetFilePath);
                return Task.CompletedTask;
            }

            public Task MoveAsync(IFileContentCopyMoveContext context) {
                string sourceFilePath = GetPath(context.SourceMetadata);
                string targetFilePath = GetPath(context.TargetMetadata);
                System.IO.File.Move(sourceFilePath, targetFilePath);
                return Task.CompletedTask;
            }
        }
    }

## File management exceptions​

| Exception type | Message | Exception conditions | Terrasoft.File.Abstractions.FileNotFoundByLocatorException | File not found by locator `{locator_type}{locator.ToString}` | When accessing any properties or methods of the `IFile` interface if file metadata is not found. | System.InvalidOperationException | Can't delete new file: `{locator_type}{locator.ToString}` | When deleting a newly created file. I. e., `FileMetadata.StoringState == FileStoringState.New` | Terrasoft.Common.NullOrEmptyException | File name cannot be null or empty | When saving a file that has the `Name` field value omitted. | System.InvalidOperationException | Can't find a metadata storage for the `{locator_type}` locator type | If a file metadata storage corresponding to the locator type is not found. | System.InvalidOperationException | Can't find a content storage for the `{metadata_type}` metadata type | If a file content storage corresponding to the file metadata storage is not found. | Content storage `{content_storage_name}` with Id `{content_storage_is}` is not active | If a selected content storage is disabled. |
| -------------- | ------- | -------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------- | ----------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------ |

- File locators
- File structure
- Operations with files
  - Access an existing file and create a new file
  - Implement a custom file storage
- File management exceptions
