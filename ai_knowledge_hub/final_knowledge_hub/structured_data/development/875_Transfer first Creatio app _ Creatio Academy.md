# Transfer first Creatio app | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 458 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/getting-started/first-app/transfer-application

## Description

We recommend to use separate working environments when developing new or
revising existing features, as well as testing and using Creatio.

## Key Concepts

configuration, section, database, package, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/first-app/transfer-application)**
(8.3).

Version: 8.0

On this page

Level: beginner

We recommend to use separate working environments when developing new or
revising existing features, as well as testing and using Creatio.

Below we will describe a way to transfer a package developed in the
[Develop your first application](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/category/app-development)
example between environments using the Creatio IDE.

To transfer the package using the
[WorkspaceConsole utility](https://academy.creatio.com/documents?ver=8.0&id=15207),
contact Creatio support.

## 1\. Export a package from the development environment​

Export the `TryItPackage` from the development environment as a \*.zip archive.

1. Go to the **Configuration** section.

2. Click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SettingUpEnvironments/scr_Package_Settings.png)
   next to the `TryItPackage`’s title and select **Export**.

The \*.zip archive with the `TryItPackage` will be saved to the downloads folder
(`Downloads` by default).

The saved \*.zip archive contains the `TryItPackage` you can transfer to another
working environment.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SettingUpEnvironments/7.17/scr_Export_Package.gif)

Read more about exporting packages in the
[Packages export and import](https://academy.creatio.com/documents?ver=8.0&id=15203&anchor=title-1226-1)
article.

## 2\. Install a package in the pre-production environment​

- We recommend that you contact Creatio support if your pre-production
  environment is **in the cloud**.
- We recommend to use the Creatio IDE if your pre-production environment is
  **on-site**.

To **install a package** in an on-site pre-production environment:

1. Click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SettingUpEnvironments/scr_Settings_button.png)
   to open the System Designer.

2. Click **Installed applications** in the **Applications** block. The
   **Installed applications** section will open in a separate window.

3. Select **Install from file** in the **Add application** dropdown. An
   application install page will open in a separate window.

4. Click **Select file** and select the `TryItPackage` \*.zip archive.

This will create a back-up copy of the application. The process may take several
minutes.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SettingUpEnvironments/7.17/scr_Install_Package.gif)

Creatio will notify you upon success.

To make the **Group sections** display in the **General** workplace, log out of
Creatio and log back in.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SettingUpEnvironments/scr_Group_Sections.png)

Read more about installing packages in the
[Packages export and import](https://academy.creatio.com/documents?ver=8.0&id=15203&anchor=title-1226-1)
article.

After the package is installed in the pre-production environment, you can start
testing the developed functionality.

## 3\. Install the package in the production environment​

- We recommend that you contact Creatio support if your pre-production
  environment is **in the cloud**.
- We recommend to use the Creatio IDE if your pre-production environment is
  **on-site**.

To **install a package** in an on-site pre-production environment:

1. Choose a service window, i. e. the period when Creatio is least used.

2. Before installing the package with the developed functionality, back up the
   production environment’s database.

A backup copy will be created automatically. The installation of the package
will be the same as with a pre-production environment.

---

## See also​

[Delivery in Creatio IDE](https://academy.creatio.com/documents?ver=8.0&id=15203)

[Delivery in WorkspaceConsole](https://academy.creatio.com/documents?ver=8.0&id=15207)

- 1\. Export a package from the development environment
- 2\. Install a package in the pre-production environment
- 3\. Install the package in the production environment
- See also
