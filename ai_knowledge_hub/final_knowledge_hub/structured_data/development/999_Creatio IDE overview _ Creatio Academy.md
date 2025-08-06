# Creatio IDE overview | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 3558 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/creatio-ide/overview-creatio-ide

## Description

The Creatio platform includes an integrated development environment (Creatio
IDE). Creatio IDE is located in the Configuration section. The Configuration
section lets you execute operations with the structural items.

## Key Concepts

workflow, configuration, freedom ui, section, detail, lookup, web service,
odata, sql, database

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/overview-creatio-ide)**
(8.3).

Version: 8.1

On this page

Level: beginner

The Creatio platform includes an integrated development environment (**Creatio
IDE**). Creatio IDE is located in the **Configuration** section. The
**Configuration** section lets you execute operations with the structural items.

## Set up permissions to the Configuration section​

You can set up permissions to the **Configuration** section on the system
operation level. If a user lacks the permission to access the **Configuration**
section, they receive a standard notification about the lack of permissions to
execute an operation when trying to load the section. Out of the box, only
Creatio administrators have access to key system operations. Creatio lets you
configure access permissions to system operations for users or user groups.
Learn more:
[System operation permissions](https://academy.creatio.com/documents?ver=8.1&id=2000)
(user documentation).

To set up permissions to the **Configuration** section:

1. **Open the Operation permissions section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **Users and administration** → **Operation permissions**.
2. **Select the Can manage configuration elements** (`CanManageSolution` code)
   **system operation**.
3. **Set up the access to the Configuration section**. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_add_button.png)
   and specify the user/role in the **Operation permission** detail.

**As a result** :

- The record will appear on the **Operation permission** detail.
- The **Access level** column of the record will be set to **Yes**.
- Users that have the specified role will have access to the **Configuration**
  section.

## Open the Configuration section​

You can open the **Configuration** section in Creatio **.NET Framework** in
several ways:

- **Using System Designer**. To do this, click
  ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
  in the top right → **Admin area** → **Advanced settings**.

- **Using the browser URL**.

| Alias | URL example | .NET Framework | .NET Core or .NET 6 | /ClientApp/#/WorkspaceExplorer | `http://mycreatio.com/0/ClientApp/#/WorkspaceExplorer` | `http://mycreatio.com/ClientApp/#/WorkspaceExplorer` | /we | `http://mycreatio.com/0/we` | `http://mycreatio.com/we` | /conf | `http://mycreatio.com/0/conf` | `http://mycreatio.com/conf` | /dev | `http://mycreatio.com/0/dev` | `http://mycreatio.com/dev` |
| ----- | ----------- | -------------- | ------------------- | ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------- | --- | --------------------------- | ------------------------- | ----- | ----------------------------- | --------------------------- | ---- | ---------------------------- | -------------------------- |

**As a result** , Creatio opens the **Configuration** section in a new tab.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_common_view_new.png)

- Toolbar (1)
- Package workspace (2)
- Main workspace (3)

## Manage packages​

**Configuration** section lets you manage packages using the following tools:

- **Packages action group**. To do this, click **Actions** on the section
  toolbar → **Packages**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_Packages.png)

- **Package workspace**

- **Package menu** in the package workspace

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_PackageMenu.png)

