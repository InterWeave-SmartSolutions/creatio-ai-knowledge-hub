# Open a Classic UI page from a custom request handler | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1656
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/open-a-page-from-a-custom-handler/examples/open-a-record-page

## Description

To implement the example:

## Key Concepts

business process, freedom ui, classic ui, section, lookup, operation, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/open-a-page-from-a-custom-handler/examples/open-a-record-page)**
(8.3).

Version: 8.0

On this page

Level: intermediate

To implement the example:

1. Set up the page UI. Read more >>>
2. Set up how to open Classic UI pages. Read more >>>

Example

Add the following buttons to the custom request page:

- **Edit event**. Must open the "Networking Day" event page.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/OpenAClassicUIPage/8.0/scr_result.gif)

- **Create FAQ**. Must open the new knowledge base page that has "New FAQ" name
  and "FAQ" type.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/OpenAClassicUIPage/8.0/scr_result_01.gif)

## 1\. Set up the page UI​

1. **Create an app** based on the **Records & business processes** template.
   Instructions:
   [Create an app manually](https://academy.creatio.com/documents?ver=8.0&id=2377&anchor=title-2232-6)
   (user documentation).

For this example, create a **Requests** app.

2. **Open the form page**.

For this example, open the **Requests form page**.

3. **Add a button**.

For this example, add the following buttons:

     * button that opens the "Networking Day" event page
     * button that opens the new knowledge base page

To do this:

     1. Add a **Button** type component to the toolbar of the Freedom UI Designer.

     2. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png) and fill out the button properties.

| Element | Property | Property value | Button that opens the "Networking Day" event page | Title | Edit event | Button that opens the new knowledge base page | Title | Create FAQ | Style | Primary |
| ------- | -------- | -------------- | ------------------------------------------------- | ----- | ---------- | --------------------------------------------- | ----- | ---------- | ----- | ------- |

4. **Save the changes**.

## 2\. Set up how to open Classic UI pages​

Configure the business logic in the Client Module Designer. For this example,
set up how to open Classic UI pages.

1. **Open the source code** of the Freedom UI page. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_SourceCode_button.png).

2. **Add the dependencies**. To do this, add `@creatio-devkit/common` library as
   a dependency. The library includes the `HandlerChainService` service that
   opens pages.

AMD module dependencies

         /* Declare the AMD module. */
         define("UsrAppRequests_FormPage", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
             return {
                 ...
             }
         });


3. **Set up how to handle the action** executed on button click.
   1. Go to the `viewConfigDiff` schema section → `EditEventButton` element.
   2. Bind the sending of the custom `usr.EditEventRequest` request to the
      `clicked` button event.
   3. Go to the `CreateFaqButton` element.
   4. Bind the sending of the custom `usr.CreateFaqRequest` request to the
      `clicked` button event.

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        /* Button that opens the "Networking Day" event page. */
        {
            "operation": "insert",
            "name": "EditEventButton",
            "values": {
                ...,
                "clicked": {
                    /* Bind the sending of the custom request to the "clicked" button event. */
                    "request": "usr.EditEventRequest"
                }
            },
            ...
        },
        /* Button that opens the new knowledge base page. */
        {
            "operation": "insert",
            "name": "CreateFaqButton",
            "values": {
                ...,
                "clicked": {
                    /* Bind the sending of the custom request to the "clicked" button event. */
                    "request": "usr.CreateFaqRequest"
                }
            },
            ...
        }
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

4. **Implement the custom request handlers**.
   1. Go to the `handlers` schema section.

   2. Implement the `usr.EditEventRequest` custom request handler.
      1. Retrieve the instance of the HTTP client from `@creatio-devkit/common`.
      2. Send the `crt.UpdateRecordRequest` base request handler that opens the
         "Networking Day" event page using the specified ID. View the ID of the
         "Networking Day" event page in the browser address bar. For this
         example, the ID is "60cb269d-7447-4347-b657-63030cbd810e."

   3. Implement the `usr.CreateFaqRequest` request handler.
      1. Retrieve the instance of the HTTP client from `@creatio-devkit/common`.
      2. Send the `crt.CreateRecordRequest` base request handler that opens the
         new knowledge base page. Both Freedom UI and Classic UI open record
         pages in a similar way. When Creatio adds a record, you can pass the
         needed column values. Fill out the **Name** and **Type** fields using
         the "New FAQ" and "FAQ," respectively. View the ID of the FAQ type in
         the **Knowledge base article types** lookup. For this example, the ID
         is "80bb327e-f36b-1410-a29d-001d60e938c6."

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "usr.EditEventRequest",
            /* The implementation of the custom request handler. */
            handler: async (request, next) => {
                /* Retrieve the instance of the HTTP client from "@creatio-devkit/common." */
                const handlerChain = sdk.HandlerChainService.instance;
                /* Send the base request handler to open the event page that has the specified ID. */
                await handlerChain.process({
                    type: 'crt.UpdateRecordRequest',
                    entityName: 'Event',
                    recordId: '60cb269d-7447-4347-b657-63030cbd810e',
                    $context: request.$context,
                    scopes: [...request.scopes]
                });
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        },
        {
            request: "usr.CreateFaqRequest",
            /* The implementation of the custom request handler. */
            handler: async (request, next) => {
                /* Retrieve the instance of the HTTP client from "@creatio-devkit/common." */
                const handlerChain = sdk.HandlerChainService.instance;
                /* Send the base request handler to open the new knowledge base page. Fill out the "Name" and "Type" fields using the specified values. */
                await handlerChain.process({
                    type: 'crt.CreateRecordRequest',
                    entityName: 'KnowledgeBase',
                    defaultValues: [
                        {
                            attributeName: 'Name',
                            value: 'New FAQ'
                        },
                        {
                            attributeName: 'Type',
                            value: '80bb327e-f36b-1410-a29d-001d60e938c6'
                        }
                    ],
                    $context: request.$context,
                    scopes: [...request.scopes]
                });
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        }
    ]/**SCHEMA_HANDLERS*/,

