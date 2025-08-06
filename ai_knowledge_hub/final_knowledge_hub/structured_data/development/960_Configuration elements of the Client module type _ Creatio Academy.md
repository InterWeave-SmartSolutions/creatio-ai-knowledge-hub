# Configuration elements of the Client module type | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1524
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/client-module

## Description

A configuration element of the Client module type is a separate functionality
block you can upload and run on demand. The purpose of the client module is
front-end Creatio development.

## Key Concepts

page schema, configuration, freedom ui, section, detail, operation, package,
contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

A configuration element of the **Client module** type is a separate
functionality block you can upload and run on demand. The **purpose** of the
client module is front-end Creatio development.

Client modules have the following **types** :

- Non-visual module. Read more >>>
- Visual module. Read more >>>
- Replacing module. Read more >>>

Learn more:
[Client module types](https://academy.creatio.com/documents?ver=8.3&id=15304&anchor=title-3038-3).

The items of the **Add** drop-down list in the toolbar of the **Configuration**
section workspace represent the client module types you can add in Creatio IDE.

View the client module types in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_AddList.png)

The **Client module** schema type in the **Type** drop-down list in the toolbar
of the **Configuration** section workspace represents the client module. The
client schema is the basis of Creatio configuration. As far as software
implementation is concerned, a schema is a core class inherited from the base
`Schema` class.

View the type of the client module schema in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_TypeList.png)

## Implement a non-visual module​

The **Module** schema type represents the non-visual module.

General procedure to implement a non-visual module:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add a module schema**. To do this, click **Add** → **Module** on the
   section list toolbar. This opens the Module Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_module.png)

4. **Fill out the schema properties**.

| Property | Property value | Property description | Code\* | The schema name | Starts with the prefix. Learn more: [Manage configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-6). Can contain Latin characters and digits. | Title\* | The localizable schema title | The title of the configuration element schema is generated automatically and matches the value of the **Code** property without the prefix. | Package | The user-made package where you create the schema | The property is populated automatically and non-editable. | Description | The localizable schema description |
| -------- | -------------- | -------------------- | ------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------- | --------------------------------------------------------- | ----------- | ---------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_module_properties.png)

5. **Apply the changes**.

If needed, use
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png)
in the properties area to **change the schema properties**.

6. **Fill out the additional properties** (optional). To do this, use
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   in the properties area.

View the additional properties in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_AdditionalProperties.png)

7. **Implement the functionality**. The module name in the `define()` function
   must match the schema name in the **Code** property.

Creatio displays the type of the **error**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
or **warning**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)
– if any – to the left of the row number. Hover over the error type to view a
tooltip with the error description.

8. **Save the changes**.

## Implement a visual module​

Visual modules have the following types:

- Freedom UI page schema. Read more >>>
- View model schema. Read more >>>

The **Module** schema type represents the visual module.

### Freedom UI page schema​

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add a Freedom UI page schema**. To do this, click **Add** → **Freedom UI
   page** on the section list toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_freedom_ui_page.png)

4. **Select a template** of the Freedom UI page to add based on your business
   goals. This opens the Freedom UI Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_FreedomUiPageTemplate.png)

5. **Open the schema properties area**. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_Settings_button.png)
   in the action panel.

6. **Fill out the schema properties**.

| Property | Property value | Property description | Page title | The localizable schema title |     | Code\* | The schema name | Starts with the prefix. Learn more: [Manage configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-6). Can contain Latin characters and digits. | Package | The user-made package where you create the schema | The property is populated automatically and non-editable. | Description | The localizable schema description |
| -------- | -------------- | -------------------- | ---------- | ---------------------------- | --- | ------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------- | --------------------------------------------------------- | ----------- | ---------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_FreedomUiPageProperties.png)

7. **Set up the Freedom UI page** using tools of Freedom UI Designer. Learn
   more:
   [Element setup examples](https://academy.creatio.com/docs/8.x/no-code-customization/category/element-setup-examples)
   (user documentation).

8. **Customize the Freedom UI page** using development tools (optional).
   1. Open the Module Designer. To do this, click
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_SourceCode_button.png)
      → **Save**.

   2. Change the schema properties if needed. To do this, use
      ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png)
      in the properties area.

| Property | Property value | Property description | Code\* | The schema name | Matches the **Code** properties specified in the Freedom UI Designer. | Title\* | The localizable schema title | Matches the **Page title** property specified in the Freedom UI Designer. | Parent object | The object whose properties the module inherits | Creatio populates the property automatically based on the template selected when adding the Freedom UI page in the **Configuration** section. We do not recommend editing the **Parent object** property after you add elements to the schema. This can cause page malfunction. | Package | The user-made package where you create the schema | Matches the **Package** property specified in the Freedom UI Designer. The property is populated automatically and non-editable. | Description | The localizable schema description | Matches the **Description** property specified in the Freedom UI Designer. |
| -------- | -------------- | -------------------- | ------ | --------------- | --------------------------------------------------------------------- | ------- | ---------------------------- | ------------------------------------------------------------------------- | ------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------------------------------- | -------------------------------------------------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_FreedomUiPageConfigurationProperties.png)

     3. Apply the changes.

     4. Fill out the additional properties (optional). To do this, use ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png) in the properties area.

