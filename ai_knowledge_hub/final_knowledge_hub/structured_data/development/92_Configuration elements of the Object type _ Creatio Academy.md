# Configuration elements of the Object type | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 2204 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/object

## Description

A configuration element of the Object type is a business entity that lets you
declare a new ORM model class on the server core level. If you create an object,
a new table with the same name and the same set of columns as the object is
created on the database level. In other words, a Creatio object is a system view
of a physical database table in most cases. The purpose of the object is to
enable back-end Creatio development.

## Key Concepts

entity schema, configuration, section, lookup, sql, database, system setting,
package, contact, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

A configuration element of the **Object** type is a business entity that lets
you declare a new ORM model class on the server core level. If you create an
object, a new table with the same name and the same set of columns as the object
is created on the database level. In other words, a Creatio object is a system
view of a physical database table in most cases. The **purpose** of the object
is to enable back-end Creatio development.

The items of the **Add** drop-down list in the toolbar of the **Configuration**
section workspace represent the object types you can add in Creatio IDE.

View the object **types** in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_AddList.png)

The **Object** schema type in the **Type** drop-down list in the toolbar of the
**Configuration** section workspace represents the object. The object schema
describes the list of object columns, indexes, and methods. Creatio platform
does not limit the number of object columns. The number of object columns is
limited by the maximum number of columns in the tables of the client database.

View the **type** of the object schema in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_TypeList.png)

## Implement an object​

The **Object** schema **type** represents the object.

To implement an object:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add an object schema**. To do this, click **Add** → **Object** in the
   section list toolbar. This opens the Object Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_add_object.png)

4. **Fill out the schema properties**.

| Property | Property description | Code\* | The schema name. Starts with the prefix. Learn more: [Manage configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-6). Can contain Latin characters and digits. The object name can contain up to and including 128 characters. Oracle databases version 12.2 and earlier do not accept objects that have names longer than 30 characters. | Title\* | The localizable schema title. The title of the configuration element schema is generated automatically and matches the value of the **Code** property without the prefix. | Package | The user-made package where you create the schema. The property is populated automatically and non-editable. | Description | The localizable schema description |
| -------- | -------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ | ----------- | ---------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_object_properties.png)

5. **Select the parent object** in the Object Designer.

For the object to **inherit the functionality** of a different object, select
the schema of the object to inherit in the **Parent object** property’s
drop-down list. For example, to inherit the functionality of the `BaseEntity`
object’s base schema, specify the `BaseEntity` schema as the parent object.
Creatio adds columns inherited from the parent object to the **Inherited
columns** property of the object schema automatically.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_BaseEntity_props.png)