5. **Save the changes**.

## View the result​

To view the outcome of the example that **opens the "Networking Day" event
page** :

1. **Open the Requests section**.
2. **Create a request**.
3. Click **Edit event**.

**As a result** , Creatio will open the "Networking Day" event page whose ID is
"60cb269d-7447-4347-b657-63030cbd810e."
[View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15365&anchor=view-result-1)

To view the outcome of the example that **opens the new knowledge base page and
populates fields** :

1. **Open the Requests section**.
2. **Create a request** that has an arbitrary name. For example, "Vacation."
3. Click **Create FAQ**.

**As a result** , Creatio will open the new knowledge base page and populate the
**Name** and **Type** fields using "New FAQ" and "FAQ," respectively.
[View the result >>>](https://academy.creatio.com/documents?ver=8.01&id=15365&anchor=view-result-2)

## Source code​

UsrAppRequests_FormPage

    /* Declare the AMD module. */
    define("UsrAppRequests_FormPage", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
        return {
            viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
                /* Button that opens the "Networking Day" event page. */
                {
                    "operation": "insert",
                    "name": "EditEventButton",
                    "values": {
                        "type": "crt.Button",
                        "caption": "#ResourceString(EditEventButton_caption)#",
                        "color": "default",
                        "disabled": false,
                        "clicked": {
                            /* Bind the sending of the custom request to the "clicked" button event. */
                            "request": "usr.EditEventRequest"
                        },
                        "iconPosition": "only-text"
                    },
                    "parentName": "ActionButtonsContainer",
                    "propertyName": "items",
                    "index": 0
                },
                /* Button that opens the new knowledge base page. */
                {
                    "operation": "insert",
                    "name": "CreateFaqButton",
                    "values": {
                        "type": "crt.Button",
                        "caption": "#ResourceString(CreateFaqButton_caption)#",
                        "color": "primary",
                        "disabled": false,
                        "clicked": {
                            /* Bind the sending of the custom request to the "clicked" button event. */
                            "request": "usr.CreateFaqRequest"
                        },
                        "iconPosition": "only-text"
                    },
                    "parentName": "ActionButtonsContainer",
                    "propertyName": "items",
                    "index": 1
                },
                {
                    "operation": "insert",
                    "name": "UsrName",
                    "values": {
                        "layoutConfig": {
                            "column": 1,
                            "row": 1,
                            "colSpan": 1,
                            "rowSpan": 1
                        },
                        "type": "crt.Input",
                        "label": "$Resources.Strings.UsrName",
                        "control": "$UsrName"
                    },
                    "parentName": "LeftAreaProfileContainer",
                    "propertyName": "items",
                    "index": 0
                }
            ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
            viewModelConfig: /**SCHEMA_VIEW_MODEL_CONFIG*/{
                "attributes": {
                    "UsrName": {
                        "modelConfig": {
                            "path": "PDS.UsrName"
                        }
                    },
                    "Id": {
                        "modelConfig": {
                            "path": "PDS.Id"
                        }
                    }
                }
            }/**SCHEMA_VIEW_MODEL_CONFIG*/,
            modelConfig: /**SCHEMA_MODEL_CONFIG*/{
                "dataSources": {
                    "PDS": {
                        "type": "crt.EntityDataSource",
                        "config": {
                            "entitySchemaName": "UsrAppRequests"
                        }
                    }
                }
            }/**SCHEMA_MODEL_CONFIG*/,
            handlers: /**SCHEMA_HANDLERS*/[
                {
                    request: "usr.EditEventRequest",
                    /* The implementation of the custom request handler. */
                    handler: async (request, next) => {
                        /* Retrieve the instance of the HTTP client from "@creatio-devkit/common." */
                        const handlerChain = sdk.HandlerChainService.instance;
                        /* Send the base request handler to open the event page that has the specified ID. */
                        await handlerChain.process({
                            type: 'crt.UpdateRecordRequest',
                            entityName: 'Event',
                            recordId: '60cb269d-7447-4347-b657-63030cbd810e',
                            $context: request.$context,
                            scopes: [...request.scopes]
                        });
                        /* Call the next handler if it exists and return its result. */
                        return next?.handle(request);
                    }
                },
                {
                    request: "usr.CreateFaqRequest",
                    /* The implementation of the custom request handler. */
                    handler: async (request, next) => {
                        /* Retrieve the instance of the HTTP client from "@creatio-devkit/common." */
                        const handlerChain = sdk.HandlerChainService.instance;
                        /* Send the base request handler to open the new knowledge base page. Fill out the "Name" and "Type" fields using the specified values. */
                        await handlerChain.process({
                            type: 'crt.CreateRecordRequest',
                            entityName: 'KnowledgeBase',
                            defaultValues: [
                                {
                                    attributeName: 'Name',
                                    value: 'New FAQ'
                                },
                                {
                                    attributeName: 'Type',
                                    value: '80bb327e-f36b-1410-a29d-001d60e938c6'
                                }
                            ],
                            $context: request.$context,
                            scopes: [...request.scopes]
                        });
                        /* Call the next handler if it exists and return its result. */
                        return next?.handle(request);
                    }
                }
            ]/**SCHEMA_HANDLERS*/,
            converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
            validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
        };
    });

---

## Resources​

[Package with example implementation](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/OpenAClassicUIPage/8.0/AppRequests_2024-07-17_11.51.17.zip)

- 1\. Set up the page UI
- 2\. Set up how to open Classic UI pages
- View the result
- Source code
- Resources
