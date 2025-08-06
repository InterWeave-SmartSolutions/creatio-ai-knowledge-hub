# Develop client code | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 797
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/external-ides/examples/develop-the-client-code

## Description

To improve the developer experience, Creatio lets you manage the files of client
module schemas in an external IDE, for example, WebStorm, Visual Studio Code,
Sublime Text, etc. To do this, download the schema source code from the
database. Creatio downloads the source code of client module schema as \.js
files and client module styles as \.less files. Since database access is
required to write client code, this instruction is relevant only for Creatio
on-site.

## Key Concepts

configuration, section, integration, database, operation, package, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/external-ides/examples/develop-the-client-code)**
(8.3).

Version: 8.1

On this page

Level: advanced

To improve the developer experience, Creatio lets you manage the files of
[client module schemas](https://academy.creatio.com/documents?ver=8.1&id=15106)
in an external IDE, for example, WebStorm, Visual Studio Code, Sublime Text,
etc. To do this, download the schema source code from the database. Creatio
downloads the source code of client module schema as _.js files and client
module styles as _.less files. Since database access is required to write client
code, this instruction is relevant only for Creatio on-site.

To **write the source code of client module schemas in the file system** :

1. Enable the file system development mode.
2. Set up the package in the SVN repository.
3. Create a client module schema in Creatio IDE.
4. Download the package to the file system.
5. Write the source code of the client module schema in an external IDE.
6. Debug the source code (optional).
7. Disable the file system development mode (optional).

## 1\. Enable the file system development mode​

To **enable the file system development mode** , follow the instruction in a
separate article:
[External IDEs](https://academy.creatio.com/documents?ver=8.1&id=15111&anchor=title-2098-4).

## 2\. Set up the package in the SVN repository​

To **set up the package in the SVN repository** , take one of the following
steps:

- **Create a package in the SVN repository**.

Creatio lets you create a package in the following **ways** :

    * Using SVN. To do this, follow the instruction in a separate article: [Create a user-made package using Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15122).
    * Without using SVN. To do this, follow the instruction in a separate article: [Create a package in the file system development mode](https://academy.creatio.com/documents?ver=8.1&id=15143).

- **Install a package from the SVN repository**. To do this, follow the
  instruction in a separate article:
  [Install an SVN package in the file system development mode](https://academy.creatio.com/documents?ver=8.1&id=15144).

- **Update a package from the SVN repository**. To do this, follow the
  instruction in a separate article:
  [Update and commit changes to the SVN from the file system](https://academy.creatio.com/documents?ver=8.1&id=15147).

The steps below use the `sdkPackageInFileSystem` package installed from the SVN
repository as an example.

note

When developing in the file system, it is more convenient to manage version
control system repositories using client applications, for example,
[Tortoise SVN](https://tortoisesvn.net/) or [Git](https://git-scm.com/), instead
of the out-of-the-box Creatio integration.

## 3\. Create a client module schema in Creatio IDE​

To **create a client module schema in Creatio IDE** , follow the instruction in
a separate article:
[Client module](https://academy.creatio.com/documents?ver=8.1&id=15106).

For example, create a schema of the `ContactPageV2` replacing view model and
schema of the `ContactPageV2CSS` view model in the `sdkPackageInFileSystem`
package.

## 4\. Download the package to the file system​

To **download the package that contains the client module schema to the file
system** , select **Download packages to the file system** in the **File system
development mode** action group on the toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatingPackageInFileSystem(7.17)/scr_download_to_fs.png>)

For example, after you download the `sdkPackageInFileSystem` to the file system,
the
`..Terrasoft.WebApp\Terrasoft.Configuration\Pkg\sdkPackageInFileSystem\Schemas`
subdirectories will contain the `ContactPageV2.js` (source code of the client
module schema) and `ContactPageV2CSS.less` (client module styles) files.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/UploadClientSchemas/8.0/scr_pkg_exporer.png)

## 5\. Write the source code of the client module schema in an external IDE​

For example, to hide the **Full job title** field from the contact page:

1. Open the `ContactPageV2.js` file in an external IDE and add the source code
   displayed below.

ContactPageV2.js

         define("ContactPageV2", [], function() {
             return {
                 entitySchemaName: "Contact",
                 diff: /**SCHEMA_DIFF*/ [{
                     "operation": "remove",
                     "name": "JobTitleProfile"
                 }] /**SCHEMA_DIFF*/
             };
         });



2. Save the `ContactPageV2.js` file.

As a result, Creatio will hide the **Full job title** field from the contact
page.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/UploadClientSchemas/8.0/scr_result.png)

Note that the changes will be displayed automatically.

## 6\. Debug the source code (optional)​

Debug the source code if it was written with errors. To do this, follow the
instruction in a separate article:
[Front-end debugging](https://academy.creatio.com/documents?ver=8.1&id=15193).

## 7\. Disable the file system development mode (optional)​

If you do not need to use the file system for further development, disable the
file system development mode.

To **disable the file system development mode** :

1. Select **Update packages from file system** in the **File system development
   mode** action group on the toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPkgFromSvnInFileSystemMode(7.17)/scr_updating.png>)

2. Set the `enabled` attribute of the `fileDesignMode` element in the
   `Web.config` file in Creatio root directory to `false`.

---

## Resources​

[Official Tortoise SVN website](https://tortoisesvn.net/)

[Official Git website](https://git-scm.com/)

[Module coupling](<https://en.wikipedia.org/w/index.php?title=Coupling_(computer_programming)&oldid=1086406506>)
(Wikipedia)

- 1\. Enable the file system development mode
- 2\. Set up the package in the SVN repository
- 3\. Create a client module schema in Creatio IDE
- 4\. Download the package to the file system
- 5\. Write the source code of the client module schema in an external IDE
- 6\. Debug the source code (optional)
- 7\. Disable the file system development mode (optional)
- Resources