6. **Specify the object ID** if the **Parent object** property contains a custom
   object. Creatio populates the **Id** property automatically if the **Parent
   object** property contains a base object.
   [Read more >>>](https://academy.creatio.com/documents?ver=8.3&id=15107&anchor=title-3028-11)

7. **Add an object index**.
   [Read more >>>](https://academy.creatio.com/documents?ver=8.3&id=15107&anchor=title-3028-13)

8. **Set up cascade connection** for **Lookup** type columns (optional).
   [Read more >>>](https://academy.creatio.com/documents?ver=8.3&id=15107&anchor=title-3028-14)

9. **Publish the schema**. Creatio alerts users that an action could degrade
   environment performance temporarily. Therefore, we recommend executing such
   actions during non-business hours. Out of the box, those messages are enabled
   only for environments whose **Environment type** (`EnvironmentType` code)
   system setting is set to "Production."

If you need to generate the static content, update the database structure
**without configuration compilation** , click **Save and publish**. This
accelerates the development of objects and replacing objects.

If you need to generate the static content, update the database structure
**including configuration compilation** , click **Actions** → **Publish and
compile**. The object compilation on publishing is required if the embedded
process of the object was saved while editing but not published in the Process
Designer.

### Specify the object ID for custom parent object​

Since a Creatio object is a database table view, it must contain the ID column.
**Id** is the system column that serves as the primary key in the database
table.

To specify the object ID for custom parent object:

1. **Click**
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   → **Other** → **Unique identifier** in the properties area of the **Columns**
   node’s context menu.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_add_unique_identifier.png)

2. **Fill out the column properties**.

Property| Property description| Code*| The column name. Starts with the prefix.
Learn more:
[Manage configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-6).
Can contain Latin characters, digits, special characters. Make sure that the
**Code** property is different from the **Code** of column's object. Otherwise,
Creatio will display an error message when you attempt to publish the object.|
Title*| The localizable column title.| Data type| The column data type. Creatio
populates the property automatically depending on the column type selected when
adding a column. This is a non-editable field.| Description| The localizable
column description.| | Required| Specify for the required columns. Select "Yes"
since the column of the **Unique identifier** type is required for the object.
If you attempt to save the object schema without the column of the **Unique
identifier** type, Creatio displays a corresponding message.| Default value| The
default column value.
[Read more >>>](https://academy.creatio.com/documents?ver=8.3&id=15107&anchor=title-3028-12).|
Usage mode| Advanced.Creatio IDE supports the following column **usage modes** :
_ **General** is the standard column mode in the app. _ **Advanced**. Columns
are displayed in the configuration and are available in the app. \* **None**.
Columns are displayed as system columns in the configuration and are not
available in the app.  
---|---

### Specify the default value for the column of the Unique identifier type​

1. **Click**
   ![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateEntitySchema(7.17)/scr_edit_button.png>)
   in the **Default value** property.

2. **Fill out the default value properties.**

| Property | Property value | Default value type | System variable | System variable | New Id |
| -------- | -------------- | ------------------ | --------------- | --------------- | ------ |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_default_column_value.png)

### Add an object index​

Besides columns, Creatio IDE lets you add indexes to the object. Indexes are
created automatically in the database table when you publish an object.

You can add an object index in the following **ways** :

- **Single column index**. To do this, select the **Indexed** checkbox in the
  **Behavior** property block. Creatio indexes lookup columns by default.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_Behavior.png)

- **Composite index**. To do this, follow the instructions below.

To add a composite object index:

1. **Click**
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   in the properties area of the **Indexes** node’s context menu.

2. **Fill out the index properties**.

| Property | Property value | Code\* | The schema name. | Unique | Select the checkbox to enable integrity constraints for index columns, i. e., remove the possibility of adding repeating value combinations. | Index Columns | Select the columns to add to the index. To do this, click **Add** in the **Index Columns** property block, select an object column, and specify the sorting order. |
| -------- | -------------- | ------ | ---------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_index_props.png)

### Set up the cascade connection​

1. **Add a Lookup type column** (optional). To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   → **Lookup** in the context menu of the **Columns** node.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_add_lookup.png)

2. **Move to the Data source property block**.

3. **Select or clear the Do not control integrity checkbox** based on your
   business goals.

4. **Select the option** in the **On lookup value deletion** item block.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_data_source_lookup.png)

For example, set up a cascade connection to the **Contact** object connected to
the **Account** object via the **AccountId** lookup column. To do this, select
**Account** in the **Lookup** field.

The cascade connection **setup options** are as follows:

- If you need to **delete the account without deleting the contacts connected to
  the account** , select the **Do not control integrity** checkbox.
- If you need to **confirm deletion the account without deleting the contacts
  connected to the account** , do not select the **Do not control integrity**
  checkbox and select the **Block deletion if there are connected records in
  current object with this value** item, Creatio checks for connected contacts.
  If Creatio detects them, it displays a warning message asking you to confirm
  the deletion.
- If you need to **delete both the account and connected contacts** , do not
  select the **Do not control integrity** checkbox and select the **Delete
  records from current object with this value** option.

## Implement a replacing object​

The schema of the **Replacing object** type represents the replacing object.
Learn more:
[Replace configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15105).

To implement a replacing object:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Set up the package dependencies**. You must add the package that contains
   the replaced object to the dependency list.

4. **Add a replacing object schema.** To do this, click **Add** → **Replacing
   object** on the section list toolbar. This opens the Object Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_add_replacing_object.png)

5. **Select the parent object** to replace the functionality in the **Parent
   object** property’s drop-down list . For example, to replace the
   functionality of the `BaseEntity` object’s base schema, specify the
   `BaseEntity` schema as the parent object. Creatio adds columns inherited from
   the parent object to the **Inherited columns** property of the object schema
   automatically. After you select the parent object, Creatio populates other
   object properties automatically.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_replacing_object_properties.png)

6. **Implement the functionality** that distinguishes the replacing object from
   the replaced object.

7. **Publish the schema**. Creatio alerts users that an action could degrade
   environment performance temporarily. Therefore, we recommend executing such
   actions during non-business hours. Out of the box, those messages are enabled
   only for environments whose **Environment type** (`EnvironmentType` code)
   system setting is set to "Production."

