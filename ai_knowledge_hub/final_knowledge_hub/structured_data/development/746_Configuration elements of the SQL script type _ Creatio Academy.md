# Configuration elements of the SQL script type | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 716
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/sql-script

## Description

Configuration element of the SQL script type is an entity that lets you
implement database queries written in SQL. The purpose of an SQL script is to
create database objects, for example, views, procedures, functions, or execute
other Creatio database queries.

## Key Concepts

configuration, section, sql, database, operation, system setting, package,
notification

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

**Configuration element** of the **SQL script** type is an entity that lets you
implement database queries written in SQL. The **purpose** of an SQL script is
to create database objects, for example, views, procedures, functions, or
execute other Creatio database queries.

The item of the **Add** drop-down list in the toolbar of the **Configuration**
section workspace represents the configuration element of the **SQL script**
type you can add in Creatio IDE.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SqlScript/8.0/scr_AddList.png)

Learn more about configuration element types:
[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-12).

The **SQL script** item in the **Type** drop-down list in the toolbar of the
**Configuration** section workspace represents the configuration element of the
**SQL script** type.

View the SQL script **type** in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SqlScript/8.0/scr_TypeList.png)

Learn more about configuration element types:
[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-14).

## Implement an SQL script​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.3&id=15121) to add the
   configuration element.

2. Click **Add** → **SQL script** on the section list toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SqlScript/8.0/scr_AddList.png)

3. Fill out the configuration element properties in the Script Designer.

Fill out the **main properties** of the configuration element:

     * **Code** * is the schema name. Name the SQL script using the **template** below.

       * Template of the SQL script name
       * Example of the SQL script name

    [Prefix][Operation][Object][DBMS];


    UsrUpdateActivityDateMSSQL;

`[Prefix]` is the prefix of the configuration element name (by default, `Usr`)
specified in the **Prefix for object name** (`SchemaNamePrefix` code) system
setting. Can contain alphanumeric characters. Creatio checks whether the prefix
exists and matches the system setting when you go to a different configuration
element property. If the prefix does not exist or does not match, Creatio sends
a corresponding user notification.

`[Operation]` is the operation the SQL script executes Available values:
`Insert`, `Update`, `Delete`. Optional for SQL scripts that create objects (the
`Create` value).

`[Object]`\* is the object with which the SQL script interacts.

`[DBMS]`\* is the database type for which you are developing the SQL script.
Must match the **DBMS type** property value of the SQL script.

     * **DBMS type** * is the database type for which you are developing the SQL script. Available values: "MSSql," "Oracle," "PostgreSql." Creatio in the cloud supports PostgreSQL only.

     * **Installation type** * is the script execution order when installing the package.

Available **values** :

       * Select "BeforePackage" to execute the SQL script before the package installation.
       * Select "AfterPackage" to execute the SQL script after the package installation.
       * Select "AfterSchemaData" to execute the SQL script after the package data (configuration elements of the **Data** type) installation.
       * Select "UninstallApp" to execute the SQL script when deleting the package to which the script is bound.
     * **Package** is the user-made package where you create the configuration element. The property is populated automatically and non-editable.

     * **Backward compatible** specifies whether the script is backward compatible. Learn more: [Backward compatible SQL scripts](https://academy.creatio.com/documents?ver=8.3&id=15109).

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SqlScript/8.0.3/scr_sql_script_properties.png)

Click **Apply** to apply the properties.

The **properties area** of the Script Designer lets you:

     * edit the main configuration element properties (![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png) button)
     * specify the additional configuration element properties (![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png) button)

The **additional properties** of the configuration element are as follows:

     * **Depends on SQL Scripts**. Lets you select the SQL scripts to execute before executing the current script.
     * **Dependent SQL Scripts**. Contains the SQL scripts to execute after executing the current script. The property is populated automatically and non-editable.

To **execute SQL scripts in a set order** :

     1. Select the corresponding installation type (the value of the **Installation type** property).
     2. Set the needed dependencies between scripts (**Depends on SQL Scripts** and **Dependent SQL Scripts** properties).

4. Click **Validation** on the Script Designer’s toolbar to validate the syntax
   of the SQL script.

5. Click **Save** on the Script Designer’s toolbar to save the changes to
   configuration element properties.

## Use hot keys​

To display the index of available hot keys:

1. **Open the Script Designer**.
2. **Click**
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_Info_Button.png)
   on the toolbar.

| Hot key | Action | Ctrl+A | Select all | Ctrl+Z | Undo | Shift+Ctrl+Z | Redo | Ctrl+F | Find | F3  | Find next | Shift+F3 | Find previous | Shift+Ctrl+F | Replace | Shift+Ctrl+R | Replace all | Ctrl+Y | Delete line | Alt+Left | Go to line start | Alt+Right | Go to line end | Alt+G | Jump to line | F11 | Fullscreen code editor | Esc | Exit fullscreen mode | Ctrl+Space | Call autocomplete | Ctrl+S | Save the changes |
| ------- | ------ | ------ | ---------- | ------ | ---- | ------------ | ---- | ------ | ---- | --- | --------- | -------- | ------------- | ------------ | ------- | ------------ | ----------- | ------ | ----------- | -------- | ---------------- | --------- | -------------- | ----- | ------------ | --- | ---------------------- | --- | -------------------- | ---------- | ----------------- | ------ | ---------------- |

- Implement an SQL script
- Use hot keys
