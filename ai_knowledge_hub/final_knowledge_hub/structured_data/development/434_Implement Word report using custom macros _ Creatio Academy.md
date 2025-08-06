# Implement Word report using custom macros | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 3532
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/classic-ui/ms-word/examples/create-ms-word-report-custom-macros

## Description

To implement the example:

## Key Concepts

configuration, freedom ui, section, package, contact, account, case, no-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

To implement the example:

1. Implement custom macros. Read more >>>
2. Create a report. Read more >>>
3. Set up the report columns. Read more >>>
4. Set up the report template. Read more >>>
5. Upload the file of report template to Creatio. Read more >>>
6. Set up how to display the report. Read more >>>

Example

Generate the custom "Account summary" Word report from the account page. The
report must include the following account fields:

- **Name**.

- **Type**.

- **Primary contact**.

- **Additional information**.
  - Display the annual revenue for "Customer" account type.
  - Display the number of employees for "Partner" account type.
  - Display an empty string for other account types.

- **Date of report generation**.

- **Employee who generated the report**.

Report for Customer account type

![Report for Customer account type](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_result_for_Customer.png)

Report for Partner account type

![Report for Partner account type](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_result_for_Partner.png)

Report for other account type

![Report for other account type](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_result_for_other_account_type.png)

## 1\. Implement custom macros​

For this example, implement the following custom macros:

- Macro that receives additional information about the account depending on the
  account type.
- Macro that receives date of report generation.
- Macro that receives the name of the employee who generated the report.

### Additional account information​

1. **Open the Customer 360 app** in the No-Code Designer.

2. **Open the Advanced settings tab** in the No-Code Designer. To do this, click
   ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → "Application management" → "Application Hub" → **Customer
   360** app → "Advanced settings."

3. **Create a user-made package** to add the schema. To do this, click
   ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreateConfigurationWebService/8.1/btn_create_a_package.png)
   → **Create new package** → fill out the package properties → **Save**.

For this example, create the `sdkMsWordReportCustomMacros` user-made package.

4. **Add the package properties**.
   1. Open the package properties. To do this, click
      ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/PopulateDeliveryType/8.1/scr_open_properties.png)
      → **Properties**. This opens the **Dependencies** tab on the **Package
      properties** page.
   2. Click **Add** in the **Depends on Packages** block. This opens the
      **Select package** window.
   3. Select the checkbox for the `CrtNUI` package. The `CrtNUI` package
      includes the `ExpressionConverterHelper` schema that implements the basic
      `IExpressionConverter` interface.
   4. Click **Select**.
   5. Apply the changes.

5. **Change the current package**. Instructions:
   [Change the current package](https://academy.creatio.com/documents?ver=8.0&id=15072&anchor=change-the-current-package).

For this example, change the current package to `sdkMsWordReportCustomMacros`
user-made package.

6. **Create the source code schema**. To do this, click **Add** → **Source
   code**.

7. **Fill out the schema properties**.

For this example, use the following schema properties.

| Property | Property value | Code | UsrAccountInfoByAccountType | Title | AccountInfoByAccountType |
| -------- | -------------- | ---- | --------------------------- | ----- | ------------------------ |

8. **Apply the changes**.

9. **Add localizable strings**.

For this example, add the following localizable strings:

     * Localizable string that stores the text to be displayed in the report for the "Customer" account type.
     * Localizable string that stores the text to be displayed in the report for the "Partner" account type.

To do this:

     1. Create a localizable string. To do this, go the **Localizable strings** additional property node and click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/btn_add.png).

     2. Fill out the localizable string properties.

| Element | Property | Property value | Localizable string that stores the text to be displayed in the report for the "Customer" account type | Code | CustomerAccountType | Value | Annual turnover {0} | Localizable string that stores the text to be displayed in the report for the "Partner" account type. | Code | PartnerAccountType | Value | Number of employees {0} persons |
| ------- | -------- | -------------- | ----------------------------------------------------------------------------------------------------- | ---- | ------------------- | ----- | ------------------- | ----------------------------------------------------------------------------------------------------- | ---- | ------------------ | ----- | ------------------------------- |

     3. Save the changes.

