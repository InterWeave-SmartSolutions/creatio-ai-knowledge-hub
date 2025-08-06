# Create a replacing class | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1108
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/back-end-development/replacing-class-factory/examples/create-a-replacing-class

## Description

Create a replaced class and a custom web service that uses cookie-based
authentication in a user-made package. Create a replacement class in another
user-made package. Call the custom web service both using and not using the
class replacement.

## Key Concepts

configuration, section, web service, operation, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/replacing-class-factory/examples/create-a-replacing-class)**
(8.3).

Version: 8.2

On this page

Level: advanced

Example

Create a replaced class and a custom web service that uses cookie-based
authentication in a user-made package. Create a replacement class in another
user-made package. Call the custom web service both using and not using the
class replacement.

## 1\. Implement the replaced class​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.2&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.2&id=15121) to which to
   add the schema.

2. Click **Add** → **Source code** on the section list toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateSourceCodeSchema(7.17)/scr_add_schema.png>)

3. Fill out the schema properties in the Schema Designer:
   - **Code** – "UsrOriginalClass".
   - **Title** – "OriginalClass".

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ExampleClassReplacement/7.18/scr_OriginalClass_Settings.png)

4. Create a replaced `UsrOriginalClass` class that contains the
   `GetAmount(int, int)` virtual method. The method adds two values passed as
   parameters.

UsrOriginalClass

         namespace Terrasoft.Configuration {
             public class UsrOriginalClass {
                 /* GetAmount() is a virtual method that has its own implementation. Inheritors can redefine the method. */
                 public virtual int GetAmount(int originalValue1, int originalValue2) {
                     return originalValue1 + originalValue2;
                 }
             }
         }



5. **Publish the schema**.

## 2\. Implement a replacing class​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.2&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.2&id=15121) to which to
   add the schema. Select a package other than the package in which you
   implemented the `UsrOriginalClass` replaced class.

2. Add the user-made package that contains the `UsrOriginalClass` replaced class
   as a
   [dependency](https://academy.creatio.com/documents?ver=8.2&id=15121&anchor=title-2105-3)
   for the user-made package that contains the replacing class.

3. Click **Add** → **Source code** on the section list toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateSourceCodeSchema(7.17)/scr_add_schema.png>)

4. Fill out the schema properties in the Schema Designer:
   - **Code** – "UsrSubstituteClass".
   - **Title** – "SubstituteClass".

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ExampleClassReplacement/7.18/scr_SubstituteClass_Settings.png)

5. Create a `SubstituteClass` replacing class that contains the
   `GetAmount(int, int)` method. The method summarizes two values passed as
   parameters and multiplies the sum by the value passed in the `Rate` property.
   Creatio will initialize the `Rate` property in the replacing class
   constructor.

UsrSubstituteClass

         namespace Terrasoft.Configuration {
             [Terrasoft.Core.Factories.Override]
             public class UsrSubstituteClass: UsrOriginalClass {
                 /* Rate. Assign the property value in the class. */
                 public int Rate {
                     get;
                     private set;
                 }

                 /* Initialize the Rate property in the constructor using the passed value. */
                 public UsrSubstituteClass(int rateValue) {
                     Rate = rateValue;
                 }

                 /* Replace the parent method using the custom implementation. */
                 public override int GetAmount(int substValue1, int substValue2) {
                     return (substValue1 + substValue2) * Rate;
                 }
             }

         }



6. **Publish the schema**.

## 3\. Implement a custom web service​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.2&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.2&id=15121) to which to
   add the schema. Use the package in which you implemented the
   `UsrOriginalClass` replaced class for the
   [custom web service](https://academy.creatio.com/documents?ver=8.2&id=15262).

2. Click **Add** → **Source code** on the section list toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateSourceCodeSchema(7.17)/scr_add_schema.png>)

3. Fill out the schema properties in the Schema Designer:
   - **Code** – "UsrAmountService".
   - **Title** – "AmountService".

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots//ExampleClassReplacement/7.18/scr_AmountService_Settings.png)

4. Create a service class.
   1. Add the `Terrasoft.Configuration` namespace in the Schema Designer.
   2. Add the namespaces the data types of which to utilize in the class using
      the `using` directive.
   3. Add the name of the `UsrAmountService` class that matches the schema name
      (the **Code** property).
   4. Specify the `Terrasoft.Nui.ServiceModel.WebService.BaseService` class as a
      parent class.
   5. Add the `[ServiceContract]` and
      `[AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]`
      attributes to the class.