View the additional properties in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_AdditionalProperties_1.png)

     5. Implement the functionality. The module name in the `define()` function must match the schema name in the **Code** property.

Creatio displays the type of the **error**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
or **warning**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)
– if any – to the left of the row number. Hover over the error type to view a
tooltip with the error description.

You can use TypeScript to customize Freedom UI pages.

9. **Save the changes**.

If you set up the page **using only tools of Freedom UI Designer** , save the
changes in Freedom UI Designer.

If you customize the page **using development tools** , save the changes in
Module Designer.

### View model schema​

View model schema has the following types:

- **Page view model**
- **Section view model**
- **Detail (list) view model**
- **Detail (fields) view model**

General procedure to implement the view model schema:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add a module schema**. To do this, click **Add** on the section list
   toolbar → select the type of the view model schema. This opens the Module
   Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_model_view.png)

4. **Fill out the schema properties**.

| Property | Property value | Property description | Code\* | The schema name | Starts with the prefix. Learn more: [Manage configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-6). Can contain Latin characters and digits. | Title\* | The localizable schema title | The title of the configuration element schema is generated automatically and matches the value of the **Code** property without the prefix. | Package | The user-made package where you create the schema | The property is populated automatically and non-editable. | Parent object | The object whose properties the module inherits | Select the parent object in the drop-down list. | Description | The localizable schema description |
| -------- | -------------- | -------------------- | ------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------- | --------------------------------------------------------- | ------------- | ----------------------------------------------- | ----------------------------------------------- | ----------- | ---------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_view_module_properties.png)

5. **Apply the changes**.

If needed, use
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png)
in the properties area to **change the schema properties**.

6. **Fill out the additional properties** (optional). To do this, use
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   in the properties area.

View the additional properties in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_AdditionalProperties_2.png)

7. **Implement the functionality**. The module name in the `define()` function
   must match the schema name in the **Code** property. The view model schema
   inherits from the `BaseModulePageV2` base schema.

Creatio displays the type of the **error**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
or **warning**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)
– if any – to the left of the row number. Hover over the error type to view a
tooltip with the error description.

8. **Save the changes**.

## Implement a replacing module​

The **Replacing view model** schema type represents the replacing module. Learn
more:
[Replace configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15105).

General procedure to implement a replacing module:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add a replacing module schema**. To do this, click **Add** → **Replacing
   view model** on the section list toolbar. This opens the Module Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_replacing_view_module.png)

4. **Select the parent object**.

To replace a section or page with the module, specify the view model schema to
replace in the drop-down list of the **Parent object** \* property. For example,
to create a replacing schema for the **Contacts** section, specify the
`ContactSectionV2` schema as the parent object. After you select the parent
object, Creatio populates other module properties automatically.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_replacing_view_module_properties.png)

5. **Apply the changes**.

If needed, use
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png)
in the properties area to **change the schema properties**.

6. **Fill out the additional properties** (optional). To do this, use
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   in the properties area.

View the additional properties in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_AdditionalProperties_3.png)

7. **Implement the functionality**. The module name in the `define()` function
   must match the schema name in the **Code** property.

Creatio displays the type of the **error**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
or **warning**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)
– if any – to the left of the row number. Hover over the error type to view a
tooltip with the error description.

8. **Save the changes**.

## Use hot keys​

To display the index of available hot keys:

1. **Open the Module Designer**.
2. **Click**
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_Info_Button.png)
   on the toolbar.

| Hot key | Action | Ctrl+A | Select all | Ctrl+Z | Undo | Shift+Ctrl+Z | Redo | Ctrl+F | Find | F3  | Find next | Shift+F3 | Find previous | Shift+Ctrl+F | Replace | Shift+Ctrl+R | Replace all | Ctrl+Y | Delete line | Alt+Left | Go to line start | Alt+Right | Go to line end | Alt+G | Jump to line | F11 | Fullscreen code editor | Esc | Exit fullscreen mode | Ctrl+Space | Call autocomplete | Ctrl+S | Save the changes |
| ------- | ------ | ------ | ---------- | ------ | ---- | ------------ | ---- | ------ | ---- | --- | --------- | -------- | ------------- | ------------ | ------- | ------------ | ----------- | ------ | ----------- | -------- | ---------------- | --------- | -------------- | ----- | ------------ | --- | ---------------------- | --- | -------------------- | ---------- | ----------------- | ------ | ---------------- |

---

## See also​

[Module types](https://academy.creatio.com/documents?ver=8.3&id=15304)

[Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15101)

[Operations in Creatio IDE](https://academy.creatio.com/documents?ver=8.3&id=15107)

[Replace configuration elements](https://academy.creatio.com/documents?ver=8.3&id=15105)

---

## Resources​

[Front-end development](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/front-end-development)

[Element setup examples](https://academy.creatio.com/docs/8.x/no-code-customization/category/element-setup-examples)
(user documentation)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/e-learning/development-creatio-platform)

- Implement a non-visual module
- Implement a visual module
  - Freedom UI page schema
  - View model schema
- Implement a replacing module
- Use hot keys
- See also
- Resources
- E-learning courses