10. **Implement the business logic** of receiving additional account information
    depending on the account type.

UsrAccountInfoByAccountType

         namespace Terrasoft.Configuration
         {
             using System;
             using System.CodeDom.Compiler;
             using System.Collections.Generic;
             using System.Data;
             using System.Linq;
             using System.Runtime.Serialization;
             using System.ServiceModel;
             using System.ServiceModel.Web;
             using System.ServiceModel.Activation;
             using System.Text;
             using System.Text.RegularExpressions;
             using System.Web;
             using Terrasoft.Common;
             using Terrasoft.Core;
             using Terrasoft.Core.DB;
             using Terrasoft.Core.Entities;
             using Terrasoft.Core.Packages;
             using Terrasoft.Core.Factories;

             /* Attribute that stores the macro name. */
             [ExpressionConverterAttribute("AccountInfoByAccountType")]

             /* Class that implements the "IExpressionConverter" interface. */
             class UsrAccountInfoByAccountType : IExpressionConverter
             {

                 private UserConnection _userConnection;
                 private string _customerAdditional;
                 private string _partnerAdditional;

                 /* Call localizable string values. */
                 private void SetResources() {
                     string sourceCodeName = "UsrAccountInfoByAccountType";
                     _customerAdditional = new LocalizableString(_userConnection.ResourceStorage, sourceCodeName, "LocalizableStrings.CustomerAccountType.Value");
                     _partnerAdditional =  new LocalizableString(_userConnection.ResourceStorage, sourceCodeName, "LocalizableStrings.PartnerAccountType.Value");
                 }

                 /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
                 public string Evaluate(object value, string arguments = "")
                 {
                     try
                     {
                         _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];
                         Guid accountId = new Guid(value.ToString());
                         return getAccountInfo(accountId);
                     }
                     catch (Exception err)
                     {
                         return err.Message;
                     }
                 }

                 /* Receive additional information based on the account type ID. */
                 private string getAccountInfo(Guid accountId)
                 {
                     SetResources();
                     try
                     {

                         /* Create an "EntitySchemaQuery" instance that has the "Account" root schema. */
                         EntitySchemaQuery esq = new EntitySchemaQuery(_userConnection.EntitySchemaManager, "Account");

                         /* Add columns to the query. */
                         var columnType = esq.AddColumn("Type.Name").Name;
                         var columnNumber = esq.AddColumn("EmployeesNumber.Name").Name;
                         var columnRevenue = esq.AddColumn("AnnualRevenue.Name").Name;

                         /* Filter records by the account ID. */
                         var accountFilter = esq.CreateFilterWithParameters(
                             FilterComparisonType.Equal,
                             "Id",
                             accountId
                         );
                         esq.Filters.Add(accountFilter);

                         /* Retrieve an entity collection. */
                         EntityCollection entities = esq.GetEntityCollection(_userConnection);

                         /* If the collection includes entities, the method returns data depending on the account type. */
                         if (entities.Count > 0)
                         {
                             Entity entity = entities[0];
                             var type = entity.GetTypedColumnValue<string>(columnType);
                             switch (type)
                             {
                                 case "Customer":
                                     return String.Format(_customerAdditional, entity.GetTypedColumnValue<string>(columnRevenue));
                                 case "Partner":
                                     return String.Format(_partnerAdditional, entity.GetTypedColumnValue<string>(columnNumber));
                                 default:
                                     return String.Empty;
                             }
                         }
                         return String.Empty;
                     }
                     catch (Exception err)
                     {
                         throw err;
                     }
                 }
             }
         }


11. **Publish the schema**.

### Date of report generation​

1. **Select a user-made package** to add the schema.

