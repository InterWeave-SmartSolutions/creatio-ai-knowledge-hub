# Interact with business processes using a request handler | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1032
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/platform-customization/freedom-ui/business-processes

## Description

This functionality is available for Creatio 8.2.3 and later.

## Key Concepts

business process, freedom ui, section, automation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/business-processes)**
(8.3).

Version: 8.2

On this page

Level: advanced

note

This functionality is available for Creatio 8.2.3 and later.

Since version 8.2.3, `@creatio-devkit/common` includes the
`ProcessEngineService` service that lets you interact with business processes.
This ensures context transfer, enabling stable and predictable business logic
execution as part of automation and development. Learn more:
[Service that runs business processes](https://academy.creatio.com/documents?ver=8.2&id=15441).

## Run a business process​

note

Creatio forbids running the business process that has output parameters in the
background.

To run a business process:

1. **Add a button** to run a business process from a Freedom UI page if needed.
   Instructions:
   [Set up Button components](https://academy.creatio.com/documents?ver=8.2&id=2401)
   (user documentation).

2. **Add the dependencies**. Instructions:
   [Display the value of a system variable](https://academy.creatio.com/documents?ver=8.2&id=15380&anchor=amd-dependencies)
   (similarly to step 2). Instead of the `SysValuesService` service, use the
   `ProcessEngineService` service that lets you interact with business
   processes.

3. **Set up how to handle the action** executed on button click. Instructions:
   [Optimize the execution of a custom business logic](https://academy.creatio.com/documents?ver=8.2&id=15095&anchor=action-executed-on-button-click)
   (step 4).

4. **Implement the custom request handler**.
   1. Go to the `handlers` schema section.

   2. Implement the `usr.SomeCustomRequest` custom request handler.
      1. Create an instance of the business process service from
         `@creatio-devkit/common`.

      2. Implement the `executeProcessByName()` method that runs the business
         process.

      3. Pass the following method parameters:
         - Name (the `Code` property value) of the business process to run. Pass
           as a string.
         - Key-value collection of input business process parameters where key
           is the parameter code (the `Code` property value) and the value is
           the parameter value.
         - Collection of output business process parameters. Pass as an array.

      4. Retrieve the ID of the business process to run and specify it in the
         `ProcessId` attribute.

      5. Retrieve output parameters of the business process to run using the
         `resultParameterValues` property and specify them in the attributes if
         needed.

View an example of a `usr.SomeCustomRequest` request handler that runs the
business process whose `Code` property value is `SomeBusinessProcess` below. The
business process uses the `SomeInputParameter` parameter whose value is
"SomeInputParameterValue."

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "usr.SomeCustomRequest",
            /* The implementation of the custom request handler. */
            handler: async (request, next) => {
                /* Create an instance of the business process service from "@creatio-devkit/common." */
                const service = new sdk.ProcessEngineService();
                /* Implement the "executeProcessByName()" method that runs the business process. */
                const result = await service.executeProcessByName(
                    /* Name (the "Code" property value) of the business process to run. */
                    "SomeBusinessProcessCode",
                    /* Key-value collection of input business process parameters where key is the parameter code (the "Code" property value) and the value is the parameter value. */
                    {
                        "SomeInputParameter1": SomeInputParameter1Value,
                        "SomeInputParameter2": SomeInputParameter2Value
                    },
                    /* Collection of output business process parameters. */
                    [
                        "SomeOutputParameter1",
                        "SomeOutputParameter2"
                    ],
                );
                /* Retrieve the ID of the business process to run and specify it in the "ProcessId" attribute. */
                request.$context['ProcessId'] = result.processId;

                /* Retrieve collection of business process output parameters using the "resultParameterValues" property and specify them in the attributes if needed. */
                const resultParameters = result.resultParameterValues;
                request.$context['SomeAttribute1'] = resultParameters.SomeOutputParameter1;
                request.$context['SomeAttribute2'] = resultParameters.SomeOutputParameter2;

                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            },
        },
    ]

## Complete a business process element​

1. **Set up the page UI** if needed. Instructions:
   [Element setup examples](https://academy.creatio.com/docs/8.x/no-code-customization/category/element-setup-examples)
   (user documentation).

2. **Add the dependencies**. Instructions:
   [Display the value of a system variable](https://academy.creatio.com/documents?ver=8.2&id=15380&anchor=amd-dependencies)
   (similarly to step 2). Instead of the `SysValuesService` service, use the
   `ProcessEngineService` service that lets you interact with business
   processes.

3. **Implement the custom request handler**.
   1. Go to the `handlers` schema section.

   2. Implement the `usr.SomeCustomRequest` custom request handler.
      1. Retrieve the ID of the business process to run.
      2. Retrieve the ID of the business process element using process ID and
         caption of the Freedom UI page.
      3. Create an instance of the business process service from
         `@creatio-devkit/common`.
      4. Implement the `completeExecuting()` method that completes a business
         process element using element ID.
      5. Pass a list of additional method parameters if needed.

View an example of a `usr.SomeCustomRequest` request handler that completes a
business process element whose `Code` property value is
`SomeBusinessProcessElement` below.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "usr.SomeCustomRequest",
            /* The implementation of the custom request handler. */
            handler: async (request, next) => {
                /* Retrieve the ID of the business process to run. */
                const processId = await request.$context["ProcessId"];
                /* Retrieve the ID of the business process element using process ID and caption of the Freedom UI page. */
                const sysProcessElementLogModel = await sdk.Model.create("SysProcessElementLog");
                const filters = new sdk.FilterGroup();
                await filters.addSchemaColumnFilterWithParameter(sdk.ComparisonType.Equal, "SysProcess", processId);
                await filters.addSchemaColumnFilterWithParameter(sdk.ComparisonType.Equal, "Caption", "Show page");
                const sysProcessElementLog = await sysProcessElementLogModel.load({
                    attributes: ["Id"],
                    parameters: [{
                        type: sdk.ModelParameterType.Filter,
                        value: filters
                    }]
                });
                const processElementId = sysProcessElementLog[0]["Id"];
                /* Create an instance of the business process service from "@creatio-devkit/common." */
                const service = new sdk.ProcessEngineService();
                /* Implement the "completeExecuting()" method that completes a business process element using element ID. */
                await service.completeExecuting(
                    /* Element ID. */
                    processElementId,
                    /* List of additional method parameters. For example, code of clicked button for "Auto-generated page" element. */
                    {
                        "PressedButtonCode": "SomeButtonCode"
                    }
                );
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            },
        },
    ]

---

## See also​

[Service that runs business processes](https://academy.creatio.com/documents?ver=8.2&id=15441)

[Display the value of a system variable](https://academy.creatio.com/documents?ver=8.2&id=15380)

[Element setup examples](https://academy.creatio.com/docs/8.x/no-code-customization/category/element-setup-examples)
(user documentation)

- Run a business process
- Complete a business process element
- See also