| UI element | Action | Packages action group | Package dependencies diagram | Open the package dependencies diagram. Learn more: [Package dependencies and hierarchy](https://academy.creatio.com/documents?ver=8.1&id=15121&anchor=title-2105-3). | Package workspace | Search by package | Search for a package by its name | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Add_Package.png) | Create a package. The button opens the package creation box that lets you fill out the package properties. Instructions: [Create a user-made package using Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15122). | All packages | View the list of Creatio packages. The packages are displayed in alphabetical order. Regardless of sorting, Creatio displays the modified packages and modifiable packages at the top of the **All packages** directory index and marks the modified packages using ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_ChangedPackage.png). If you select the **All packages** directory, Creatio displays the configuration elements of all packages in the **Configuration** section list alphabetically. If you select a different package, Creatio displays the configuration elements of that package alphabetically. Regardless of sorting, Creatio displays the modified configuration elements at the top of the record list and marks them using ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_star_icon.png) next to the name. Creatio places the modified elements at the top of the record list. | Package menu | Compile | Compile the package to an assembly package. The item is inactive for packages that have the **Compile into a separate assembly** checkbox cleared in the package properties. The checkbox specifies that the package is an assembly package. Learn more: [Assembly package](https://academy.creatio.com/documents?ver=8.1&id=15125). | Export | Export a package as a \*.zip archive. You can install the exported package into a different environment. Instructions: [Transfer packages](https://academy.creatio.com/documents?ver=8.1&id=15204&anchor=title-2128-1). | Move all elements | Move the package configuration elements to a different package. The item opens a box that lets you select the destination package. When you move the configuration elements, Creatio IDE can set dependencies automatically. | Delete | Delete a package. Not available for preinstalled packages. **Configuration** section lets you delete empty packages and packages that contain non-parent configuration elements. Attempting to delete a package with parent configuration elements will result in Creatio displaying a list of dependent packages and dependent elements that block deletion. You can delete a package that is a part of app. You need to confirm the deletion. Note that package removal can make app lose functionality or become inoperative. | Lock package in SVN | Lock the package from changes in the connected SVN repository. The item is available only for packages installed from the SVN repository. | Unlock package in SVN | Unlock the package for changes in the connected SVN repository. The item is active only for locked packages installed from the SVN repository. | Update from repository | Update the package from the repository. Instructions: [Update a package from the SVN repository](https://academy.creatio.com/documents?ver=8.1&id=15141&anchor=title-2109-3). | Commit to repository | Commit a package to the repository. Instructions: [Commit a package to the SVN repository](https://academy.creatio.com/documents?ver=8.1&id=15141&anchor=title-2109-1). | Properties | View the package properties. To **open the package properties** , double-click the package name. This opens the **Properties** tab. The tab lets you set up the package dependencies for modifiable packages and contains system information: the package author and editor, the creation and modification dates, the unique ID, and the primary package key in the database table. |
| ---------- | ------ | --------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## Manage configuration elements​

To manage configuration elements, use the following actions:

- Add a configuration element. Read more >>>
- Select the type of the configuration element to display. Read more >>>
- Select the status of configuration elements to display. Read more >>>
- Search for a configuration element. Read more >>>
- Sort the configuration elements. Read more >>>
- Execute configuration element actions. Read more >>>

### Add a configuration element​

To select the type of configuration element to add:

1. **Select a package** to add a configuration element. You cannot add
   configuration elements to preinstalled packages.

2. **Select the configuration element** to add. To do this, click **Add** →
   select the configuration element.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_AddList_new.png)

Creatio lets you **import a schema** (_.md) or **a reference assembly** (_.dll)
into the user-made package. To do this, click **Add** on the toolbar of the main
workspace → **Import** → select the file that implements configuration element
to add.

Creatio displays added and existing configuration elements in the section list.

Column| Column description| Name| Custom element name starts with the prefix
specified in the **Prefix for object name** (`SchemaNamePrefix` code) system
setting, `Usr` by default. When a configuration element schema is created, the
prefix specified in the system setting is added to the current field
automatically. Creatio checks for the prefix and whether it matches the system
setting value when saving the schema properties. If the prefix is missing or
does not match, the user receives a corresponding notification.  
The configuration elements are sorted in alphabetical order. The column lets you
view a list of modified configuration elements (marked with
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_star_icon.png)
next to the name). Creatio places the modified elements at the top of the record
list.| Title| The title of the configuration element| Object| The object to
which the bound package data is connected. The column value is available only
for the configuration element of the **Data** type.| Modified on| The
modification date of the configuration element| Package| The name of the package
that contains the configuration element  
---|---

### Select the type of configuration elements to display​

To select the type of configuration elements to display in the section list,
**click Type** on the toolbar of the main workspace → select the type of the
configuration element.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_TypeList_addAddon.png)

Creatio displays the selected type in the **Type** column of the section list.

Type| Configuration element| Client module| Freedom UI page  
Module  
Page view model  
Section view model  
Detail (list) view model  
Detail (fields) view model  
Replacing view model| Object| Object  
Replacing object| Web service| REST service  
SOAP service  
---|---

### Select the status of configuration elements to display​

To select the status of configuration elements to display in the section list,
**click Filters** on the toolbar of the main workspace → select the status.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_FiltersList.png)

Creatio displays configuration elements that have selected status in the
**Status** column of the section list. Creatio saves the settings of the
**Filters** drop-down list to the user profile and applies them when you open
the **Configuration** section.

View configuration element statuses that are available in the **Filters**
drop-down list and **Status** in the table below.

| Status icon | Status description | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Locked_icon.png) | The configuration element is locked and you cannot change it | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_NeedActualization_icon.png) | The configuration element must be updated | ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png) | The configuration element contains an error |
| ----------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |

