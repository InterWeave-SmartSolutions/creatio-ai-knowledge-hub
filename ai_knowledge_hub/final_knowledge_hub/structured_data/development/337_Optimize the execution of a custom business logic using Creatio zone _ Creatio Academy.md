# Optimize the execution of a custom business logic using Creatio zone | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 2018
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/creatio-zone/examples/execute-custom-code-outside-of-creatio-zone

## Description

To implement the example:

## Key Concepts

business process, freedom ui, section, web service, operation, package, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

To implement the example:

1. Set up the page UI. Read more >>>
2. Implement the execution of business logic using Creatio zone. Read more >>>

Example

Add the following buttons to the custom request page:

- **Open contacts**. Must open the **Contacts** section.

- **Show emails**. Must call the `{JSON} Placeholder` external web service that
  retrieves emails of post comments.
  - Creatio lets you switch between pages regardless of whether the request to
    the web service is complete or still in progress.

![](https://academy.creatio.com/docs/sites/academy_en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioZone/8.1/scr_result.gif)

    * Creatio blocks switching between pages while the request to the web service is still in progress.

![](https://academy.creatio.com/docs/sites/academy_en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreatioZone/8.1/scr_result_01.gif)

## 1\. Set up the page UI​

1. **Create an app** based on the **Records & business processes** template.
   Instructions:
   [Create an app manually](https://academy.creatio.com/documents?ver=8.3&id=2377&anchor=title-2232-6)
   (user documentation).

For this example, create a **Requests** app.

2. **Open the form page** in the Freedom UI Designer.

For this example, open the **Requests form page**.

3. **Add a button**.

For this example, add the following buttons:

     * button that calls the [{JSON} Placeholder](https://jsonplaceholder.typicode.com/posts) external web service from the request page
     * button that opens the **Contacts** section

To do this:

     1. Add a **Button** type component to the toolbar of the Freedom UI Designer.

     2. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png) and fill out the button properties.

| Element | Property | Property value | Button that calls the `{JSON} Placeholder` external web service from the request page | Title | Show emails | Button that opens the **Contacts** section | Title | Open contacts | Style | Primary |
| ------- | -------- | -------------- | ------------------------------------------------------------------------------------- | ----- | ----------- | ------------------------------------------ | ----- | ------------- | ----- | ------- |

4. **Save the changes**.

## 2\. Implement the execution of business logic using Creatio zone​

1. **Open the source code** of the Freedom UI page. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_SourceCode_button.png).

2. **Enable the** `CrtZoneService` **service** that optimizes the execution of
   custom business logic using Creatio zone. To do this, add
   `@creatio-devkit/common` to the AMD module as a dependency.

AMD module dependencies

         /* Declare the AMD module. */
         define("UsrRequests_FormPage", /**SCHEMA_DEPS*/["@creatio-devkit/common"] /**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
                 ...
             };
         );


3. **Set up how to handle the action** executed on button click.
   1. Go to the `viewConfigDiff` schema section → `ShowEmailsButton` element.
   2. Bind the sending of the custom `usr.ShowEmailsRequest` request to the
      `clicked` button event.
   3. Go to the `OpenContactsButton` element.
   4. Bind the sending of the base `crt.OpenPageRequest` request to the
      `clicked` button event.
   5. Enter the schema code of the page to open in the `params` property.

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        /* Button that calls the {JSON} Placeholder external web service from the request page. */
        {
            "operation": "insert",
            "name": "ShowEmailsButton",
            "values": {
                ...,
                "clicked": {
                    /* Bind the sending of the custom request to the clicked button event. */
                    "request": "usr.ShowEmailsRequest"
                }
            },
            ...
        },
        /* Button that opens the Contacts section. */
        {
            "operation": "insert",
            "name": "OpenContactsButton",
            "values": {
                ...,
                "clicked": {
                    /* Bind the sending of the custom request to the clicked button event. */
                    "request": "crt.OpenPageRequest",
                    "params": {
                        "schemaName": "Contacts_ListPage"
                    }
                }
            },
            ...
        }
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

4. **Implement the custom request handler**.

For this example, implement the custom `usr.ShowEmailsRequest` request handler.

     1. Go to the `handlers` schema section.

     2. Create an instance of the `CrtZoneService` service.

     3. Create an instance of the `HttpClientService` service.

     4. Specify the URL to retrieve a list of posts. Use the `{JSON} Placeholder` external service.

     5. Retrieve emails from post comments. For this example, handle 10 posts.

     6. Implement the business logic.

        * If you need to **switch between pages** regardless of whether the request to the web service is complete or still in progress, use the `CrtZoneService` service instance and `runOutside()` method.

handlers schema section

              handlers: /**SCHEMA_HANDLERS*/[
                  {
                      request: "usr.ShowEmailsRequest",
                      /* Implement the custom request handler. */
                      handler: async (request, next) => {
                          /* Create an instance of the CrtZoneService service. */
                          const zoneService = new sdk.CrtZoneService();
                          /* Create an instance of the HttpClientService service. */
                          const httpClientService = new sdk.HttpClientService();
                          /* Specify the URL to retrieve emails from post comments. Use the {JSON} Placeholder external service. */
                          const postsEndpoint = "https://jsonplaceholder.typicode.com/posts";
                          /* Implement the business logic to switch between pages regardless of whether the request to the web service is complete or still in progress. */
                          zoneService.runOutside(async () => {
                              const collectedEmails = [];
                              /* Retrieve emails from comments to 10 posts. */
                              for (let postsId = 1; postsId <= 10; postsId++) {
                                  const commends = await httpClientService.get(`${postsEndpoint}/${postsId}/comments`);
                                  const commentEmails = commends.body.map(comment => comment.email);
                                  collectedEmails.push(...commentEmails);
                              }
                              alert(`Post comments have been successfully processed.` + '\n\n' + `Selected posts are commented by users with following emails:` + '\n' + collectedEmails.join(', '));
                          });
                      }
                  }
              ]/**SCHEMA_HANDLERS*/,


        * If you need to **block switching between pages** while the request to the web service is still in progress, comment out the use of the `CrtZoneService` service instance and `runOutside()` method. This retrieves emails from post comments without using Creatio zone.

handlers schema section

              handlers: /**SCHEMA_HANDLERS*/[
                  {
                      request: "usr.ShowEmailsRequest",
                      /* Implement the custom request handler. */
                      handler: async (request, next) => {
                          /* Create an instance of the CrtZoneService service. */
                          //const zoneService = new sdk.CrtZoneService();
                          /* Create an instance of the HttpClientService service. */
                          const httpClientService = new sdk.HttpClientService();
                          /* Specify the URL to retrieve emails from post comments. Use the {JSON} Placeholder external service. */
                          const postsEndpoint = "https://jsonplaceholder.typicode.com/posts";
                          /* Implement the business logic to switch between pages regardless of whether the request to the web service is complete or still in progress. */
                          //zoneService.runOutside(async () => {
                              const collectedEmails = [];
                              /* Retrieve emails from comments to 10 posts. */
                              for (let postsId = 1; postsId <= 10; postsId++) {
                                  const commends = await httpClientService.get(`${postsEndpoint}/${postsId}/comments`);
                                  const commentEmails = commends.body.map(comment => comment.email);
                                  collectedEmails.push(...commentEmails);
                              }
                              alert(`Post comments have been successfully processed.` + '\n\n' + `Selected posts are commented by users with following emails:` + '\n' + collectedEmails.join(', '));
                          //});
                      }
                  }
              ]/**SCHEMA_HANDLERS*/,


5. **Save the changes**.

## View the result​

To view the outcome of the example that **lets you switch between pages** :

1. Make sure the `usr.ShowEmailsRequest` request handler **uses the**
   `CrtZoneService` **service instance and** `runOutside()` **method**.
2. **Open the Requests section**.
3. **Create a request**.
4. Click **Show emails**.
5. Click **Open contacts**.

**As a result** , Creatio will open the **Contacts** section regardless of
whether the request to the web service is complete or still in progress.
[View the result >>>](https://academy.creatio.com/documents?ver=8.3&id=15093&anchor=view-result-1)

To view the outcome of the example that **blocks switching between pages** :

1. Make sure the `usr.ShowEmailsRequest` request handler **does not use the**
   `CrtZoneService` **service instance and** `runOutside()` **method**.
2. **Open the Requests section**.
3. **Create a request**.
4. Click **Show emails**.
5. Click **Open contacts**.

**As a result** , Creatio will block opening the **Contacts** section while the
request to the web service is still in progress.
[View the result >>>](https://academy.creatio.com/documents?ver=8.3&id=15093&anchor=view-result-2)

## Source code​

UsrRequests_FormPage

    /* Declare the AMD module. */
    define("UsrRequests_FormPage", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
        return {
            viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
                {
                    "operation": "merge",
                    "name": "Feed",
                    "values": {
                        "dataSourceName": "PDS",
                        "entitySchemaName": "UsrRequests"
                    }
                },
                {
                    "operation": "merge",
                    "name": "AttachmentList",
                    "values": {
                        "columns": [
                            {
                                "id": "2756ad1d-3f63-4d21-9e4f-f4c3ad260326",
                                "code": "AttachmentListDS_Name",
                                "caption": "#ResourceString(AttachmentListDS_Name)#",
                                "dataValueType": 28,
                                "width": 200
                            }
                        ]
                    }
                },
                /* Button that calls the {JSON} Placeholder external web service from the request page. */
                {
                    "operation": "insert",
                    "name": "ShowEmailsButton",
                    "values": {
                        "type": "crt.Button",
                        "caption": "#ResourceString(ShowEmailsButton_caption)#",
                        "color": "default",
                        "disabled": false,
                        "size": "large",
                        "iconPosition": "only-text",
                        "visible": true,
                        "clicked": {
                            /* Bind the sending of the custom request to the clicked button event. */
                            "request": "usr.ShowEmailsRequest"
                        }
                    },
                    "parentName": "CardToolsContainer",
                    "propertyName": "items",
                    "index": 0
                },
                /* Button that opens the Contacts section. */
                {
                    "operation": "insert",
                    "name": "OpenContactsButton",
                    "values": {
                        "type": "crt.Button",
                        "caption": "#ResourceString(OpenContactsButton_caption)#",
                        "color": "primary",
                        "disabled": false,
                        "size": "large",
                        "iconPosition": "only-text",
                        "visible": true,
                        "clicked": {
                            /* Bind the sending of the custom request to the clicked button event. */
                            "request": "crt.OpenPageRequest",
                            "params": {
                                "schemaName": "Contacts_ListPage"
                            }
                        }
                    },
                    "parentName": "CardToolsContainer",
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
                        "control": "$UsrName",
                        "labelPosition": "auto"
                    },
                    "parentName": "SideAreaProfileContainer",
                    "propertyName": "items",
                    "index": 0
                }
            ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
            viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
                {
                    "operation": "merge",
                    "path": [
                        "attributes"
                    ],
                    "values": {
                        "UsrName": {
                            "modelConfig": {
                                "path": "PDS.UsrName"
                            }
                        }
                    }
                },
                {
                    "operation": "merge",
                    "path": [
                        "attributes",
                        "Id",
                        "modelConfig"
                    ],
                    "values": {
                        "path": "PDS.Id"
                    }
                }
            ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
            modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[
                {
                    "operation": "merge",
                    "path": [],
                    "values": {
                        "primaryDataSourceName": "PDS"
                    }
                },
                {
                    "operation": "merge",
                    "path": [
                        "dataSources"
                    ],
                    "values": {
                        "PDS": {
                            "type": "crt.EntityDataSource",
                            "config": {
                                "entitySchemaName": "UsrRequests"
                            },
                            "scope": "page"
                        }
                    }
                }
            ]/**SCHEMA_MODEL_CONFIG_DIFF*/,
            handlers: /**SCHEMA_HANDLERS*/[
                {
                    request: "usr.ShowEmailsRequest",
                    /* Implement the custom request handler. */
                    handler: async (request, next) => {
                        /* Create an instance of the CrtZoneService service. */
                        const zoneService = new sdk.CrtZoneService();
                        /* Create an instance of the HttpClientService service. */
                        const httpClientService = new sdk.HttpClientService();
                        /* Specify the URL to retrieve emails from post comments. Use the {JSON} Placeholder external service. */
                        const postsEndpoint = "https://jsonplaceholder.typicode.com/posts";
                        /* Implement the business logic to switch between pages regardless of whether the request to the web service is complete or still in progress. */
                        zoneService.runOutside(async () => {
                            const collectedEmails = [];
                            /* Retrieve emails from comments to 10 posts. */
                            for (let postsId = 1; postsId <= 10; postsId++) {
                                const commends = await httpClientService.get(`${postsEndpoint}/${postsId}/comments`);
                                const commentEmails = commends.body.map(comment => comment.email);
                                collectedEmails.push(...commentEmails);
                            }
                            alert(`Post comments have been successfully processed.` + '\n\n' + `Selected posts are commented by users with following emails:` + '\n' + collectedEmails.join(', '));
                        });
                    }
                }
            ]/**SCHEMA_HANDLERS*/,
            converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
            validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
        };
    });

---

## Resources​

[Package with example implementation](https://academy.creatio.com/docs/sites/academy_en/files/packages/CreatioZone/8.1/UsrRequests_2024-03-21_08.51.00.zip)

- 1\. Set up the page UI
- 2\. Implement the execution of business logic using Creatio zone
- View the result
- Source code
- Resources
