# Plagiarism-proof the source code of a Marketplace app | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 2329 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/plagiarism-proof-the-code

## Description

Creatio stores the open-source code of a Marketplace app in a read-only package.
The code is not plagiarism-proof. Users that have the corresponding access
permissions can view the code. Plagiarism-proof your front-end and back-end code
separately.

## Key Concepts

business process, configuration, section, detail, sql, database, package,
contact, marketplace, customization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

On this page

Level: advanced

Creatio stores the open-source code of a Marketplace app in a read-only package.
The code is not plagiarism-proof. Users that have the corresponding access
permissions can view the code. Plagiarism-proof your front-end and back-end code
separately.

## Plagiarism-proof the C# code​

Use the project package to protect the C# source code of the Marketplace app
from plagiarism. Learn more:
[Project package](https://academy.creatio.com/documents?id=15124).

Important

You are permitted to plagiarism-proof only C# source code developed by you.

The ways to protect the C# code of a Marketplace app from plagiarism are as
follows:

- Develop a **new Marketplace app** as a project package.
- Convert an **existing Marketplace app** to a project package.

Develop your Marketplace app on the configuration level that contains
preinstalled Creatio packages, similar to the development of other apps. Compile
the C# source code of the packages into the `Terrasoft.Configuration.dll` as
part of the publishing. The code can interact with the core. Learn more:
[Creatio customization levels](https://academy.creatio.com/documents?id=15081&anchor=title-1179-1).
View the elaborate diagram of Creatio customization levels on the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/scr_ConfigurationLayerSchema_en.png)

- `CrtBase`, `CrtNUI` are base Creatio packages.
- `OurPackage` is the project package that contains the Marketplace app.
- `Custom` is a special Creatio package.

Project packages offer the following **advantages** for Marketplace apps:

- Exclude the C# code of the custom Marketplace app from
  `Terrasoft.Configuration.dll`.
- Install the Marketplace app as a separate \*.dll.

View the diagram of Creatio customization levels that contain the Marketplace
app's project package in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/scr_PackageProject_en.png)

### Develop the Marketplace app as a project package​

We recommend developing new Marketplace apps as project packages.

**General procedure** to develop the Marketplace app as a project package is as
follows:

1. Set up Creatio for file system development. Read more >>>
2. Create a user-made package. Read more >>>
3. Code the custom functionality. Read more >>>
4. Build the project package. Read more >>>

#### 1\. Set up Creatio for file system development​

Instructions:
[Set up Creatio to work with the file system](https://academy.creatio.com/documents?id=15111&anchor=title-2098-4).

#### 2\. Create a user-made package​

Use one of the following tools to create a user-made package:

- **Creatio IDE**. Instructions:
  [Create a user-made package](https://academy.creatio.com/documents?id=15122).
- **Clio utility**. Learn more:
  [official vendor documentation](https://github.com/Advance-Technologies-Foundation/clio)
  (GitHub).

To create a user-made package using the **Clio utility** :

1. If needed, **install Clio**. Learn more:
   [official vendor documentation](https://github.com/Advance-Technologies-Foundation/clio#register-and-unregister)
   (GitHub).

Command that installs Clio

         dotnet tool install clio -g


2. **Go to the Creatio** `Pkg` **directory**.

Command that opens the Pkg directory

         cd C:\inetpub\wwwroot\creatio\Terrasoft.WebApp\Terrasoft.Configuration\Pkg;



3. **Create a new package**.

Command that creates a new package

         clio init OurPackage;


4. **Set up the package dependencies**. To do this, modify the `descriptor.json`
   file.

See the example that sets up the dependencies (the `DependsOn` property) of the
`OurPackage` package on the `CrtCore` package and adds the package description
(the `Descriptor` property) below.

Example that sets up the package dependencies and adds the package description

         {
             "Descriptor": {
                 "UId": "45cc06b2-6448-4d9e-9f51-bee31a6dbc25",
                 "PackageVersion": "7.8.0",
                 "Name": "OurPackage",
                 "ModifiedOnUtc": "/Date(1633420586000)/",
                 "Maintainer": "Customer",
                 "Description": "Payment calculator",
                 "DependsOn": [
                     {
                         "UId": "2fabaf6c-0f92-4530-aef8-40345c021da2",
                         "PackageVersion": "7.8.0",
                         "Name": "CrtCore"
                     }
                 ]
             }
         }


**As a result** , Creatio will create the `OurPackage` user-made package that
depends on the `CrtCore` package.

#### 3\. Code the custom functionality​

You can code the custom functionality in any external IDE. This example uses
Microsoft Visual Studio Code.

To code the custom functionality:

1. **Open the** `OurPackage.sln` **project**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_OurPackage_sln.png)

2. **Download** the relevant version of **CreatioSDK NuGet package** from the
   repository available on the
   [official vendor website](https://www.nuget.org/packages/CreatioSDK/).

3. **Install the CreatioSDK NuGet package**.

4. **Implement the custom functionality** in the `Files\cs` app directory.

You can create the app in the IDE while developing the C# code. To do this,
press `Ctrl+Shift+B` in Visual Studio.

5. **Build the app**.

If the IDE builds the app successfully, the _.dll, _.pdb, and other auxiliary
files will be placed in the `Files\Bin` app directory.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_FilesBin_folder.png)

6. **Upload the** `OurPackage` **package** from the
   `[Path to app]\Terrasoft.WebApp\Terrasoft.Configuration\Pkg` directory **to
   the database**.
   1. Open the **Configuration** section. Instructions:
      [Open the **Configuration** section](https://academy.creatio.com/documents?id=15101&anchor=title-2093-2).

   2. Click **Actions** → **File system development mode** group → **Update
      packages from file system**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_UpdatePackage.png)

This uploads the `OurPackage` package to Creatio IDE.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_ImportPackage.png)

7. **Restart Creatio**.

Command that restarts Creatio

         clio restart


#### 4\. Build the project package​

Build the project package to **prepare the Marketplace app for publishing** on
the Creatio Marketplace online platform.

Important

If you want to exclude the C# source code that belongs to you from the project
package, make sure to delete the code before exporting the package.

To build the assembly package:

1. **Delete the C# source code** that belongs to you from the project package
   (if necessary). Do this if you want to exclude the C# source code from the
   project package.

2. **Create the** `PackagePublish.target` **file** to automate the project
   package building.

3. **Add the following code** to the `PackagePublish.target` file.

PackagePublish.target file

         <?xml version="1.0" encoding="utf-8" ?>
         <Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
             <PropertyGroup>
                 <DestinationFolder>C:\PkgRelease\$(AssemblyName)</DestinationFolder>
             </PropertyGroup>

             <ItemGroup>
                 <PkgAssemblies Include="Assemblies\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgData Include="Data\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgFiles Include="Files\Bin\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgProperties Include="Properties\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgResources Include="Resources\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgSchemas Include="Schemas\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgSqlScripts Include="SqlScripts\**"/>
             </ItemGroup>
             <ItemGroup>
                 <PkgDescriptor Include="descriptor.json"/>
             </ItemGroup>

             <Target Name="CopyFiles">
                 <Copy
                     SourceFiles="@(PkgAssemblies)"
                     DestinationFiles="@(PkgAssemblies->'$(DestinationFolder)\Assemblies\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgData)"
                     DestinationFiles="@(PkgData->'$(DestinationFolder)\Data\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgFiles)"
                     DestinationFiles="@(PkgFiles->'$(DestinationFolder)\Files\Bin\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgProperties)"
                     DestinationFiles="@(PkgProperties->'$(DestinationFolder)\Properties\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgResources)"
                     DestinationFiles="@(PkgResources->'$(DestinationFolder)\Resources\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgSchemas)"
                     DestinationFiles="@(PkgSchemas->'$(DestinationFolder)\Schemas\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgSqlScripts)"
                     DestinationFiles="@(PkgSqlScripts->'$(DestinationFolder)\SqlScripts\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
                 <Copy
                     SourceFiles="@(PkgDescriptor)"
                     DestinationFiles="@(PkgDescriptor->'$(DestinationFolder)\%(RecursiveDir)%(Filename)%(Extension)')"
                 />
             </Target>

             <Target Name="CreateRelease" AfterTargets="CopyFiles">
                 <Exec Command="clio generate-pkg-zip  $(DestinationFolder) -d C:\PkgRelease\$(AssemblyName).gz" />
             </Target>
         </Project>


4. **Add the following string** to the `OurPackage.csproj` file.

OurPackage.csproj file

         <Import Project="PackagePublish.target" />


5. **Open the command line**.

6. **Run the following command**.
   msbuild /t:CreateRelease  


**As a result** , Creatio will download the project package to the
`C:\PkgRelease` directory that contains the `OurPackage` subdirectory and the
`OurPackage.gz` \*.gz archive. The archive contains the Marketplace app ready to
be published on the Creatio Marketplace online platform.

### Convert the Marketplace app package to a project package​

You might need to modify your Marketplace app significantly to prepare it for
the conversion to a project package.

Use the `clio convert` command to convert the existing Marketplace app to a
project package. Instructions:
[official vendor documentation](https://github.com/Advance-Technologies-Foundation/clio#convert-existing-package-to-project)
(GitHub).

Some files and schemas are not suitable for conversion. For example, the **User
task** business process element. The **User task** process element remains a
partial class regardless of the **Partial** flag status. Place the element to
`Terrasoft.Configuration.dll` library. By default, the utility saves the code of
the **User task** element to the `AutoGenerated` directory of the project
package, not `Terrasoft.Configuration.dll`, as part of the conversion.

To convert the existing Marketplace app to a project package, **run one of the
following commands** :

- `clio convert .\OurPackage_Conf\ -c false`.
- `clio convert .\OurPackage_Conf\`.

The outcome of each command is identical since the utility sets the `-c`
(ConvertSourceCode) key to `false` by default.

After the conversion, the C# package will contain the following data:

- The project package, which contains the **converted Marketplace app**.
- The \*.zip archive that contains the **original Marketplace app**.

View the structure of the C# project after the conversion on the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_CsProject.png)

**As a result** , the existing Marketplace app will be converted to a project
package ready to be installed into Creatio.

note

Generate the project package as part of the CI/CD pipeline. We recommend storing
the unprotected source code of your Marketplace app in the repository.

## Plagiarism-proof the JavaScript code​

The ways to plagiarism-proof the JavaScript code of a Marketplace app are as
follows:

- minification
- obfuscation

Important

Do not modify the structure of the client module schema. Creatio Designers
expect a particular schema structure.

The best way to plagiarism-proof the JavaScript code is to implement the
protected logic using mixins. We do not recommend obfuscating client module
schemas that Creatio Wizards (Section Wizard, Page Wizard, Detail Wizard)
utilize.

You can obfuscate the JavaScript code using a large number of open source
solutions. This example uses JavaScript Obfuscator. Learn more:
[official vendor documentation](https://github.com/javascript-obfuscator/javascript-obfuscator)
(GitHub).

To plagiarism-proof the JavaScript code using **JavaScript Obfuscator** :

1. **Install JavaScript Obfuscator**. Instructions:
   [official vendor documentation](https://github.com/javascript-obfuscator/javascript-obfuscator#installation)
   (GitHub).

Command that installs JavaScript Obfuscator

         npm install javascript-obfuscator -g


2. **Prepare the JavaScript code for obfuscation**.
   1. Create a mixin.

For this example, create the `MRKT_DemoMixin` mixin. Learn more:
[Mixins (mixins)](https://academy.creatio.com/documents?id=15311&anchor=title-3051-4).

     2. Implement the JavaScript code to obfuscate in the mixin.

MRKT_DemoMixin

            define("MRKT_DemoMixin", [], function () {
                Ext.define("Terrasoft.configuration.mixins.MRKT_DemoMixin", {
                    alternateClassName: "Terrasoft.MRKT_DemoMixin",

                    secretMethod: function () {
                        console.log("MRKT_DemoMixin");
                    },
                });
            });


     3. Add the `MRKT_DemoMixin` mixin to the `mixins` property of the client module schema.

For this example, add the `MRKT_DemoMixin` mixin to the `ContactPageV2` client
module schema.

ContactPageV2

            define("ContactPageV2", ["MRKT_DemoMixin"], function() {
                return {
                    entitySchemaName: "Contact",
                    mixins: {
                        "MRKT_DemoMixin": "Terrasoft.MRKT_DemoMixin"
                    },
                    attributes: {},
                    modules: /**SCHEMA_MODULES*/{}/**SCHEMA_MODULES*/,
                    details: /**SCHEMA_DETAILS*/{}/**SCHEMA_DETAILS*/,
                    businessRules: /**SCHEMA_BUSINESS_RULES*/{}/**SCHEMA_BUSINESS_RULES*/,
                    methods: {
                        onEntityInitialized: function() {
                            this.callParent(arguments);

                            /* Consume MRKT_DemoMixin. */
                            this.secretMethod();
                        },
                    },
                    dataModels: /**SCHEMA_DATA_MODELS*/{}/**SCHEMA_DATA_MODELS*/,
                    diff: /**SCHEMA_DIFF*/[]/**SCHEMA_DIFF*/
                };
            });


3. **Back up the unprotected JavaScript code**. You might need to edit it later.

4. **Obfuscate the JavaScript code**.

Command that obfuscates the JavaScript code

         javascript-obfuscator MRKT_DemoMixin.js --output MRKT_DemoMixin.obfuscated.js


Learn more:
[official vendor documentation](https://github.com/javascript-obfuscator/javascript-obfuscator#cli-usage)
(GitHub).

**As a result** , JavaScript Obfuscator will generate an obfuscated file. View
the example of the obfuscated file below.

Example of an obfuscated file

    function a0_0x2c69() {
        var _0x272852 = ['Terrasoft.MRKT_DemoMixin', 'Ok\x20-\x20MRKT_DemoMixin', '636527SjITzq', '47544MWcgAk', '1503XwngZr', '1735980OhnVnL', '7cyzbFA', '1795796hIfdLG', '655476qGUaEY', '22085740BJZJXi', '3038716Shuabr', 'MRKT_DemoMixin', '5iENPSJ'];
        a0_0x2c69 = function() {
            return _0x272852;
        };
        return a0_0x2c69();
    }
    var a0_0x31e3ab = a0_0x3f9a;

    function a0_0x3f9a(_0x104961, _0x4f9883) {
        var _0x2c694d = a0_0x2c69();
        return a0_0x3f9a = function(_0x3f9a09, _0x1d247d) {
            _0x3f9a09 = _0x3f9a09 - 0xa7;
            var _0x481962 = _0x2c694d[_0x3f9a09];
            return _0x481962;
        }, a0_0x3f9a(_0x104961, _0x4f9883);
    }(function(_0x479332, _0x464f89) {
        var _0x279ddd = a0_0x3f9a,
            _0x3c692e = _0x479332();
        while (!![]) {
            try {
                var _0xae3ae0 = -parseInt(_0x279ddd(0xac)) / 0x1 + parseInt(_0x279ddd(0xa7)) / 0x2 + parseInt(_0x279ddd(0xaf)) / 0x3 + -parseInt(_0x279ddd(0xb1)) / 0x4 * (-parseInt(_0x279ddd(0xa9)) / 0x5) + -parseInt(_0x279ddd(0xb2)) / 0x6 * (-parseInt(_0x279ddd(0xb0)) / 0x7) + -parseInt(_0x279ddd(0xad)) / 0x8 * (-parseInt(_0x279ddd(0xae)) / 0x9) + -parseInt(_0x279ddd(0xb3)) / 0xa;
                if (_0xae3ae0 === _0x464f89) break;
                else _0x3c692e['push'](_0x3c692e['shift']());
            } catch (_0x44cb38) {
                _0x3c692e['push'](_0x3c692e['shift']());
            }
        }
    }(a0_0x2c69, 0xc4309), define(a0_0x31e3ab(0xa8), [], function() {
        var _0x3dbe12 = a0_0x31e3ab;
        Ext['define']('Terrasoft.configuration.mixins.MRKT_DemoMixin', {
            'alternateClassName': _0x3dbe12(0xaa),
            'secretMethod': function() {
                var _0x3b8302 = _0x3dbe12;
                return _0x3b8302(0xab);
            }
        });
    }));

To view the JavaScript code in the browser page:

1. **Clear the browser cache**.
2. **Refresh the page**.
3. **Open the developer tools**. Instructions:
   [Integrated debugging tools](https://academy.creatio.com/documents?id=15193&anchor=title-2127-1).

View the example of the JavaScript code in the browser page in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MarketplacePlagiarism/7.18/scr_CodeInBrowser.png)

note

Obfuscate the JavaScript code as part of the CI/CD pipeline. We recommend
storing the unprotected JavaScript source code of your Marketplace app in the
repository.

---

## See also​

[Project package](https://academy.creatio.com/documents?id=15124)

[Creatio development basics](https://academy.creatio.com/documents?id=15081)

[External IDEs basics](https://academy.creatio.com/documents?id=15111)

[Create a user-made package](https://academy.creatio.com/documents?id=15122)

[Creatio IDE overview](https://academy.creatio.com/documents?id=15101)

---

## Resources​

[Official Clio utility documentation](https://github.com/Advance-Technologies-Foundation/clio)
(GitHub)

[CreatioSDK NuGet package](https://www.nuget.org/packages/CreatioSDK/)

[Official JavaScript Obfuscator documentation](https://github.com/javascript-obfuscator/javascript-obfuscator)
(GitHub)

[Marketplace updates](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/category/marketplace-updates)

- Plagiarism-proof the C# code
  - Develop the Marketplace app as a project package
  - Convert the Marketplace app package to a project package
- Plagiarism-proof the JavaScript code
- See also
- Resources