### Search for a configuration element​

To search for a configuration element in the section list by the element name:

1. **Select the search option** in the package workspace.
   - Select the package to search for a configuration element **in the current
     package**.
   - Select the **All packages** directory to search for a configuration element
     **in all packages**.

2. **Enter the value** in the **Search** search bar of the main workspace
   toolbar.

3. **Set up additional search parameters**.
   1. Click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_SearchSettings_Button.png)
      in the **Search** search bar of the main workspace toolbar.

   2. Fill out the search parameters.

| Parameter | Parameter description | Search by column "Title" | Search by title. Selected by default. | Search by column "UID" | Search by a unique ID | Starts with | Search mode. The configuration element name starts with the text you type in the **Search** search bar. Selected by default. | Contains | Search mode. The configuration element name contains the text you type in the **Search** search bar. | Equals | Search mode. The configuration element name is the same as the text you type in the **Search** search bar. |
| --------- | --------------------- | ------------------------ | ------------------------------------- | ---------------------- | --------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |

4. **Apply the changes**.

Creatio saves the search settings to the user profile and applies them when you
open the **Configuration** section.

### Sort the configuration elements​

Creatio lets you sort the configuration elements in the list ascending or
descending. To sort the configuration elements:

1. **Select the sort option**.
   - Sort the configuration elements in the **current package**. To do this,
     select a package in the package workspace.
   - Sort the configuration elements in **all packages**. To do this, select the
     **All packages** directory in the package workspace.

2. **Click the column name**.

Regardless of sorting, Creatio displays the modified configuration elements at
the top of the record list and marks them using
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_star_icon.png)
next to the name. Creatio places the modified elements at the top of the record
list.

### Execute configuration element actions​

**Configuration** section lets you execute configuration element actions using
the following tools:

- **Configuration element menu** in the main workspace. Use to execute a single
  configuration element action. To do this, click
  ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Settings.png)
  in the configuration element row of the section list → select the action in
  the configuration element menu. The item index of the configuration element
  menu depends on the configuration element type. Learn more:
  [Select the type of configuration elements to display](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-14).

- **Multi actions drop-down list** in the main workspace toolbar. Use to execute
  bulk configuration element actions.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_MultiActionsList.png)

- **Actualize items action group**. Use to execute a limited list of bulk
  configuration element actions. To do this, click **Actions** on the section
  toolbar → **Actualize items**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_ActualizeItems.png)

To execute bulk configuration element actions **using the Multi actions
drop-down list** :

1. **Select configuration elements** in the section list of the main workspace
   to activate the items of the **Multi actions** drop-down list.
2. **Click Multi actions** → select the action. The index of displayed items in
   the **Multi actions** drop-down list depends on the type of configuration
   elements selected in the section list. Learn more:
   [Select the type of configuration elements to display](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-14).

UI element for single action (configuration element menu)| UI element for bulk
actions| Action| Configuration element type that supports UI element| Multi
actions drop-down list| Actualize items action group| Edit process| Not
available| Not available| Edit an object. If the object was created by a third
party, Creatio displays the corresponding notification.| Object| Export| Export|
Not available| Download single or multiple configuration elements. Creatio saves
data of a single configuration element as an _.md file. Creatio saves data of
several configuration elements as an _.zip archive. You can install the exported
configuration elements into a different environment. Instructions:
[Transfer configuration elements](https://academy.creatio.com/documents?ver=8.1&id=15206),
[Transfer packages](https://academy.creatio.com/documents?ver=8.1&id=15204&anchor=title-2128-1).|
Object  
Source code  
Client module  
Business-process  
Web service  
Case  
User task  
Marketing campaign| Move to another package| Move to another package| Not
available| Move single or multiple configuration elements to another package.
The item opens a box that lets you select the destination package. When you move
the configuration elements, Creatio IDE can set dependencies automatically.| All
types| Delete| Delete| Not available| Delete single or multiple configuration
elements. Inactive for configuration elements in preinstalled packages.If
needed, use
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_DeleteButton.png)
to delete a single configuration element in the section list. The button is
available for configuration elements of user-made packages. Hover over the
record in the **Configuration** section list to bring up the button.| All types|
Install| Install SQL script  
Install data| Install SQL scripts where it is needed  
Install data where it is needed| Install single or multiple configuration
elements into the database. The **Status** column in the section list includes
the **Needs to be installed in database** tooltip for configuration elements to
be installed. Creatio also displays the error description in the configuration
element properties. Creatio displays the corresponding notification after
installing the configuration elements.| SQL script  
Data| Update database structure| Update objects DB structure| Update DB
structure where it is needed| Update the database structure for single or
multiple objects. The **Status** column in the section list includes the **Needs
to be updated in database** tooltip for configuration elements to be updated.
Creatio displays the corresponding notification after updating the configuration
elements.| Object| Generate source code| Generate source code| Not available|
Generate the source code of single or multiple configuration elements. Creatio
runs the process if the process includes compliable elements. The **Status**
column in the section list includes the **Needs generate source code** tooltip
for configuration elements that have source code to be generated.| Object  
Business-process  
User task| Open metadata| Not available| Not available| Open the metadata tab of
the current configuration element| Object  
Source code  
Client module  
Business-process  
Web service  
Case  
User task  
Marketing campaign| Open source code| Not available| Not available| Open the
source code tab of the current configuration element| Object  
Business-process  
User task| Lock element in SVN| Not available| Not available| Lock the current
configuration element from changes in the connected SVN repository. The item is
available only for configuration elements installed from the SVN repository.|
All types| Unlock element in SVN| Not available| Not available| Unlock the
current configuration element for changes in the connected SVN repository. The
item is available only for configuration elements installed from the SVN
repository.| All types| Discard changes| Not available| Not available| Discard
the changes from the version control system repository. The item is available if
the configuration element’s package is connected to a version control system
repository.| All types| Properties| Not available| Not available| Open the
properties box of the current configuration element| All types  
---|---|---|---|---

## Manage the source code​

**Configuration** section lets you manage the source code using the **Source
code action group**. To do this, click **Actions** on the section toolbar →
**Source code**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_SourceCode.png)