5. Implement a class method.

Add the `public string GetAmount(int value1, int value2)` method that implements
the endpoint of the custom web service to the class in the Schema Designer. The
`GetAmount(int, int)` method adds two values passed as parameters.

View the source code of the `UsrAmountService` custom web service below.

UsrAmountService

         namespace Terrasoft.Configuration
         {
         using System.ServiceModel;
         using System.ServiceModel.Activation;
         using System.ServiceModel.Web;
         using Terrasoft.Core;
         using Terrasoft.Web.Common;

             [ServiceContract]
             [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
             public class UsrAmountService : BaseService
             {

                 [OperationContract]
                 [WebGet(RequestFormat = WebMessageFormat.Json, BodyStyle = WebMessageBodyStyle.Wrapped, ResponseFormat = WebMessageFormat.Json)]
                 public string GetAmount(int value1, int value2) {
                     /*
                     // Create a source class instance using the class factory.
                     var originalObject = Terrasoft.Core.Factories.ClassFactory.Get<UsrOriginalClass>();

                     // Retrieve the GetAmount() method output. Pass the values of the page input fields as parameters.
                     int result = originalObject.GetAmount(value1, value2);

                     // Display the results on the page.
                     return string.Format("The result value, retrieved after calling the replacement class method: {0}", result.ToString());
                     */

                     /*
                     // Create a replacing class instance using the replaced objects factory.
                     // Pass the instance of the class constructor argument as the parameter of the factory method.
                     var substObject = Terrasoft.Core.Factories.ClassFactory.Get<UsrOriginalClass>(new Terrasoft.Core.Factories.ConstructorArgument("rateValue", 2));

                     // Retrieve the GetAmount() method output. Pass the values of the page input fields as parameters.
                     int result = substObject.GetAmount(value1, value2);

                     // Display the results on the page.
                     return string.Format("The result value, retrieved after calling the replaceable class method: {0}", result.ToString());
                     */

                     /* Create a replacing class instance using the new() operator. */
                     var substObjectByNew = new UsrOriginalClass();

                     /* Create a replacing class instance using the replaced objects factory. */
                     var substObjectByFactory = Terrasoft.Core.Factories.ClassFactory.Get<UsrOriginalClass>(new Terrasoft.Core.Factories.ConstructorArgument("rateValue", 2));

                     /* Retrieve the GetAmount() method output. Do not use replacement, call the UsrOriginalClass method. */
                     int resultByNew = substObjectByNew.GetAmount(value1, value2);

                     /* Retrieve the GetAmount() method output. Call the method of the SubstituteClass class that replaces the UsrOriginalClass class. */
                     int resultByFactory = substObjectByFactory.GetAmount(value1, value2);

                     /* Display the results on the page. */
                     return string.Format("Result without class replacement: {0}; Result with class replacement: {1}", resultByNew.ToString(), resultByFactory.ToString());
                 }
             }

         }



The code provides examples of creating a replacing class both using the replaced
objects factory and using the `new()` operator.

6. **Publish the schema**.

As a result, Creatio will add the custom `UsrAmountService` REST web service
that has the `GetAmount` endpoint.

## Outcome of the example​

To call the custom web service, access the `GetAmount` endpoint of the
`UsrAmountService` web service in the browser and pass 2 arbitrary numbers as
`value1` and `value2` parameters.

Request string

    http://mycreatio.com/0/rest/UsrAmountService/GetAmount?value1=25&value2=125

The `GetAmountResult` property will return the custom web service results
executed both using and not using the class replacement.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ExampleClassReplacement/7.18/scr_result.png)

---

## Resources​

[Packages with example implementation (replaced class and web service)](https://academy.creatio.com/sites/default/files/documents/downloads/SDK/Packages/sdkSubstitutableClassPackage_2021-08-30_14.09.53.zip)

[Packages with example implementation (replacing class)](https://academy.creatio.com/sites/default/files/documents/downloads/SDK/Packages/sdkSubstituteClassPackage_2021-08-30_14.10.34.zip)

- 1\. Implement the replaced class
- 2\. Implement a replacing class
- 3\. Implement a custom web service
- Outcome of the example
- Resources
