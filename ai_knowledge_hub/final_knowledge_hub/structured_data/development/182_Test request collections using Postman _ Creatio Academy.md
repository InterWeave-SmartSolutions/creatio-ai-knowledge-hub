# Test request collections using Postman | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 337
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/using-postman/working-with-request-collections

## Description

Adding a collection of requests

## Key Concepts

database

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/using-postman/working-with-request-collections)**
(8.3).

Version: 8.0

On this page

Level: intermediate

## Adding a collection of requests​

There are two ways of adding a collection of requests in Postman:

- Click **New** → **Collection** in the **Building blocks** of the **Create
  new** tab.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_Collection_button_Building_blocks.gif)

- In the dropdown menu of the **New** button, click **Collection**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_New_button.png)

- On the **Collections** tab, click **\+ New Collection**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_New_Collection_button.png)

Populate the fields in the new collection window:

Fields of the new request collection window

| Field name | Description | **Name** | The name of the collection. | **Description** | The description of the collection. |
| ---------- | ----------- | -------- | --------------------------- | --------------- | ---------------------------------- |

New collection window

![New collection window](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_CreateCollectionWindow.png)

Click **Create**.

## Adding requests to the collection​

There are two ways of adding a request to a collection in Postman:

- Drag and drop an existing request to the collection.

- Right-click the name of an earlier created collection, then click **Add
  Request**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_AddRequestInCollection.gif)

## Setting up variables for the request collection​

Collections enable setting up common variables and parameters for all requests
that it contains. To set the collection variables:

1. Right-click an earlier created collection.

2. Click **Edit** , then go to the **Variables** tab.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_VariablesSettings.gif)

3. Create the following variables for the collection:

Collection variables

| Variable name | Description | BaseURI | Creatio application URL. | UserName | Creatio application user name. | UserPassword | Creatio application user password. | BPMCSRF | CSRF protection token. | CollectionName | Object collection (database table) name. |
| ------------- | ----------- | ------- | ------------------------ | -------- | ------------------------------ | ------------ | ---------------------------------- | ------- | ---------------------- | -------------- | ---------------------------------------- |

Variable values in the **Initial value** and **Current value** must be
duplicated.

## Executing the collection of requests​

To execute a collection of requests:

1. Click
   ![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_RunCollection_button.png)
   next to the collection name.

2. Click **Run**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_Run_button.png)

3. In the **Run order** block, select requests to run and set their order (1).

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_RequestOrder.png)

4. Select the **Save responses** checkbox (2).

5. Click **Run** (3).

Getting data of the request structure elements and the response:

- Click the request name.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_RequestElements.png)

- Click **View** → **Show Postman Console** or press **Alt+Ctrl+C** on the
  keyboard.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithCollectionRequestsInPostman/scr_PostmanConsole.gif)

Select the needed item.

- Adding a collection of requests
- Adding requests to the collection
- Setting up variables for the request collection
- Executing the collection of requests