| UI element | Action | Source code action group | Generate for modified schemas | Generate the source code for modified schemas | Generate the source code for schemas that require it | Generate the source code for schemas that require it | Generate for all schemas | Generate the source code for every schema. This operation might take more than 10 minutes. |
| ---------- | ------ | ------------------------ | ----------------------------- | --------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------ |

Creatio generates the source code for schemas in the background. Learn more:
[Execute operations in the background](https://academy.creatio.com/documents?ver=8.1&id=15231).

The **major features** of background generation are as follows:

- Background generation does not affect the core user workflows.
- Starting compilation or a new source code generation is not possible while the
  running operation is not complete. If you attempt to start these actions,
  Creatio warns you that the source code generation is still in progress.
- We do not recommend working on functionality that requires compilation until
  the source code generation is done. That includes installing applications and
  extensions, configuring the UI and business logic.

**As a result** , Creatio will display the corresponding notification in the
communication panel.

## Manage the file system​

**Configuration** section lets you manage the file system using the **File
system development mode action group**. To do this, click **Actions** on the
section toolbar → **File system development mode**. To access the items in the
**File system development mode** action group, **enable the file system
development mode**. Instructions:
[Set up Creatio to work with the file system](https://academy.creatio.com/documents?ver=8.1&id=15111&anchor=title-2098-4).
Hover over an item in the action group to display a hint to enable the mode.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_FileSystemDevelopmentMode.png)

| UI element | Action | File system development mode action group | Download packages to file system | Download packages from the Creatio database to the `...\Terrasoft.WebApp\Terrasoft.Configuration\Pkg` directory | Update packages from file system | Upload packages from the `...\Terrasoft.WebApp\Terrasoft.Configuration\Pkg` directory to the Creatio database |
| ---------- | ------ | ----------------------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------- |

## Manage SVN repositories​

**Configuration** section lets you manage SVN repositories using the **SVN
repositories action group**. To do this, click **Actions** on the section
toolbar → **SVN repositories**. The SVN version control is only available for
Creatio .NET Framework. Learn more:
[Version control using the Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15141).

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_SvnRepositories_new.png)

| UI element | Action | SVN repositories action group | Install package from repository | Install a package from the SVN repository | Open list of repositories | Open the **List of repositories** tab that lets you add, set up, and delete links to the SVN repositories available in Creatio. | Restore from repository | Update the configuration from the latest version in the SVN repository. The changes not yet committed to the SVN repository will be lost. |
| ---------- | ------ | ----------------------------- | ------------------------------- | ----------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |

## Manage the configuration​

Creatio lets you execute the following configuration management actions:

- Validate the configuration. Read more >>>
- Compile the configuration. Read more >>>

### Validate the configuration​

**Configuration** section lets you validate the configuration using the
**Configuration action group**. To do this, click **Actions** on the section
toolbar → **Configuration**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_Configuration.png)

