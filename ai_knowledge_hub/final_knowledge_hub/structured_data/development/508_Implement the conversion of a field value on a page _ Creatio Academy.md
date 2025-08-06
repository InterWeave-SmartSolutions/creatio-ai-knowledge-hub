# Implement the conversion of a field value on a page | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 763
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/customize-page-fields/examples/implement-the-field-value-conversion

## Description

To implement the example:

## Key Concepts

business process, freedom ui, section, operation, package, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/customize-page-fields/examples/implement-the-field-value-conversion)**
(8.3).

Version: 8.0

On this page

Level: intermediate

To implement the example:

1. Set up the page UI. Read more >>>
2. Set up the field conversion. Read more >>>

Example

Add a converter that converts the **Name** field value to uppercase on the
custom converter page. Display the converted value in the **Label** type
component.

![](https://academy.creatio.com/docs/sites/academy_en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ImplementTheFieldValueConversion/8.0/scr_result.png)

## 1\. Set up the page UI​

1. **Create an app** based on the **Records & business processes** template.
   Instructions:
   [Create an app manually](https://academy.creatio.com/documents?ver=8.0&id=2377&anchor=title-2232-6)
   (user documentation).

For this example, create a **Converters** app.

2. **Open the form page** in the Freedom UI Designer.

For this example, open **Converters form page** that includes the **Name** field
out of the box.

3. **Add a label**.

For this example, add a label that contains the converted value of the **Name**
field.

To do this:

     1. Add a label to the working area of the Freedom UI Designer.

     2. Click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png) and fill out the label properties.

| Element | Property | Property value | Label that contains the converted value of a username | Text | Converted value of a username | Style | Body |
| ------- | -------- | -------------- | ----------------------------------------------------- | ---- | ----------------------------- | ----- | ---- |

4. **Save the changes**.

## 2\. Set up the field conversion​

Configure the business logic in the Client Module Designer. For this example,
set up the field value conversion.

1. **Open the source code** of the Freedom UI page. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_SourceCode_button.png).

2. **Implement a converter**.
   1. Go to the `converters` schema section.
   2. Implement a `usr.ToUpperCase` custom converter that converts the value to
      uppercase.

converters schema section

    converters: /**SCHEMA_CONVERTERS*/{
        /* Implement a custom converter that converts the value to uppercase. */
        "usr.ToUpperCase": function(value) {
            return value?.toUpperCase() ?? '';
        }
    }/**SCHEMA_CONVERTERS*/,

3. **Bind an attribute to the label**.
   1. Go to the `viewConfigDiff` schema section → `UsrName` element.
   2. Add an `UsrName` attribute to the `caption` property.
   3. Bind the `usr.ToUpperCase` converter to the `$UsrName` attribute.

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        ...,
        /* Label that contains the converted value of a username. */
        {
            "operation": "insert",
            "name": "UsrLabel",
            "values": {
                ...,
                /* Bind the "usr.ToUpperCase" converter to the "$UsrName" attribute. */
                "caption": "$UsrName | usr.ToUpperCase",
                ...,
            },
            ...
        }
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

4. **Save the changes**.

## View the result​

1. **Open the Requests section**.
2. **Create a request** that has an arbitrary name. For example, "Converter's
   name."

**As a result** , Creatio will convert the **Name** field value to uppercase and
display it in the **Label** type component.
[View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15360&anchor=view-result)

## Source code​

UsrAppConverters_FormPage

    /* Declare the AMD module. */
    define("UsrAppConverters_FormPage", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {
        return {
            viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
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
                },
                /* Label that contains the converted value of a username. */
                {
                    "operation": "insert",
                    "name": "Label",
                    "values": {
                        "layoutConfig": {
                            "column": 1,
                            "row": 2,
                            "colSpan": 1,
                            "rowSpan": 1
                        },
                        "type": "crt.Label",
                        /* Bind the "usr.ToUpperCase" converter to the "$UsrName" attribute. */
                        "caption": "$UsrName | usr.ToUpperCase",
                        "labelType": "headline",
                        "labelThickness": "normal",
                        "labelEllipsis": false,
                        "labelColor": "#181818",
                        "labelBackgroundColor": "transparent",
                        "labelTextAlign": "start"
                    },
                    "parentName": "LeftAreaProfileContainer",
                    "propertyName": "items",
                    "index": 1
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
                            "entitySchemaName": "UsrAppConverters"
                        }
                    }
                }
            }/**SCHEMA_MODEL_CONFIG*/,
            handlers: /**SCHEMA_HANDLERS*/[]/**SCHEMA_HANDLERS*/,
            converters: /**SCHEMA_CONVERTERS*/{
                /* Implement a custom converter that converts the value to uppercase. */
                "usr.ToUpperCase": function(value) {
                    return value?.toUpperCase() ?? '';
                }
            }/**SCHEMA_CONVERTERS*/,
            validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
        };
    });

---

## Resources​

[Package with example implementation](https://academy.creatio.com/docs/sites/academy_en/files/packages/ImplementTheFieldValueConversion/8.0/AppConverters_2022-03-16_06.10.10.zip)

- 1\. Set up the page UI
- 2\. Set up the field conversion
- View the result
- Source code
- Resources
