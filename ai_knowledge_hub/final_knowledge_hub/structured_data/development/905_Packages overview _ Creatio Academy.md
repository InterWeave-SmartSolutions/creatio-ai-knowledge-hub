# Packages overview | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 678 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/development-tools/packages/packages-overview

## Description

A Creatio package is a collection of configuration elements that implement
certain functionality. On the file system level, a package is a directory that
defines a set of subdirectories and files. Any Creatio product is a set of
packages.

## Key Concepts

business process, configuration, sql, operation, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/packages-overview)**
(8.3).

Version: 8.2

On this page

Level: beginner

A **Creatio package** is a collection of configuration elements that implement
certain functionality. On the file system level, a package is a directory that
defines a set of subdirectories and files. Any Creatio product is a set of
packages.

## Package types​

Creatio includes the following package types:

- Simple package. Learn more:
  [Simple package](https://academy.creatio.com/documents?ver=8.2&id=15072).
- Project package. Learn more:
  [Project package](https://academy.creatio.com/documents?ver=8.2&id=15124).
- Assembly package. Learn more:
  [Assembly package](https://academy.creatio.com/documents?ver=8.2&id=15125).

View comparison of package types in the table below.

Feature| Package type| Simple package and smart activation simple package|
Project package| Assembly package and smart activation assembly package| Links
to other packages| +| –| +| Configuration elements| +| –| +  
(with restrictions)| File content| +| +| +| Development in Creatio IDE| +| –  
(use an external IDE)| +| Code compilation path for .NET Framework|
..\Terrasoft.WebApp\ Terrasoft.Configuration\ Terrasoft.Configuration.dll|
..\Terrasoft.WebApp\ Terrasoft.Configuration\ Pkg\ SomePackageName\ Files\ Bin\
SomePackageName.dll| ..\Terrasoft.WebApp\ Terrasoft.Configuration\ Pkg\
SomePackageName\ Files\ Bin\ SomePackageName.dll| Code compilation path for
.NET| ..\Terrasoft.Configuration\ Pkg\ SomePackageName\ Files\ Bin\ netstandard\
SomePackageName.dll| ..\Terrasoft.Configuration\ Pkg\ SomePackageName\ Files\
Bin\ netstandard\ SomePackageName.dll  
---|---|---

## Package structure​

If you upload the package to the version control system, Creatio creates the
directory that matches the package name in the package repository.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PackageStructureAndContent/7.17/storage_copy_structure.png)

View the structure elements of the package directory in the table below.

| Structure element | Structure element description | `branches` directory | Stores the versions of the current package. Each version is a subdirectory whose name matches the package version number in Creatio. For example, 7.18.0. | `Schemas` directory | Stores the package schemas. | `Assemblies` directory | Stores third-party builds bound to the package. | `Data` directory | Stores data bound to the package. | `SqlScripts` directory | Stores SQL scripts bound to the package. | `Resources` directory | Stores the localized package resources. | `Files` directory | Stores the package file content. Available in the file system. | `tags` directory | Stores tags. The tags in the version control system are a snapshot of the project, i. e., a static copy of files made to preserve a development stage. | `descriptor.json` file | Stores the package properties in JSON. The package properties includes the ID, title, version, dependencies, etc. |
| ----------------- | ----------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------------------------- | ---------------------- | ----------------------------------------------- | ---------------- | --------------------------------- | ---------------------- | ---------------------------------------- | --------------------- | --------------------------------------- | ----------------- | -------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------------------- |

## Package dependencies and hierarchy​

Creatio app development follows the basic principles of software design,
including the **"don't repeat yourself" (DRY) principle**. Creatio implements
this principle using **package dependencies**. Each package contains certain
Creatio functionality, which the other packages should not duplicate. If a
package requires functionality from a different package, set up dependencies
between the corresponding packages. Learn more:
[Set up the package dependencies](https://academy.creatio.com/documents?ver=8.2&id=15122&anchor=title-15122-2).

Packages can have multiple dependencies. For example, package `C` depends on
packages `A` and `D`. Thus, the functionality of packages `A` and `D` is
available in package `C`.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots.en/PackageDependencies/7.17/hierarchy.png)

Package dependencies form **hierarchical chains**. This means that the package
contains the functionality of the inheritor package and the functionality of all
packages that depend on the inheritor. The closest analogy to the package
hierarchy is the class inheritance hierarchy in object-oriented programming. For
example, package `E` contains not only functionality of package `C` on which it
depends, but also the functionality of packages `A`, `B`, and `D`. In addition,
package `F` contains the functionality of packages `B` and `D`.

Creatio adds dependencies of user-made packages based on the package hierarchy.
This lets you add fewer dependencies manually. For example, if a business
process uses configuration elements of the `CrtBase`, `CrtUIv2`, and
`Completeness` packages, only the `Completeness` package is added as a
dependency of the current package, since it depends on the `CrtUIv2` package,
which, in turn, depends on the `CrtBase` package.

Creatio lets you use smart activation packages. The package is installed into
the environment and activated automatically when all its dependencies are
available. Smart activation packages do not block deleting the linked
packages/apps. Learn more:
[Smart activation package](https://academy.creatio.com/documents?ver=8.2&id=15071).

---

## See also​

[Simple package](https://academy.creatio.com/documents?ver=8.2&id=15072)

[Project package](https://academy.creatio.com/documents?ver=8.2&id=15124)

[Assembly package](https://academy.creatio.com/documents?ver=8.2&id=15125)

[Automatically activated package](https://academy.creatio.com/documents?ver=8.2&id=15071)

[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.2&id=15101)

[Set up the package dependencies](https://academy.creatio.com/documents?ver=8.2&id=15122&anchor=title-15122-2)

- Package types
- Package structure
- Package dependencies and hierarchy
- See also