| UI element | Action | Configuration action group | Validate configuration | Check for dependency conflicts that might appear after you transfer elements between packages |
| ---------- | ------ | -------------------------- | ---------------------- | --------------------------------------------------------------------------------------------- |

### Compile the configuration​

**Configuration** section lets you compile the configuration using buttons on
the section toolbar.

| UI element | Action | Section toolbar | Compile | Compile only the configuration changes | Compile all | Compile all configuration |
| ---------- | ------ | --------------- | ------- | -------------------------------------- | ----------- | ------------------------- |

**As a result** :

- The executable files will be updated.
- The static content will be downloaded to the `...\Terrasoft.WebApp\conf`
  directory.
- A corresponding notification will be displayed once the compilation finishes.
- The changes will be taking effect for users working in the relevant
  configuration.

If **errors or warnings occur as part of the compilation** , Creatio displays:

- The list of compilation errors present in your configuration in the
  **Compilation results** dialog box.

- The **Compilation errors** button in the **Configuration** section. Available
  in Creatio 8.1.2 and later.

![](https://academy.creatio.com/docs/sites/academy_en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.1/scr_CompilationErrors.png)

The button is visible only if your configuration has compilation errors. The
error list takes into account both full configuration compilation and
compilation of separate assembly packages.

Click the **Compilation errors** button to **check the list of compilation
errors**. This opens the **Compilation results** dialog box that includes the
list of compilation errors present in your configuration.

- The **Compilation error** indicator on the app page. Available in Creatio
  8.1.2 and later.

![](https://academy.creatio.com/docs/sites/academy_en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.1/scr_CompilationWarning.png)

The indicator is visible only for system administrators. Click the indicator to
**view the error list** in the **Configuration** section.

The compilation errors have the following properties:

- The error type icon (error
  ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
  or warning
  ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)).
- The name of the relevant file.
- The error description.
- The error code.
- The number of the line with an error.

Creatio also saves history compilation that was run manually or automatically to
the `CompilationHistory` **object**. The `CompilationHistory` object includes
errors and warnings that occur as part of configuration, OData, or assembly
package compilation.

To **view the compilation results** :

1. **Open the Lookups section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **Lookups**.

2. **Create a lookup**.
   1. Click **New lookup**.

   2. Fill out the lookup properties.

| Property | Property value | Name | Compilation history | Object | Compilation History |
| -------- | -------------- | ---- | ------------------- | ------ | ------------------- |

     3. Save the changes.

3. **Open the Communication history lookup**.

**As a result** :

- The compilation results will be displayed in the **Result** column.
- If errors or warnings occur during the compilation, i. e., the `No` value in
  the **Result** column, any compilation errors will be displayed in the
  **Errors/Warnings** column.
- User who ran the compilation will be displayed in the **Started by** column.
  Available in Creatio 8.1.1 and later.
- Compilation duration will be displayed in the **Duration** column. Available
  in Creatio 8.1.1 and later.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.1/scr_CompilationHistory.png)

## Close the Configuration section​

To close the **Configuration** section, click the **Close** button on the
section toolbar.

---

## See also​

[System operation permissions](https://academy.creatio.com/documents?ver=8.1&id=258)
(user documentation)

[Packages overview](https://academy.creatio.com/documents?ver=8.1&id=15121)

[Create a user-made package using Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15122)

[Assembly package](https://academy.creatio.com/documents?ver=8.1&id=15125)

[Transfer packages](https://academy.creatio.com/documents?ver=8.1&id=15204)

[Transfer configuration elements](https://academy.creatio.com/documents?ver=8.1&id=15206)

[Version control using the Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15231)

[Execute operations in the background](https://academy.creatio.com/documents?ver=8.1&id=15304)

[External IDEs basics](https://academy.creatio.com/documents?ver=8.1&id=15111)

---

## Resources​

[Back-end development ](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/back-end-development)

[Front-end development](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/front-end-development)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/online-courses/development-creatio-platform-0)

- Set up permissions to the Configuration section
- Open the Configuration section
- Manage packages
- Manage configuration elements
  - Add a configuration element
  - Select the type of configuration elements to display
  - Select the status of configuration elements to display
  - Search for a configuration element
  - Sort the configuration elements
  - Execute configuration element actions
- Manage the source code
- Manage the file system
- Manage SVN repositories
- Manage the configuration
  - Validate the configuration
  - Compile the configuration
- Close the Configuration section
- See also
- Resources
- E-learning courses
