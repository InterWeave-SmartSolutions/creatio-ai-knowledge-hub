# Configuration elements of the Data type | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 432 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/data

## Description

Configuration element of the Data type is an entity that lets you bind data to a
package. Bind data to ensure the developed functionality is transferred between
environments correctly. Learn more about data bindings: Packages basics.

## Key Concepts

configuration, section, operation, package, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

**Configuration element** of the **Data** type is an entity that lets you bind
data to a package. Bind data to ensure the developed functionality is
transferred between
[environments](https://academy.creatio.com/documents?ver=8.3&id=15201)
correctly. Learn more about data bindings:
[Packages basics](https://academy.creatio.com/documents?ver=8.3&id=15121&anchor=title-2105-9).

The items of the **Add** drop-down list in the toolbar of the **Configuration**
section workspace represent the data schema you can add in Creatio IDE.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Data/8.0/scr_AddList.png)

Learn more about configuration element types:
[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-12).

The **Data** type schema in the **Type** drop-down list in the toolbar of the
**Configuration** section workspace represents the configuration element of the
**Data** type. A **schema** is the basis of Creatio configuration.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Data/8.0/scr_TypeList.png)

Learn more about configuration element types:
[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-14).

## Implement a data binding​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.3&id=15121) to add the
   schema.

2. Click **Add** → **Data** in the section list toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Data/8.0/scr_AddList.png)

3. Fill out the schema properties on the data binding page.

The **main schema properties** are as follows:

     * **Name** * is the schema name. The property is populated automatically and becomes editable only after you select an object in the **Object** property.

     * **Object** * is the object whose data to bind to the package.

     * **Installation type** * is how to add data to Creatio when installing the package.

Creatio IDE supports the following **data installation options** :

       * **Installation**. Data is added as part of the first package installation and changed as part of package updates. Universal option. Active by default.
       * **Initial installation**. Data is added as part of the first package installation. Use the option if you install the package using the [WorkspaceConsole utility](https://academy.creatio.com/documents?ver=8.3&id=15207). We do not recommend using the option in other cases.
       * **Update existing**. Data is added as part of the first package installation. Only the installed columns are changed as part of package updates. Installed columns are those that have the **Forced update** checkbox on the **Columns setting** tab selected. For example, use the option when delivering hotfixes.
     * **Package** is the user-made package where you create the schema. The property is populated automatically and non-editable.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Data/8.0/scr_data_properties.png)

4. Select **data to bind to the package** in the data binding page’s workspace.
   1. Select the columns that contain object data on the **Columns setting**
      tab.
   2. Select the records to bind to the package on the **Bound data** tab. Use
      the filter by object name to search for the corresponding data.

5. Click **Save** on the data binding page’s toolbar to save the changes to
   schema properties. Use the `Ctrl+S` hot key to **save the changes**.

- Implement a data binding
