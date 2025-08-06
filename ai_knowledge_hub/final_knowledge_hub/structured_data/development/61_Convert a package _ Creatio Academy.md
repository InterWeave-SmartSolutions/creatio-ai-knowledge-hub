# Convert a package | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 909 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/development-tools/packages/package-conversion

## Description

Creatio supports the following conversion types:

## Key Concepts

configuration, section, database, operation, package, notification

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/package-conversion)**
(8.3).

Version: 8.2

On this page

Level: intermediate

Creatio supports the following **conversion types** :

- Simple package to assembly package
- Assembly package to simple package
- Project package to assembly package
- Assembly package to project package

Since the package conversion requires database access, it is available for
**Creatio on-site**. **Creatio in the cloud** lets you move individual
configuration elements to an assembly package.

## Convert a simple package to an assembly package​

1. Select **Properties** in the package menu.

2. Select the **Compile into a separate assembly** checkbox.

3. Click **Apply**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PackageAssembly/8.0/convert_simple_package.gif)

**Actions** that saving the package runs:

     * Change the package type in the database (`[Type]` column value). If the **Compile into a separate assembly** checkbox is selected, the value changes from "0" (simple package) to "1" (assembly package). If the **Compile into a separate assembly** checkbox is clear, the value changes from "1" (simple package) to "0" (assembly package).
     * Change the path to the assembly package project in the database (`[ProjectPath]` column value). By default, `Files/PackageName.csproj`, where `PackageName` is the name of the assembly package. For simple packages, the column contains an empty value. If the `[ProjectPath]` column contains an empty value for the assembly package (i. e., the `[Type]` column is set to "1"), this causes application failure.
     * Delete assembly package files if the **Compile into a separate assembly** checkbox is clear.
     * Generate all required schemas.

4. Compile the configuration if needed. The notification about a required
   compilation will be available in the information window.

Important

Without the compilation of a configuration when needed, a conversion of a simple
package to an assembly package is considered incomplete.

5. Make sure the converted package meets the
   [Requirements for an assembly package](https://academy.creatio.com/documents?ver=8.2&id=15125&anchor=title-3554-2).

As a result, Creatio will convert the simple package to an assembly package.

## Convert an assembly package to simple package​

1. Open the menu of the assembly package to convert to a simple package →
   **Properties** → clear the **Compile into a separate assembly** checkbox.

Click **Apply**.

2. Rebuild the project libraries for an assembly package that was previously
   converted from a project package. The libraries are removed as a byproduct of
   the conversion.

As a result, Creatio will convert the assembly package to a simple package.

## Convert a project package to an assembly package​

Creatio lets you convert a project package to an assembly package.

To **convert a project package to an assembly package** :

1. Delete all files in the `Files\Bin` and `Files\Bin\netstandard` directories.

2. Add the `<AssemblyName>` property to the C# project of the project package or
   change the property value. The name of the project package must not match the
   name of the assembly package.

Property template <AssemblyName>

         <AssemblyName>PackageProjectAssemblyName</AssemblyName>



`PackageProjectAssemblyName` is the name of the project package assembly.

3. Compile the C# project of the project package.

4. Create a `bootstrapAssemblies.json` file in the `Files` directory. Use the
   file structure below.

bootstrapAssemblies.json file structure template

         {
             "assemblies": [
                 "PackageProjectAssemblyName.dll"
             ]
         }



`PackageProjectAssemblyName` is the name of the project package assembly.

5. Open the menu of the project package to convert to an assembly package →
   **Properties** → select the **Compile into a separate assembly** checkbox.

Click **Apply**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PackageAssembly/8.0/convert_simple_package.gif)

6. Compile the assembly package. This step depends on the status of
   [development mode in the file system](https://academy.creatio.com/documents?ver=8.2&id=15111&anchor=title-1193-1).

With **development mode enabled in the file system**.

     1. Export the assembly package to the file system. To do this, click **Download packages to the file system** in the **File system development mode** group of the **Actions** drop-down list on the **Configuration** section toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ConvertPackages/8.0/scr_Download_packages_to_file_system.png)

     2. Exempt the project package from compilation in the `PackageName.csproj` file of the assembly package.

Template for adding the exemption

            <Compile Remove="$(RelativeCurrentPkgFolderPath)Files/PackageProjectFolder/**" />


`PackageProjectFolder` is the directory name of the project package.

     3. Compile the assembly package. To do this, click **Compile** in the assembly package menu.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ConvertPackages/8.0/scr_Compile.png)

With **development mode disabled in the file system**.

     1. Compile the assembly package. To do this, click **Compile** in the assembly package menu.

Compilation fails.

     2. Exempt the project package from compilation in the `PackageName.csproj` file of the assembly package.

Template for adding the exemption

            <Compile Remove="$(RelativeCurrentPkgFolderPath)Files/PackageProjectFolder/**" />


`PackageProjectFolder` is the directory name of the project package.

     3. Recompile the assembly package. To do this, click **Compile** in the assembly package menu.

7. Make sure the converted package meets the
   [Requirements for an assembly package](https://academy.creatio.com/documents?ver=8.2&id=15125&anchor=title-3554-2).

As a result, Creatio will convert the project package to an assembly package.

## Convert an assembly package to a project package​

Creatio lets you convert an assembly package to a project package.

note

Creatio lets you convert an assembly package previously converted from a project
package. A previously unconverted assembly package cannot be converted.

To **convert an assembly package to a project package** :

1. Open the menu of the assembly package to convert to a project package, select
   **Properties** and clear the **Compile into a separate assembly** checkbox.

Click **Apply**.

2. Compile the project package.

3. Compile the configuration. Learn more about compilation:
   [Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.2&id=15101&anchor=title-2093-8).

As a result, Creatio will convert the assembly package to a project package.

---

## See also​

[Creatio IDE](https://academy.creatio.com/documents?ver=8.2&id=15101)

[External IDEs](https://academy.creatio.com/documents?ver=8.2&id=15111)

[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.2&id=15101)

[Assembly package](https://academy.creatio.com/documents?ver=8.2&id=15125)

- Convert a simple package to an assembly package
- Convert an assembly package to simple package
- Convert a project package to an assembly package
- Convert an assembly package to a project package
- See also