For this example, select the `sdkMsWordReportCustomMacros` user-made package.

2. **Create the source code schema**. To do this, click **Add** → **Source
   code**.

3. **Fill out the schema properties**.

For this example, use the following schema properties.

| Property | Property value | Code | UsrCurrentDate | Title | CurrentDate |
| -------- | -------------- | ---- | -------------- | ----- | ----------- |

4. **Apply the changes**.

5. **Implement the business logic** of receiving date of report generation.

UsrCurrentDate

         namespace Terrasoft.Configuration
         {
             using System;
             using System.CodeDom.Compiler;
             using System.Collections.Generic;
             using System.Data;
             using System.Linq;
             using System.Runtime.Serialization;
             using System.ServiceModel;
             using System.ServiceModel.Web;
             using System.ServiceModel.Activation;
             using System.Text;
             using System.Text.RegularExpressions;
             using System.Web;
             using Terrasoft.Common;
             using Terrasoft.Core;
             using Terrasoft.Core.DB;
             using Terrasoft.Core.Entities;
             using Terrasoft.Core.Packages;
             using Terrasoft.Core.Factories;

             /* Attribute that stores the macro name. */
             [ExpressionConverterAttribute("CurrentDate")]

             /* Class that implements the "IExpressionConverter" interface. */
             class UsrCurrentDate : IExpressionConverter
             {
                 private UserConnection _userConnection;

                 /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
                 public string Evaluate(object value, string arguments = "")
                 {
                     try
                     {
                         _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                         /* Return current date. */
                         return _userConnection.CurrentUser.GetCurrentDateTime().Date.ToString("dd MMM yyyy");
                     }
                     catch (Exception err)
                     {
                         return err.Message;
                     }
                 }
             }
         }


6. **Publish the schema**.

### Employee who generated the report​

1. **Select a user-made package** to add the schema.

For this example, select the `sdkMsWordReportCustomMacros` user-made package.

2. **Create the source code schema**. To do this, click **Add** → **Source
   code**.

3. **Fill out the schema properties**.

For this example, use the following schema properties.

| Property | Property value | Code | UsrCurrentUser | Title | CurrentUser |
| -------- | -------------- | ---- | -------------- | ----- | ----------- |

4. **Apply the changes**.

5. **Implement the business logic** of receiving the name of the employee who
   generated the report.

UsrCurrentUser

         namespace Terrasoft.Configuration
         {
             using System;
             using System.CodeDom.Compiler;
             using System.Collections.Generic;
             using System.Data;
             using System.Linq;
             using System.Runtime.Serialization;
             using System.ServiceModel;
             using System.ServiceModel.Web;
             using System.ServiceModel.Activation;
             using System.Text;
             using System.Text.RegularExpressions;
             using System.Web;
             using Terrasoft.Common;
             using Terrasoft.Core;
             using Terrasoft.Core.DB;
             using Terrasoft.Core.Entities;
             using Terrasoft.Core.Packages;
             using Terrasoft.Core.Factories;

             /* Attribute that stores the macro name. */
             [ExpressionConverterAttribute("CurrentUser")]

             /* Class that implements the "IExpressionConverter" interface. */
             class UsrCurrentUser : IExpressionConverter
             {
                 private UserConnection _userConnection;

                 /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
                 public string Evaluate(object value, string arguments = "")
                 {
                     try
                     {
                         _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                         /* Return the contact of current user. */
                         return _userConnection.CurrentUser.ContactName;
                     }
                     catch (Exception err)
                     {
                         return err.Message;
                     }
                 }
             }
         }


6. **Publish the schema**.

## 2\. Create a report​

1. **Open the Report setup section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **Report setup**.

2. **Click New report**.

3. **Fill out the report properties**.

| Property | Property value | Report name | Account summary | Object | Account | Show in the list view | Clear the checkbox | Show in the record page | Select the checkbox |
| -------- | -------------- | ----------- | --------------- | ------ | ------- | --------------------- | ------------------ | ----------------------- | ------------------- |

