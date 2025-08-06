# Customize Word reports | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1620 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/classic-ui/ms-word/overview

## Description

A Word report (print-ready documents) is a document that is generated based on
the records of Creatio sections as a \.docx file. For example, reports of the
Contracts section let you print contracts, reports of the Activities\* section
let you print out emails, minutes of meetings, etc. Learn more: Print-ready
reports (user documentation).

## Key Concepts

configuration, freedom ui, section, detail, role, operation, package,
notification, account, no-code

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

Level: beginner

A **Word report (print-ready documents)** is a document that is generated based
on the records of Creatio sections as a \*.docx file. For example, reports of
the **Contracts** section let you print contracts, reports of the **Activities**
section let you print out emails, minutes of meetings, etc. Learn more:
[Print-ready reports](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/category/print-ready-reports)
(user documentation).

Creatio lets you use both basic and custom macros in Word reports. **Macro** is
a tool that lets you convert data retrieved from Creatio into data suitable for
a Word report. Depending on the usage of macros, Creatio lets you create the
following types of Word reports:

- **Simple report**
- **Report that uses basic macros**
- **Report that uses custom macros**

## Set up permissions to the Report setup section​

You can set up permissions to the **Report setup** section on the system
operation level. If a user lacks the permission to access the **Report setup**
section, they receive a notification about the lack of permissions to execute an
operation when trying to load the section. Out of the box, only Creatio
administrators have access to key system operations. Creatio lets you configure
access permissions to system operations for users or user groups. Learn more:
[System operation permissions](https://academy.creatio.com/documents?ver=8.0&id=2000)
(user documentation).

To set up permissions to the **Report setup** section:

1. **Open the Operation permissions section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **Users and administration** → **Operation permissions**.
2. **Select the Access to "Report setup" section** (`CanManageReports` code)
   **system operation**.
3. **Set up the access to the Report setup section**. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_add_button.png)
   and specify the user/role in the **Operation permission** detail.

**As a result** :

- The record will appear on the **Operation permission** detail.
- The **Access level** column of the record will be set to **Yes**.
- Users that have the specified role will have access to the **Report setup**
  section.

## General procedure​

### 1\. Implement custom macros (optional)​

1. **Open the needed app** in the No-Code Designer.

2. **Open the Advanced settings tab** in the No-Code Designer. To do this, click
   ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **Application management** → **Application Hub** → select
   the app → **Advanced settings**.

3. **Create a user-made package** to add the schema. To do this, click
   ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/CreateConfigurationWebService/8.1/btn_create_a_package.png)
   → **Create new package** → fill out the package properties → **Save**.

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

6. **Create the source code schema**. To do this, click **Add** → **Source
   code**.

7. **Fill out the schema properties**.

8. **Apply the changes**.

9. **Add localizable strings**. Instructions:
   [Add a localizable string](https://academy.creatio.com/documents?ver=8.0&id=15272&anchor=title-2174-3).

10. **Implement the business logic**.

11. Add the `Terrasoft.Configuration` namespace or any of its nested namespaces
    in the Schema Designer.

12. Add the namespaces the data types of which to utilize in the class using the
    `using` directive.

13. Add the class name that matches the schema name (the **Code** property).

14. Add an `ExpressionConverterAttribute` attribute that stores the macro tag.
    This macro can be added to a report column while setting up the report
    columns.

View an example of the `ExpressionConverterAttribute` attribute that stores the
`CurrentUser` macro tag below.

Example of the ExpressionConverterAttribute attribute

            [ExpressionConverterAttribute("CurrentUser")]


     5. Implement the `IExpressionConverter` interface in the class.

     6. Implement the `Evaluate(object value, string arguments = "")` interface method. The method receives a field value from a report template as a parameter. The method returns a value of the `string` type that replaces the corresponding column in the generated report.

11. **Publish the schema**.

### 2\. Create a report​

1. **Open the Report setup section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **Report setup**.

2. **Click New report**.

3. **Fill out the report properties**.

| Property | Property description | Report name | An arbitrary report name that is displayed on the toolbar. Required. | Object | The section object for which Creatio will generate a report. For example, to generate a report for **Accounts** section, set the **Object** property to "Account." Required. | Type | Report type. The property is populated automatically using the "MS Word" value and is non-editable. Required. | Show in the list view | Select the checkbox to generate a report from the section if needed. For example, select the checkbox if you need to generate a report from the **Accounts** section whose object is selected in the **Object** property. | Show in the record page | Select the checkbox to generate a report from the record page if needed . For example, select the checkbox if you need to generate a report from the account page whose object is selected in the **Object** property. |
| -------- | -------------------- | ----------- | -------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

4. **Apply the changes**.

**As a result** , Creatio will add the report to the **Report setup** section.

### 3\. Set up the report columns​

1. **Add the report columns**.
   1. Go to the **Set up report data** block.
   2. Add the column of account name. To do this, click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BasicMacros/scr_AddButton.png)
      → open the **Column** field → select the corresponding column → click
      **Select**.