If you need to generate the static content, update the database structure
without configuration compilation, click **Save and publish**. This accelerates
the development of objects and replacing objects.

If you need to generate the static content, update the database structure
including configuration compilation, click **Actions** → **Publish and
compile**. The object compilation on publishing is required if the embedded
process of the object was saved while editing but not published in the Process
Design.

## Deactivate object records​

Creatio lets you deactivate object records to exclude them from the business
logic. For example, this can be useful if the data is outdated and no longer
used. You can deactivate records of any object.

To deactivate object records:

1. **Open the schema of the object** whose records to deactivate.

2. **Select the Allow records deactivation checkbox** in the **Behavior**
   property block.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_records_deactivation.png)

3. **Publish the schema**. Creatio alerts users that an action could degrade
   environment performance temporarily. Therefore, we recommend executing such
   actions during non-business hours. Out of the box, those messages are enabled
   only for environments whose **Environment type** (`EnvironmentType` code)
   system setting is set to "Production."

Creatio can **filter inactive records** automatically for certain UI elements.

The automatic record filtering is **available** for the following UI elements:

- drop-down list
- lookup value selection box
- quick filter

The automatic record filtering is **not available** for the following UI
elements:

- lookup content page
- section
- advanced filter

The `UseRecordDeactivation` parameter of the `EntitySchemaQuery` class lets you
**manage the filtering of inactive records**. The default value is `false`. If
you set the `UseRecordDeactivation` parameter to `true`, the select query to the
object that has record deactivation enabled will contain the filter that
excludes inactive record.

View the example that deactivates records in the front-end below.

Example that deactivates records (front-end)

    var esq = Ext.create("Terrasoft.EntitySchemaQuery", {
        rootSchemaName: "MyCustomLookup",
        useRecordDeactivation: true,
    });

View the example that deactivates records in the back-end below.

Example that deactivates records (back-end)

    var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "ContactType") {
        UseRecordDeactivation = true
    };
    esq.PrimaryQueryColumn.IsAlwaysSelect = true;

View the resulting SQL query below.

Example of the SQL query

    SELECT [ContactType].[Id] [Id]
    FROM [dbo].[ContactType] [ContactType] WITH(NOLOCK)
    WHERE [ContactType].[RecordInactive] = 0

## Hide rarely used objects​

You can hide rarely used objects in Studio Creatio. To do this:

1. **Open the schema of the object** to hide.

2. **Mark the object as hidden**. To do this, select the **Show in advanced mode
   only** checkbox in the **Behavior** property block.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_hidden_object.png)

3. **Publish the schema**. Creatio alerts users that an action could degrade
   environment performance temporarily. Therefore, we recommend executing such
   actions during non-business hours. Out of the box, those messages are enabled
   only for environments whose **Environment type** (`EnvironmentType` code)
   system setting is set to "Production."

To **view hidden objects** , turn off the `IsAdvancedObjectDisplayModeDisabled`
feature. Instructions:
[Manage the status of an additional feature](https://academy.creatio.com/documents?ver=8.3&id=15631&anchor=title-3459-1).

## Update record fields automatically​

Creatio updates fields on an open form page automatically without the need to
refresh the page.
[Read more >>>](https://academy.creatio.com/documents?ver=8.3&id=15379&anchor=title-2397-1)

This functionality is enabled for fields of directly linked records out of the
box. To enable the functionality for record fields:

1. **Open the schema of the object** whose records to update.

2. **Enable the functionality**. To do this, select the **Enable live data
   update** checkbox in the **Behavior** property block.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Object/8.0/scr_records_updating.png)

3. **Publish the schema**. Creatio alerts users that an action could degrade
   environment performance temporarily. Therefore, we recommend executing such
   actions during non-business hours. Out of the box, those messages are enabled
   only for environments whose **Environment type** (`EnvironmentType` code)
   system setting is set to "Production."

---

## See also​

[Creatio IDE overview](https://academy.creatio.com/documents?ver=8.3&id=15101)

[Replace configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15105)

---

## Resources​

[Back-end development](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/back-end-development)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/e-learning/development-creatio-platform)

- Implement an object
  - Specify the object ID for custom parent object
  - Specify the default value for the column of the Unique identifier type
  - Add an object index
  - Set up the cascade connection
- Implement a replacing object
- Deactivate object records
- Hide rarely used objects
- Update record fields automatically
- See also
- Resources
- E-learning courses
