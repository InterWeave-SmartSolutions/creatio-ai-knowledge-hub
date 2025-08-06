# Project package | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 425 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/development-tools/packages/project-package

## Description

A project package is a package that lets you develop Creatio functionality as a
standard C# project.

## Key Concepts

configuration, integration, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/project-package)**
(8.3).

Version: 8.2

On this page

Level: intermediate

A **project package** is a package that lets you develop Creatio functionality
as a standard C# project.

## Project package major features​

- Project packages take much faster to compile than simple packages if both
  contain a large number of **Source code** type schemas: 1-2 seconds as opposed
  to 30-120 seconds.
- Project packages let you deploy functionality to a
  [production environment](https://academy.creatio.com/documents?ver=8.2&id=15201&anchor=title-2124-3)
  indirectly.
- Project packages streamline C# development for Creatio in the cloud.
- Project packages let you track the implementation dependencies. Use this to
  create a list of classes to test after functionality updates.
- Project packages streamline the automatic functionality tests.

## Project package structure​

The project package structure in the file system is identical to the structure
of a simple package. The main **difference** between the project package and a
simple package is in the `Package.sln` and `Package.csproj` files unique to the
project package. Learn more about the simple package structure:
[Packages basics](https://academy.creatio.com/documents?ver=8.2&id=15121&anchor=title-2105-2).

View the structure of project package directories in the figure below. Include
the functionality developed in the project package in the
[package file content](https://academy.creatio.com/documents?ver=8.2&id=15126)
(the `Files` directory) as the compiled library and \*.cs files.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PackageProject/7.18/scr_package_project_folders.png)

## Project package development tools​

1. [Creatio command-line interface utility (clio)](https://github.com/Advance-Technologies-Foundation/clio)
   is an open source utility for integration, development, and CI/CD.

**Use the utility** :

     * to create a project package
     * to import the package into Creatio on-site or in the cloud
     * to export the package from Creatio on-site or in the cloud
     * to restart Creatio
     * to convert existing packages

2. [CreatioSDK](https://www.nuget.org/packages/CreatioSDK) is a NuGet package
   that provides a set of development tools. Use the NuGet package to create an
   application on the Creatio platform.

## Import a project package​

1. Compile the project package.

Compile the project package into a library as an individual C# project. The
library name must match the package name. Place the compiled files to the
`../Files/Bin/[PackageName].dll` directory.

2. Transfer the library.

3. Copy the library to the directory.

4. Run Creatio.

As a result, Creatio will check for qualifying libraries in the packages upon
start or restart. If such libraries exist, Creatio will connect them
immediately. You do not have to compile the configuration to deploy the
functionality.

View the package import procedure in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PackageProject/7.18/scr_package_project_compile.png)

---

## See also​

[Environment overview](https://academy.creatio.com/documents?ver=8.2&id=15201)

[Packages basics](https://academy.creatio.com/documents?ver=8.2&id=15121)

[Packages file content](https://academy.creatio.com/documents?ver=8.2&id=15126)

---

## Resources​

[Creatio command-line interface utility (clio)](https://github.com/Advance-Technologies-Foundation/clio)

[CreatioSDK NuGet package](https://www.nuget.org/packages/CreatioSDK)

- Project package major features
- Project package structure
- Project package development tools
- Import a project package
- See also
- Resources