4. **Apply the changes**.

**As a result** , Creatio will add the "Account summary" report to the **Report
setup** section.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_report_in_the_report_list.png)

## 3\. Set up the report columns​

1. **Add the report columns**.
   1. Go to the **Set up report data** block.

   2. Add the column of account name. To do this, click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BasicMacros/scr_AddButton.png)
      → open the **Column** field → select **Id** → click **Select**.

The **Id** column is an input parameter for a custom macro.

     3. Add the **Id** , **Name** , **Type** , **Primary contact** and **Id** columns similarly.

As a result, the "Account summary" report data will be as follows.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_report_data.png)

2. **Add the macro tag** to the column.

For this example, add the macro tags to the different **Id** columns. To do
this:

     1. Open the setting page of the **Id** column. To do this, go to the **Set up report data** block and double-click the column or click ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/BasicMacros/8.1/btn_edit.png) in the column row.

     2. Go to the **Title** property.

     3. Add the `[#CurrentDate#]` macro tag to the **Name** column. The `[#CurrentDate#]` macro receives date of report generation.

     4. Add the `[#CurrentUser#]` and `[#AccountInfoByAccountType#]` macro tags to the different **Id** columns similarly.

The `[#CurrentUser#]` macro receives the name of the employee who generated the
report.

The `[#AccountInfoByAccountType#]` macro receives additional information of the
account depending on the account type.

     5. Save the changes.

3. **Apply the changes**.

**As a result** , the "Account summary" report data will be as follows.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_resulted_report_data.png)

## 4\. Set up the report template​

1. **Install the Creatio plug-in for MS Word**. Instructions:
   [Install Creatio plug-in for MS Word](https://academy.creatio.com/documents?ver=8.0&id=1412)
   (user documentation). This is a one-time procedure.

2. **Run the MS Word app**.

3. **Connect to the Creatio instance** that includes the created report.
   1. Open the **Creatio** tab.

   2. Click **Connect**. This opens the **Login** window.

   3. Enter the Creatio user credentials.

   4. Click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BasicMacros/scr_PlusButton.png).
      This opens the **Available Servers** window.

   5. Click **New**. This opens the **Server Connection Setup** window.

   6. Fill out the server properties.

| Property | Property value | Name | An arbitrary server name. For example, "Creatio." | Link | URL of the Creatio instance that includes the created report. For example, `https://mycreatio.com/`. |
| -------- | -------------- | ---- | ------------------------------------------------- | ---- | ---------------------------------------------------------------------------------------------------- |

     7. Click **OK**. This closes the **Server Connection Setup** window.

     8. Click **OK**. This closes the **Available Servers** window and adds the server name to the **Server** field of the **Login** window.

     9. Click **OK**. This closes the **Login** window and connects to the Creatio instance.

4. **Select the report** to set up the template.
   1. Open the **Creatio** tab.
   2. Click **Select report**. This opens the **Creatio Word reports** window.
   3. Select "Account summary" report.
   4. Click **OK**. This closes the **Creatio Word reports** window and opens
      the **Word report data** panel that includes the "Account summary" report
      data set up in the Creatio instance.

5. **Set up the template layout** based on your business goals.

**As a result** , the template of the "Account summary" report will look as
follows.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_report_template.png)

## 5\. Upload the file of report template to Creatio​

1. **Open the Creatio tab**.
2. **Click Save to Creatio**.

**As a result** , the template file of the "Account summary" report will be
uploaded to the report page in Creatio.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_report_template_in_Creatio.png)

## 6\. Set up how to display the report​

Add the report to the account page. To do this:

1. **Open the Accounts form page**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **Application management** → **Application Hub** →
   **Customer 360** → **Accounts form page**.

2. **Add a button** that opens the "Account summary" report.
   1. Add a **Button** type component to the toolbar of the Freedom UI Designer.

   2. Click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png)
      and fill out the button properties.

