# Marketplace app licensing | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 2006
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/app-licensing

## Description

Licensing lets you control usage of paid Marketplace apps. Learn more: Licensing
(user documentation).

## Key Concepts

configuration, freedom ui, section, detail, lookup, operation, package,
notification, lead, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

On this page

Level: intermediate

**Licensing** lets you control usage of paid Marketplace apps. Learn more:
[Licensing](https://academy.creatio.com/docs/8.x/setup-and-administration/category/licensing)
(user documentation).

The licensed options of the Marketplace app depend on the license type and
licensed element.

**General procedure** to license paid Marketplace app:

1. Define the license type. Read more >>>
2. Define the licensed elements. Read more >>>
3. Implement the license verification. Read more >>>
4. Send data obtained on previous steps to the Creatio Marketplace support
   (`marketplace@creatio.com`) when publishing the Marketplace app via the
   Creatio Marketplace Console. Instructions:
   [Steps to publish the Marketplace listing using Creatio Marketplace Console](https://academy.creatio.com/documents?id=15957).
5. Creatio Marketplace support generates licenses for the Marketplace app based
   on the received data.

The developer must take steps 1–3 when developing the Marketplace app.

## 1\. Define the license type​

View the license types provided by Creatio in the table below.

| License type | License description | Personal | Grant access to the app for specific users. Bound to the user account and cannot be used by other users. The system administrator can redistribute licenses among users at any time. Instructions: [Distribute or recall licenses for multiple users](https://academy.creatio.com/documents?id=1472&anchor=title-230-2) (user documentation). | Server | Grant access to the app without binding access to specific users. All Creatio users that have the corresponding permissions have access to the licensed functionality. |
| ------------ | ------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Licenses last for 365 days regardless of the type. The license expiration date
is specified in the license and controlled by Creatio.

## 2\. Define the licensed elements​

View the licensed elements in the table below.

| Licensed element | Description of licensed element | Licensed objects | Names of custom objects added to the Marketplace app. Licensed objects are any custom objects, for example, section, detail, or lookup objects. | Licensed operations | Names of operations added to the Marketplace app logic to verify the license for specific functionality. For example, an additional action was added to a base Creatio section. The action must be connected to the licensed operation. When the action is called, the app business logic verifies the license. Based on the result, Creatio executes or interrupts the functionality. |
| ---------------- | ------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

The license can include one or more licensed elements. Make sure the licensed
elements meet the
[Requirements for Pricing and support tab properties](https://academy.creatio.com/documents?id=15008&anchor=title-4007-10).
The licensed elements do not depend on the license type.

Important

Do not use personal and server licenses that control the same objects and
operations at the same time.

View the licensed options of the Marketplace app in the table below.

| Licensed element | Example of functionality | License type | Subscription type | Licensed objects | New Creatio section. | Personal | Paid per user that works with the section. | Server | Fixed price regardless of the number of users that work with the section. | Key object that contains active data changes. | Personal | Paid per user that works with the key object. | Server | Fixed price regardless of the number of users that work with the key object. | Licensed operations | Connector to an external service, for example, a telephony connector. | Personal | Paid per user that can access to the service. For example, access to a telephony connector is paid per individual user. | Connector to an external service, for example, web chat that registers leads or requests in Creatio. | Server | Fixed price regardless of the number of users that have access to the service. | Custom component | Sidebar | Licensed objects and operations | Section with records that use connectors to various external services. | Personal | Paid both per user that can access the section and per service connector. For example, the **Requests** section was improved. The section is integrated with an external system that registers requests. The customer pays for access to the section functionality per user. |
| ---------------- | ------------------------ | ------------ | ----------------- | ---------------- | -------------------- | -------- | ------------------------------------------ | ------ | ------------------------------------------------------------------------- | --------------------------------------------- | -------- | --------------------------------------------- | ------ | ---------------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------ | ---------------- | ------- | ------------------------------- | ---------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## 3\. Implement the license verification​

Since Creatio verifies the licenses that include **licensed objects** using
out-of-the-box tools, you do not need to implement the license verification for
licensed objects.

If the license includes **licensed operations** , implement the license
verification in the source code of a Marketplace app. Creatio can verify the
licenses both from back-end and front-end.

### Implement the license verification from the back-end​

1. **Call the method** that verifies licenses.

View the methods of the `Terrasoft.Core.LicHelper` class that check license
restrictions, in the table below.

| Method | Method parameter | Method description | GetHasOperationLicense(string sysPackageOperationCode); | `sysPackageOperationCode` is a string parameter that contains the name of the licensed operation. Specify this name in the `Licensed operations` property on the revision page when publishing the Marketplace app. Instructions: [Release details tab](https://academy.creatio.com/documents?id=15957&anchor=title-2399-8). | If the license is found, returns `true`. Otherwise, returns `false`. | CheckHasOperationLicense(string sysPackageOperationCode); | If the license is found, returns `true`. Otherwise, generates the `LicException` exception. |
| ------ | ---------------- | ------------------ | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------- |

View the examples that check the status of the `SomeLicensedOperation.Use`
licensed operation in the back-end below.

     * Example that uses the GetHasOperationLicense() method
     * Example that uses the CheckHasOperationLicense() method

    UserConnection.LicHelper.GetHasOperationLicense("SomeLicensedOperation.Use");


    UserConnection.LicHelper.CheckHasOperationLicense("SomeLicensedOperation.Use");

2. **Handle the result**.

### Implement the license verification from the front-end​

Creatio lets you implement the license verification from the front-end in the
source code of both Freedom UI page and remote module.

#### Implement the license verification in the source code of a Freedom UI page​

1. **Add the dependencies**. To do this, add `@creatio-devkit/common` library as
   a dependency.

`@creatio-devkit/common` includes the `LicenseService` service to check license
restrictions.

2. **Call the method** that verifies licenses.

View the method of the `LicenseService` service that checks license restrictions
in the table below.

| Method | Method parameter | Method description | getLicenseOperationStatuses(operationCodes: string[]); | `operationCodes` is a string parameter that contains the list of the licensed operation names. Specify this name in the `Licensed operations` property on the revision page when publishing the Marketplace app. Instructions: [Release details tab](https://academy.creatio.com/documents?id=15957&anchor=title-2399-8). | Returns an object that has keys as operation codes and values as operation statuses. |
| ------ | ---------------- | ------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |

3. **Handle the result**.

View the example that checks the status of the `MrktShowButton.Use` licensed
operation in the Freedom UI page below.

MrktSomeApp_Page

    /* Declare the AMD module. */
    define("MrktSomeApp_Page", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
        return {
            ...,
            handlers: /**SCHEMA_HANDLERS*/[
                {
                    request: "mrkt.SomeHandleRequest",
                    /* The custom implementation of the request handler. */
                    handler: async (request, next) => {
                        /* Create an instance of the "LicenseService" service from "@creatio-devkit/common." */
                        const licenseService = new sdk.LicenseService();
                        /* Retrieve data about status of the "MrktShowButton.Use" licensed operation. */
                        const licenseStatus = await licenseService.getLicenseOperationStatuses(['MrktShowButton.Use']);
                        const mrktShowButtonLicenseStatus = licenseStatus['MrktShowButton.Use'];
                        /* Set the "SomeAttribute" attribute to "mrktShowButtonLicenseStatus". */
                        request.$context.SomeAttribute = mrktShowButtonLicenseStatus;
                        /* If the user has license restrictions for using the "MrktShowButton.Use" licensed operation, Creatio displays "NotLicensedFunctionalityMessage" notification message. "NotLicensedFunctionalityMessage" is a localizable string. */
                        request.$context.NotLicensedFunctionalityMessage = mrktShowButtonLicenseStatus ? "" : await request.$context.Resources.Strings.MrktNotLicensedFunctionalityMessage;
                        /* Call the next handler if it exists and return its result. */
                        return next?.handle(request);
                    },
                }
            ]/**SCHEMA_HANDLERS*/,
            ...,
        };
    });

#### Implement the license verification in the source code of a remote module​

1. **Open the** `some-mrkt-component.component.ts` **file**.

2. **Import the** `LicenseService` **functionality** from the
   `@creatio-devkit/common` library into the component.

`@creatio-devkit/common` includes the `LicenseService` service to check license
restrictions.

3. **Call the method** that verifies licenses.

4. **Handle the result**.

View the example that checks the status of the `MrktShowButton.Use` licensed
operation in the remote module below.

some-mrkt-component.component.ts

    /* Import the required functionality from the libraries. */
    import { LicenseService } from '@creatio-devkit/common';
    ...
    export class SomeMrktComponent {
      private readonly _licenseService: LicenseService;
      constructor() {
        /* Create an instance of the "LicenseService" service from "@creatio-devkit/common." */
        this._licenseService = new LicenseService();
      }

      public async getButtonLicenseOperationsStatus(): Promise<boolean> {
        /* Retrieve data about status of the "MrktShowButton.Use" licensed operation. */
        const licenseStatus = await this._licenseService.getLicenseOperationStatuses(['MrktShowMyButton.Use']);
        return licenseStatus.['MrktShowMyButton.Use'];
      }
    }

#### Implement the license verification from the front-end for a custom component​

1. **Add a single custom component to a single package**.

2. **Set the package as a licensed package**.
   1. Download the package that contains the functionality of custom component
      to be licensed.

   2. Extract the \*.zip archive that contains the package using the Clio
      utility. Instructions:
      [official vendor documentation](https://github.com/Advance-Technologies-Foundation/clio#extract-package).

   3. Open the `..\SomePackage\descriptor.json` file.

`SomePackage` is a package that contains the functionality of custom component
to be licensed.

`descriptor.json` file stores the package properties, including codes of
licensed operations.

     4. Add the `LicOperations` property that contains an array of configuration objects.

     5. Add the configuration object of licensed operation.

     6. Fill out the properties of licensed operation.

| Property | Property description | Property example | Code | Code of licensed operation added to the Marketplace app logic to verify the license for specific functionality. | MrktTimerComponent.Use | Name | Name of licensed operation added to the Marketplace app logic to verify the license for specific functionality. Must correspond to the component functionality and be understandable for end users.Creatio uses the `Name` property value in the notification when a user installs a package that includes a custom component for which they do not have a license. The notification pattern is as follows: `You have no license for the following components: "SomeComponent" (SomePackage), ... . Contact the system administrator to receive the license. Otherwise, access to the components will be forbidden.`, where `SomeComponent` is the `Name` property value. | Timer |
| -------- | -------------------- | ---------------- | ---- | --------------------------------------------------------------------------------------------------------------- | ---------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |

     7. Save the changes.

View the example of the `descriptor.json` file that uses
`MrktTimerComponent.Use` licensed operation, below.

descriptor.json file

    {
        "Descriptor": {
            ...,
            "LicOperations": [
                {
                    "Code": "MrktTimerComponent.Use",
                    "Name": "Timer"
                },
                ...,
            ]
        }
    }

#### Implement the license verification from the front-end for a custom sidebar​

note

This functionality is available for Creatio 8.1.5 and later.

1. **Download the package that contains the custom sidebar** to be licensed.

2. **Extract the \*.zip archive** that contains the package using the Clio
   utility. Instructions:
   [official vendor documentation](https://github.com/Advance-Technologies-Foundation/clio#extract-package).

3. **Open the** `..\SomePackage\descriptor.json` **file**.

`SomePackage` is a package that contains the custom sidebar to be licensed.

`descriptor.json` file stores the package properties, including codes of
licensed operations.

4. **Add the** `LicOperations` **property** that contains an array of
   configuration objects.

5. **Add the configuration object of licensed operation**.

6. **Fill out the properties** of licensed operation.

| Property | Property description | Property example | Code | Code of licensed operation added to the app logic to verify the license for sidebar. | MrktCtiSidebar.Use | Name | Name of licensed operation added to the app logic to verify the license for sidebar. Must correspond to the sidebar functionality and be understandable for end users.Creatio uses the `Name` property value in the notification when a user installs a package that includes a sidebar for which they do not have a license. The notification pattern is as follows: `You have no license for the following sidebars: "SomeSidebar" (SomePackage), ... . Contact the system administrator to receive the license. Otherwise, access to the sidebar will be forbidden.`, where `SomeSidebar` is the `Name` property value. | CTI sidebar | Schemas property | Name | The code of schema that implements custom functionality of the sidebar to be licensed. | MrktCtiSidebar | ManagerName | The name of the manager that implements the **Addon** schema type of the sidebar. | AddonSchemaManager |
| -------- | -------------------- | ---------------- | ---- | ------------------------------------------------------------------------------------ | ------------------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------------- | ---- | -------------------------------------------------------------------------------------- | -------------- | ----------- | --------------------------------------------------------------------------------- | ------------------ |

7. **Save the changes**.

View the example of the `descriptor.json` file that uses `MrktCtiSidebar.Use`
licensed operation, below.

descriptor.json file

    {
        "Descriptor": {
            ...,
            "LicOperations": [
                {
                    "Code": "MrktCtiSidebar.Use",
                    "Name": "CTI sidebar",
                    "Schemas": [
                        {
                            "Name": "MrktCtiSidebar",
                            "ManagerName": "AddonSchemaManager"
                        }
                    ]
                },
                ...,
            ]
        }
    }

---

## See also​

[Licensing](https://academy.creatio.com/docs/8.x/setup-and-administration/category/licensing)
(user documentation)

[Steps to publish the Marketplace listing using Creatio Marketplace Console](https://academy.creatio.com/documents?id=15957)

[Requirements for Marketplace listing resources](https://academy.creatio.com/documents?id=15008)

[Steps to publish a public profile](https://academy.creatio.com/documents?id=15092)

[Customize sidebars](https://academy.creatio.com/documents?id=15102)

---

## Resources​

[Official Clio utility documentation](https://github.com/Advance-Technologies-Foundation/clio)

[Marketplace updates](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/category/marketplace-updates)

- 1\. Define the license type
- 2\. Define the licensed elements
- 3\. Implement the license verification
  - Implement the license verification from the back-end
  - Implement the license verification from the front-end
- See also
- Resources
