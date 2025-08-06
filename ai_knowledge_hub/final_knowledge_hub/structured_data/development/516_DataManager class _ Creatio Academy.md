# DataManager class | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1122
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/front-end-development/classic-ui/data-operations-front-end/references/datamanager

## Description

DataManager class

## Key Concepts

entity schema, configuration, database, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/front-end-development/classic-ui/data-operations-front-end/references/datamanager)**
(8.3).

Version: 8.0

On this page

Level: intermediate

## DataManager class​

`DataManager` is a singleton class available via the `Terrasoft` global object.
The class provides the `dataStore` repository. You can upload the contents of
one or more database tables to the repository.

    dataStore: {
        /* The DataManagerItem type data collection of the SysModule schema. */
        SysModule: sysModuleCollection,
        /* The DataManagerItem type data collection of the SysModuleEntity schema. */
        SysModuleEntity: sysModuleEntityCollection
    }

Each record of the collection represents the record of the corresponding
database table.

### Properties​

    {Object} dataStore

The data collection repository.

    {String} itemClassName

The record class name. Has the `Terrasoft.DataManagerItem` value.

### Methods​

    {Terrasoft.Collection} select(config, callback, scope)

If `dataStore` does not contain a data collection that has the
`config.entitySchemaName` name, the method builds and executes a database query,
then returns the retrieved data. Otherwise, the method returns the data
collection from `dataStore`.

Parameters

| {Object} config | The configuration object.Configuration object properties | {String} entitySchemaName | The schema name. | {Terrasoft.FilterGroup} filters | The conditions. |
| --------------- | -------------------------------------------------------- | ------------------------- | ---------------- | ------------------------------- | --------------- |

{Function} callback| The callback function.| {Object} scope| The scope of the
callback function.

    {Terrasoft.DataManagerItem} createItem(config, callback, scope)

Creates a new record of the `config.entitySchemaName` type. The record columns
have the `config.columnValues` values.

Parameters

| {Object} config | The configuration object.Configuration object properties | {String} entitySchemaName | The schema name. | {Object} columnValues | The record column values. |
| --------------- | -------------------------------------------------------- | ------------------------- | ---------------- | --------------------- | ------------------------- |

{Function} callback| The callback function.| {Object} scope| The scope of the
callback function.

    {Terrasoft.DataManagerItem} addItem(item)

Adds the `item` record to the schema data collection.

Parameters

| {Terrasoft.DataManagerItem} item | The record to add. |
| -------------------------------- | ------------------ |

    {Terrasoft.DataManagerItem} findItem(entitySchemaName, id)

Returns the record from the data collection of the schema that has the
`entitySchemaName` name and `id` ID.

Parameters

| {String} entitySchemaName | The data collection name. | {String} id | The record ID. |
| ------------------------- | ------------------------- | ----------- | -------------- |

    {Terrasoft.DataManagerItem} remove(item)

Selects the `isDeleted` flag for the `item` record. Once the changes are
recorded, the record will be deleted from the database.

Parameters

| {Terrasoft.DataManagerItem} item | The record to delete. |
| -------------------------------- | --------------------- |

    removeItem(item)

Deletes the record from the schema data collection.

Parameters

| {Terrasoft.DataManagerItem} item | The record to delete. |
| -------------------------------- | --------------------- |

    {Terrasoft.DataManagerItem} update(config, callback, scope)

Updates the record that has the `config.primaryColumnValue` primary column value
with the values from `config.columnValues`.

Parameters

| {Object} config | The configuration object.Configuration object properties | {String} entitySchemaName | The schema name. | {String} primaryColumnValue | The primary column value. | {Mixed} columnValues | The column values. |
| --------------- | -------------------------------------------------------- | ------------------------- | ---------------- | --------------------------- | ------------------------- | -------------------- | ------------------ |

{Function} callback| The callback function.| {Object} scope| The scope of the
callback function.

    {Terrasoft.DataManagerItem} discardItem(item)