| Element | Property | Property value | Button that opens the "Account summary" report | Title | Print report | Action | Print report | Print settings | Print report for the current record |
| ------- | -------- | -------------- | ---------------------------------------------- | ----- | ------------ | ------ | ------------ | -------------- | ----------------------------------- |

3. **Save the changes**.

**As a result** , Creatio will add the **Print report** button that lets you
open the "Account summary" report from the account page.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CustomMacros/8.1/scr_Print_button_on_the_account_page.png)

## View the result​

1. **Open the Accounts section**.
2. **Open the page of an arbitrary account**.
3. **Generate the report**. To do this, click **Print report** → **Account
   summary**.
4. **Save the report file** to your device.
5. **Open the report file**.

**As a result** , Creatio will generate the "Account summary" report from the
account page. The **Additional information** field value differs for different
account types:

- For the "Customer" account type, the field will include the annual revenue.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15703&anchor=view-result)
- For the "Partner" account type, the field will include the number of
  employees.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15703&anchor=view-result-1)
- For other account types, the field will include empty string.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15703&anchor=view-result-2)

## Source code​

- UsrAccountInfoByAccountType
- UsrCurrentDate
- UsrCurrentUser

  namespace Terrasoft.Configuration  
  {  
   using System;  
   using System.CodeDom.Compiler;  
   using System.Collections.Generic;  
   using System.Data;  
   using System.Linq;  
   using System.Runtime.Serialization;  
   using System.ServiceModel;  
   using System.ServiceModel.Web;  
   using System.ServiceModel.Activation;  
   using System.Text;  
   using System.Text.RegularExpressions;  
   using System.Web;  
   using Terrasoft.Common;  
   using Terrasoft.Core;  
   using Terrasoft.Core.DB;  
   using Terrasoft.Core.Entities;  
   using Terrasoft.Core.Packages;  
   using Terrasoft.Core.Factories;

      /* Attribute that stores the macro name. */
      [ExpressionConverterAttribute("AccountInfoByAccountType")]

      /* Class that implements the "IExpressionConverter" interface. */
      class UsrAccountInfoByAccountType : IExpressionConverter
      {

          private UserConnection _userConnection;
          private string _customerAdditional;
          private string _partnerAdditional;

          /* Call localizable string values. */
          private void SetResources() {
              string sourceCodeName = "UsrAccountInfoByAccountType";
              _customerAdditional = new LocalizableString(_userConnection.ResourceStorage, sourceCodeName, "LocalizableStrings.CustomerAccountType.Value");
              _partnerAdditional =  new LocalizableString(_userConnection.ResourceStorage, sourceCodeName, "LocalizableStrings.PartnerAccountType.Value");
          }

          /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
          public string Evaluate(object value, string arguments = "")
          {
              try
              {
                  _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];
                  Guid accountId = new Guid(value.ToString());
                  return getAccountInfo(accountId);
              }
              catch (Exception err)
              {
                  return err.Message;
              }
          }

          /* Receive additional information based on the account type ID. */
          private string getAccountInfo(Guid accountId)
          {
              SetResources();
              try
              {

                  /* Create an "EntitySchemaQuery" instance that has the "Account" root schema. */
                  EntitySchemaQuery esq = new EntitySchemaQuery(_userConnection.EntitySchemaManager, "Account");

                  /* Add columns to the query. */
                  var columnType = esq.AddColumn("Type.Name").Name;
                  var columnNumber = esq.AddColumn("EmployeesNumber.Name").Name;
                  var columnRevenue = esq.AddColumn("AnnualRevenue.Name").Name;

                  /* Filter records by the account ID. */
                  var accountFilter = esq.CreateFilterWithParameters(
                      FilterComparisonType.Equal,
                      "Id",
                      accountId
                  );
                  esq.Filters.Add(accountFilter);

                  /* Retrieve an entity collection. */
                  EntityCollection entities = esq.GetEntityCollection(_userConnection);

                  /* If the collection includes entities, the method returns data depending on the account type. */
                  if (entities.Count > 0)
                  {
                      Entity entity = entities[0];
                      var type = entity.GetTypedColumnValue<string>(columnType);
                      switch (type)
                      {
                          case "Customer":
                              return String.Format(_customerAdditional, entity.GetTypedColumnValue<string>(columnRevenue));
                          case "Partner":
                              return String.Format(_partnerAdditional, entity.GetTypedColumnValue<string>(columnNumber));
                          default:
                              return String.Empty;
                      }
                  }
                  return String.Empty;
              }
              catch (Exception err)
              {
                  throw err;
              }
          }
      }

  }

  namespace Terrasoft.Configuration  
  {  
   using System;  
   using System.CodeDom.Compiler;  
   using System.Collections.Generic;  
   using System.Data;  
   using System.Linq;  
   using System.Runtime.Serialization;  
   using System.ServiceModel;  
   using System.ServiceModel.Web;  
   using System.ServiceModel.Activation;  
   using System.Text;  
   using System.Text.RegularExpressions;  
   using System.Web;  
   using Terrasoft.Common;  
   using Terrasoft.Core;  
   using Terrasoft.Core.DB;  
   using Terrasoft.Core.Entities;  
   using Terrasoft.Core.Packages;  
   using Terrasoft.Core.Factories;

      /* Attribute that stores the macro name. */
      [ExpressionConverterAttribute("CurrentDate")]

      /* Class that implements the "IExpressionConverter" interface. */
      class UsrCurrentDate : IExpressionConverter
      {
          private UserConnection _userConnection;

          /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
          public string Evaluate(object value, string arguments = "")
          {
              try
              {
                  _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                  /* Return current date. */
                  return _userConnection.CurrentUser.GetCurrentDateTime().Date.ToString("dd MMM yyyy");
              }
              catch (Exception err)
              {
                  return err.Message;
              }
          }
      }

  }

  namespace Terrasoft.Configuration  
  {  
   using System;  
   using System.CodeDom.Compiler;  
   using System.Collections.Generic;  
   using System.Data;  
   using System.Linq;  
   using System.Runtime.Serialization;  
   using System.ServiceModel;  
   using System.ServiceModel.Web;  
   using System.ServiceModel.Activation;  
   using System.Text;  
   using System.Text.RegularExpressions;  
   using System.Web;  
   using Terrasoft.Common;  
   using Terrasoft.Core;  
   using Terrasoft.Core.DB;  
   using Terrasoft.Core.Entities;  
   using Terrasoft.Core.Packages;  
   using Terrasoft.Core.Factories;

      /* Attribute that stores the macro name. */
      [ExpressionConverterAttribute("CurrentUser")]

      /* Class that implements the "IExpressionConverter" interface. */
      class UsrCurrentUser : IExpressionConverter
      {
          private UserConnection _userConnection;

          /* Implement the "Evaluate()" method of the "IExpressionConverter" interface. */
          public string Evaluate(object value, string arguments = "")
          {
              try
              {
                  _userConnection = (UserConnection)HttpContext.Current.Session["UserConnection"];

                  /* Return the contact of current user. */
                  return _userConnection.CurrentUser.ContactName;
              }
              catch (Exception err)
              {
                  return err.Message;
              }
          }
      }

  }

---

## Resources​

[Package with example implementation](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/packages/CustomMacros/8.1/sdkMsWordReportCustomMacros_2024-09-20_08.40.40.zip)

- 1\. Implement custom macros
  - Additional account information
  - Date of report generation
  - Employee who generated the report
- 2\. Create a report
- 3\. Set up the report columns
- 4\. Set up the report template
- 5\. Upload the file of report template to Creatio
- 6\. Set up how to display the report
- View the result
- Source code
- Resources
