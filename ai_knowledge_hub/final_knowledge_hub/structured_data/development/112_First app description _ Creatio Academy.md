# First app description | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 435
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/getting-started/first-app/develop-application/getting-started

## Description

Task description

## Key Concepts

workflow, configuration, section, detail, system setting, package, marketplace,
no-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

## Task description​

Example

Automate the workflow of a fitness center.

1. Add a new **Classes** section to the **Sales** workplace.
2. Create the group exercise timetable in the **Classes** section.
3. A new daily class can only be created if there is an unoccupied gym. The
   number of the fitness center’s gyms is set via a system setting and equals 4.
4. A list of group exercises can be added to each class.

## Preliminary settings​

Develop this sample Creatio application based on Sales Creatio.

A cloud or locally installed Creatio instance is required. The easiest
deployment option is using the 14-day free trial demo version.

Ensure that the current user can access the **Configuration** section. This
section lets users customize Creatio using developer tools.

## Create a development package​

A [package](https://academy.creatio.com/documents?ver=8.3&id=15121) is an
encapsulated set of particular functionality. You can transfer packages between
environments (e.g., export and install in other Creatio applications) and share
them with other users on
[Creatio Marketplace](https://marketplace.creatio.com/).

Manage packages in the Creatio IDE implemented in the **Configuration** section.

To create a package:

1. Go to the **Configuration** section.
   1. Click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_system_designer.png)
      to open the System Designer.

   2. Click **Advanced settings** in the **Admin area** block.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_Advanced_Settings.png)

2. Click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_Add_Package.png)
   in the package workspace to create a package.

3. Fill out the **package properties** :
   - **Name** – "TryItPackage";
   - **Description** – "The "Try it" section’s example package".

4. Add package dependencies

For Creatio sections to be customized, and for base object and client module
templates to be used, it is necessary to configure package dependencies.

To add **package dependencies** :

     1. Click **Create and add dependencies**.

     2. Set the "SalesEnterprise" package as a dependency in the **Depends on packages** detail on the **Dependencies** tab.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_Add_Dependencies.gif)

The created package will be used further in this example.

Important

We strongly recommend against using the "Custom" package for development.

## Override the current package​

Change the "Current package" system setting before starting the development:

1. Click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_system_designer.png)
   to open the System Designer.

2. Click **System settings** in the **System setup** block.

3. Select the "Current package" setting (`CurrentPackageId` code).

4. Select "TryItPackage" in the **Default value** field.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_CurrentPackage_Settings.png)

5. **Save the changes**.

Important

Specify the created user-made package in the "Current package" system setting
(`CurrentPackageId` code) before using **no-code tools** (e. g. the
[Section Wizard](https://academy.creatio.com/documents?ver=8.0&id=1705) and the
Detail Wizard).

On this step, we have configured the development package and set it as the
current Creatio package. Set up the new section’s interface using the built-in
**no-code tools** on
[the next step](https://academy.creatio.com/documents?ver=8.3&id=15012).

---

## See also​

[Step 1. Create a new section](https://academy.creatio.com/documents?ver=8.3&id=15012)

- Task description
- Preliminary settings
- Create a development package
- Override the current package
- See also
