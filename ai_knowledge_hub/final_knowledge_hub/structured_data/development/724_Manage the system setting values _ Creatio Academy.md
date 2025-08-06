# Manage the system setting values | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 668
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/system-setting/overview

## Description

@creatio-devkit/common includes the sdk.SysSettingsService service to manage
system settings.

## Key Concepts

freedom ui, section, detail, system setting

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/system-setting/overview)**
(8.3).

Version: 8.0

On this page

Level: beginner

`@creatio-devkit/common` includes the `sdk.SysSettingsService` service to manage
system settings.

**Detailed example** :
[Manage the system setting values on a page](https://academy.creatio.com/documents?ver=8.0&id=15362).

To manage the value of a system setting:

1. If needed, **add a label** to display the value of a system setting.
   Instructions:
   [Set up a Label component](https://academy.creatio.com/documents?ver=8.0&id=2433)
   (user documentation).

2. **Add the dependencies**. Instructions:
   [Display the value of a system variable](https://academy.creatio.com/documents?ver=8.0&id=15380&anchor=amd-dependencies)
   (similarly to step 2). Instead of the `sdk.SysValuesService` service, use the
   `sdk.SysSettingsService` service that manages system settings.

3. **Add an attribute**. Instructions:
   [Set up the field display condition](https://academy.creatio.com/documents?ver=8.0&id=15379&anchor=viewModelConfig)
   (step 2).

4. **Bind an attribute to the label**. Instructions:
   [Set up the field display condition](https://academy.creatio.com/documents?ver=8.0&id=15379&anchor=viewConfigDiff)
   (similarly to step 3). Instead of the `visible` property, use the `caption`
   property that handles the text displayed in the element.

5. **Implement the base request handler**.

For Creatio versions 8.0.6-8.0.10

     1. Go to the `handlers` schema section.

     2. Add a custom implementation of the `crt.HandleViewModelResumeRequest` base request handler.

        1. Create an instance of the system setting service from `@creatio-devkit/common`.
        2. Retrieve the value of the system setting and specify data in the corresponded attribute.
        3. Implement the business logic that changes the system setting value.
        4. Specify data in the corresponding attribute.

View an example of a `crt.HandleViewModelResumeRequest` request handler that
changes the `someSystemSetting` system setting and specifies the value in the
`SomeAttribute` attribute, below.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandleViewModelResumeRequest",
            /* The custom implementation of the system request handler. */
            handler: async (request, next) => {
                /* Wait for the rest of the initialization handlers to finish. */
                await next?.handle(request);
                /* Create an instance of the system setting service from "@creatio-devkit/common." */
                const sysSettingsService = new sdk.SysSettingsService();
                /* Retrieve the value of the "SomeSystemSetting" system setting. */
                const someVariable = await sysSettingsService.getByCode('SomeSystemSetting');
                /* Specify the value of the system setting in the "SomeAttribute" attribute. */
                request.$context.SomeAttribute = someConst.displayValue;
                /* Implement the business logic that changes the system setting value. */
                ...;
                /* Specify the new value of the system setting in the "SomeAttribute" attribute. */
                request.$context.SomeAttribute = someVariable;
            }
        },
    ] /**SCHEMA_HANDLERS*/,

For Creatio versions 8.0-8.0.5

     1. Go to the `handlers` schema section.

     2. Add a custom implementation of the `crt.HandlerViewModelInitRequest` base request handler.

        1. Create an instance of the system setting service from `@creatio-devkit/common`.
        2. Retrieve the value of the system setting and specify data in the corresponded attribute.
        3. Implement the business logic that changes the system setting value.
        4. Specify data in the corresponding attribute.

View an example of a `crt.HandlerViewModelInitRequest` request handler that
changes the `someSystemSetting` system setting and specifies the value in the
`SomeAttribute` attribute, below.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandlerViewModelInitRequest",
            /* The custom implementation of the system request handler. */
            handler: async (request, next) => {
                /* Wait for the rest of the initialization handlers to finish. */
                await next?.handle(request);
                /* Create an instance of the system setting service from "@creatio-devkit/common." */
                const sysSettingsService = new sdk.SysSettingsService();
                /* Retrieve the value of the "SomeSystemSetting" system setting. */
                const someVariable = await sysSettingsService.getByCode('SomeSystemSetting');
                /* Specify the value of the system setting in the "SomeAttribute" attribute. */
                request.$context.SomeAttribute = someConst.displayValue;
                /* Implement the business logic that changes the system setting value. */
                ...;
                /* Specify the new value of the system setting in the "SomeAttribute" attribute. */
                request.$context.SomeAttribute = someVariable;
            }
        },
    ] /**SCHEMA_HANDLERS*/,

---

## See also​

[Set up a Label component](https://academy.creatio.com/documents?ver=8.0&id=2433)
(user documentation)

[Display the value of a system variable](https://academy.creatio.com/documents?ver=8.0&id=15380)

[Customize fields (Freedom UI)](https://academy.creatio.com/documents?ver=8.0&id=15379)

- See also