If you need to use custom macros, add the **Id** column.

2. **Add the macro tag** to the column if needed.
   1. Open the setting page of the needed column. To do this, go to the **Set up
      report data** block and double-click the column or click
      ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/BasicMacros/8.1/btn_edit.png)
      in the column row.

   2. Go to the **Title** property.

   3. Add the macro tag to the column. Creatio lets you add both basic and
      custom macros.

View the structure of macro to use in Word reports below.

Structure of macro in Word reports

            ColumnName[#MacroTag|Parameters#]


Creatio lets you add basic macros to different columns and custom macros to the
**Id** column only. Learn more:
[Basic macros to use in Word reports](https://academy.creatio.com/documents?ver=8.0&id=15139).

     4. Save the changes.

3. **Apply the changes**.

### 4\. Set up the report template​

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
   3. Select the corresponding report.
   4. Click **OK**. This closes the **Creatio Word reports** window and opens
      the **Word report data** panel that includes data of the report created in
      the Creatio instance.

5. **Set up the template layout** based on your business goals.

### 5\. Upload the file of report template to Creatio​

1. **Open the Creatio tab**.
2. **Click Save to Creatio**.

**As a result** , the template file of the corresponding report will be uploaded
to the report page in Creatio.

### 6\. Set up how to display the report​

1. **Add the report to the section page** if needed.
   1. Open the **list page**. To do this, click
      ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
      in the top right → **Application management** → **Application Hub** →
      select the needed app → select the list page.

   2. Add a button that opens reports.
      1. Add a **Button** type component to the toolbar of the Freedom UI
         Designer.

      2. Click
         ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png)
         and fill out the button properties.

| Element | Property | Property value | Button that opens reports | Title | Print report | Action | Print report | Which data to print? | Select needed data |
| ------- | -------- | -------------- | ------------------------- | ----- | ------------ | ------ | ------------ | -------------------- | ------------------ |

     3. Save the changes.

2. **Add the report to the record page** if needed.
   1. Open the **form page**. To do this, click
      ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
      in the top right → **Application management** → **Application Hub** →
      select the needed app → select the form page.

   2. Add a button that opens reports.
      1. Add a **Button** type component to the toolbar of the Freedom UI
         Designer.

      2. Click
         ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png)
         and fill out the button properties.

| Element | Property | Property value | Button that opens reports | Title | Print report | Action | Print report | Print settings | Select "Print report for the current record" or "Print report for the records list" depending on your business goals |
| ------- | -------- | -------------- | ------------------------- | ----- | ------------ | ------ | ------------ | -------------- | -------------------------------------------------------------------------------------------------------------------- |

     3. Save the changes.

**As a result** :

- Creatio will add the **Print report** button that lets you open reports from
  the section page.
- Creatio will add the **Print report** button that lets you open reports from
  the record page.

### 7\. Bind the report to the package​

Instructions:
[Manual data binding](https://academy.creatio.com/documents?ver=8.0&id=15123&anchor=title-3927-17).

---

## See also​

[Print-ready reports](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/category/print-ready-reports)
(user documentation)

[System operation permissions](https://academy.creatio.com/documents?ver=8.0&id=2000)
(user documentation)

[Simple package](https://academy.creatio.com/documents?ver=8.0&id=15072)

[Operations with localizable resources](https://academy.creatio.com/documents?ver=8.0&id=15272)

[Bind data to the package](https://academy.creatio.com/documents?ver=8.0&id=15123)

- Set up permissions to the Report setup section
- General procedure
  - 1\. Implement custom macros (optional)
  - 2\. Create a report
  - 3\. Set up the report columns
  - 4\. Set up the report template
  - 5\. Upload the file of report template to Creatio
  - 6\. Set up how to display the report
  - 7\. Bind the report to the package
- See also
