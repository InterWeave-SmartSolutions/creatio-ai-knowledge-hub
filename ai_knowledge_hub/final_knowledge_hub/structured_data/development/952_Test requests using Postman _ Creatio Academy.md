# Test requests using Postman | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 269 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/integrations-and-api/using-postman/working-with-requests

## Description

Adding a request

## Key Concepts

integration, odata

## Use Cases

third-party integration, data synchronization, system connectivity

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/using-postman/working-with-requests)**
(8.3).

Version: 8.1

On this page

Level: intermediate

## Adding a request​

There are two ways of adding a request in Postman:

- Open the **Create New** tab, then in the **Building blocks** click **New** →
  **Request**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_New_button_Building_blocks.gif)

- In the dropdown menu of the **New** button, click **Request**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_New_button_Request.png)

Populate the fields in the new request window:

New request fields

| Field name | Description | **Request name** | The name of the new request. | **Request description (Optional)** | Additional information about the request (optional). | **Search for a collection or folder** | Search for an earlier created collection of requests, or create a new one. |
| ---------- | ----------- | ---------------- | ---------------------------- | ---------------------------------- | ---------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------- |

New request window

![New request window](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_CreateRequestWindow.png)

Populate the fields and click **Save**. The button becomes active only after the
**Search for a collection or folder** field is populated.

## Setting up the request​

To set up the request:

1. Select the request method.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/src_Method_Choosing.png)

2. Enter the request string.

3. Set the data format of the request. Go to the **Body** tab, select the
   "`raw`" option and `JSON` type.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_Request_Type.gif)

4. Populate the request body for `POST` and `PATCH` methods.

5. Go to the **Headers** tab and set the headers.

Headers

         Accept: application/json
         Content-Type: application/json; charset=utf-8
         ForceUseSession: true


## Executing the request​

To execute a request, click **Send**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_Send_button.png)

## Saving the request​

To save a request, click **Save**.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/WorkWithRequestsInPostman/scr_Save_button.png)

We recommend using Postman for testing queries when developing integrations with
Creatio via [OData](https://academy.creatio.com/documents?ver=8.1&id=15431).

- Adding a request
- Setting up the request
- Executing the request
- Saving the request