Discards the changes to the `item` record made as part of the current
`DataManager` session.

Parameters

| {Terrasoft.DataManagerItem} item | The record, changes to which to discard. |
| -------------------------------- | ---------------------------------------- |

    {Object} save(config, callback, scope)

Saves the data collections of the schemas specified in
`config.entitySchemaNames` to the database.

Parameters

| {Object} config | The configuration object.Configuration object properties | {String[]} entitySchemaName | The name of the schema to save. Leave empty to save the data collections of all schemas. |
| --------------- | -------------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------- |

{Function} callback| The callback function.| {Object} scope| The scope of the
callback function.

## DataManagerItem class​

### Properties​

    {Terrasoft.BaseViewMode} viewModel

The object projection of the database record.

### Methods​

    setColumnValue(columnName, columnValue)

Assigns the new `columnValue` value to the column that has the `columnName`
name.

Parameters

| {String} columnName | The column name. | {String} columnValue | The column value. |
| ------------------- | ---------------- | -------------------- | ----------------- |

    {Mixed} getColumnValue(columnName)

Returns the value of the column that has the `columnName` name.

Parameters

| {String} columnName | The column name. |
| ------------------- | ---------------- |

    {Object} getValues()

Returns the values of all record columns.

    remove()

Selects the `isDeleted` flag for the record.

    discard()

Discards the changes to the record made as part of the current `DataManager`
session.

    {Object} save(callback, scope)

Records the changes in the database.

Parameters

| callback | The callback function. | scope | The scope of the callback function. |
| -------- | ---------------------- | ----- | ----------------------------------- |

    {Boolean} getIsNew()

Returns the flag that marks the record as new.

    {Boolean} getIsChanged()

Returns the flag that marks the record as changed.

Use examples

Retrieve the records from the Contact table

    /* Define the configuration object. */
    var config = {
        /* The entity schema name. */
        entitySchemaName: "Contact",
        /* Exclude duplicates from the resulting dataset. */
        isDistinct: true
    };
    /* Retrieve the data. */
    Terrasoft.DataManager.select(config, function (collection) {
        /* Save the retrieved records to the local repository. */
        collection.each(function (item) {
            Terrasoft.DataManager.addItem(item);
        });
    }, this);

Add a new record to the DataManager object

    /* Define the configuration object. */
    var config = {
        /* The entity schema name. */
        entitySchemaName: "Contact",
        /* The column values. */
        columnValues: {
            Id: "00000000-0000-0000-0000-000000000001",
            Name: "Name1"
        }
    };
    /* Create a new record. */
    Terrasoft.DataManager.createItem(config, function (item) {
        Terrasoft.DataManager.addItem(item);
    }, this);

Retrieve the record and change the column value

    /* Retrieve the record. */
    var item = Terrasoft.DataManager.findItem("Contact",
         "00000000-0000-0000-0000-000000000001");
    /* Assign the new "Name2" value to the Name column. */
    item.setColumnValue("Name", "Name2");

Delete the record from DataManager

    /* Define the configuration object. */
    var config = {
        /* The entity schema name. */
        entitySchemaName: "Contact",
        /* The primary column value. */
        primaryColumnValue: "00000000-0000-0000-0000-000000000001"
    };
    /* Select the isDeleted flag for the item record. */
    Terrasoft.DataManager.remove(config, function () {
    }, this);

Discard the changes made as part of the current DataManager session

    /* Retrieve the record. */
    var item = Terrasoft.DataManager.findItem("Contact",
         "00000000-0000-0000-0000-000000000001");
    /* Discard the changes to the record. */
    Terrasoft.DataManager.discardItem(item);

Record the changes in the database

    /* Define the configuration object. */
    var config = {
        /* The entity schema name. */
        entitySchemaNames: ["Contact"]
    };
    /* Save the changes in the database. */
    Terrasoft.DataManager.save(config, function () {
    }, this);

- DataManager class
  - Properties
  - Methods
- DataManagerItem class
  - Properties
  - Methods
