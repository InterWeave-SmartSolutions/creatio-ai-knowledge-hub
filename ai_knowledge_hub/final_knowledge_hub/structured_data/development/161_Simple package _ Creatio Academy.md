# Simple package | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 629 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/packages/simple-package

## Description

Creatio includes the following types of simple packages:

## Key Concepts

configuration, section, detail, dashboard, database, system setting, package,
case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/simple-package)**
(8.3).

Version: 8.1

On this page

Creatio includes the following types of simple packages:

- Preinstalled packages. Read more >>>
- User-made packages. Read more >>>

## Preinstalled packages​

Preinstalled packages are available in the workspace by default. They cannot be
modified. Creatio marks preinstalled packages in the **Configuration** section
using
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Blocked.png).

Creatio includes the following types of preinstalled packages:

- **Base packages**. For example, `CrtBase`, `CrtNUI`.
- **Third-party packages**. These packages are installed from \*.zip archives
  using Creatio IDE or the WorkspaceConsole utility.

View base packages in the table below.

| Package name | Description | CrtBase, Base | Base schemas of the primary objects and Creatio sections, as well as connected objects, pages, process schemas, etc. | Platform, CrtPlatform7x | Modules and pages of the Section Wizard, List Designer, Dashboard Designer, etc. | Managers, CrtManagers7x | Client modules of the schema managers. | CrtNUI, NUI | Functionality connected to the Creatio UI. | CrtUIv2, UIv2 | CrtDesignerTools, DesignerTools | Schemas of Designers and their elements. | CrtProcessDesigner, ProcessDesigner | Process Designer schemas. |
| ------------ | ----------- | ------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------- | -------------------------------------------------------------------------------- | ----------------------- | -------------------------------------- | ----------- | ------------------------------------------ | ------------- | ------------------------------- | ---------------------------------------- | ----------------------------------- | ------------------------- |

User creates various schemas that must be saved to a user-made package. A fresh
Creatio installation has no packages open for modification except for the
`Custom` preinstalled package. You can add schemas to this package manually or
using the Wizards.

**Specific features** of the `Custom` package:

- The `Custom` package cannot be added to the version control system. As such,
  you can transfer the package’s schemas to a different environment only using
  the export and import functionality. Learn more:
  [Transfer packages](https://academy.creatio.com/documents?ver=8.1&id=15204).
- Unlike other preinstalled packages, the `Custom` package cannot be exported to
  the file system via the WorkspaceConsole utility.
- The `Custom` package has all of the other preinstalled packages as
  dependencies. If you create or install a user-made package, the new package
  becomes a dependency for the `Custom` package automatically. Therefore, always
  place the `Custom` package the last in the package hierarchy.
- User-made packages cannot have the `Custom` package as a dependency.

You can **use the** `Custom` **package** in the following cases:

- You will not transfer changes to a different environment.

Not only do the Section Wizard and Detail Wizard create various schemas, they
also bind data to the current package. The `Custom` package does not support the
standard package import mechanism. Therefore, if the `Custom` package is your
current package, you can only transfer the bound data to another user-made
package via database queries. We strongly recommend against this method as the
changes can affect the database structure and render Creatio inoperable. If you
have to modify Creatio functionality significantly, use a user-made package.

- You customize Creatio either manually or using Wizards, and the changes are
  minor.

- You do not need to use a version control system.

## User-made packages​

Use a user-made package to develop of additional functionality or expand
existing functionality.

Creatio includes the following types of user-made package:

- User-made packages **created by other Creatio users**. User-made packages are
  locked in the version control system. They cannot be modified. Creatio marks
  user-made packages in the **Configuration** section using
  ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_CustomPackage_Blocked.png).
- User-made packages **created by the current user or retrieved from the version
  control system**. They can be modified. Creatio marks user-made packages in
  the **Configuration** section using
  ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_CustomPackage.png).

Before you start development, **change the current package**. To do this:

1. **Open the System settings section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **System settings**.

2. **Open the Current package** (**CurrentPackageId** code) **system setting**.

3. **Change the properties** of the system setting.

| Property | Property description | Default value | A name of user-made package |
| -------- | -------------------- | ------------- | --------------------------- |

4. **Save the changes**.

**As a result** , Creatio will add all configuration elements to the specified
user-made package.

---

## See also​

[Delivery in Creatio IDE ](https://academy.creatio.com/documents?ver=8.1&id=15203)

- Preinstalled packages
- User-made packages
- See also
