# Configuration elements of the Source code type | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 702 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/creatio-ide/configuration-elements/source-code-c-sharp

## Description

A configuration element of the Source code type is an entity that implements the
business logic. The element lets you add, delete, and format the C# source code
of new functionality. The purpose of the configuration element of the Source
code type is to enable Creatio back-end development.

## Key Concepts

configuration, section, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/source-code-c-sharp)**
(8.3).

Version: 8.1

On this page

Level: beginner

A configuration element of the **Source code** type is an entity that implements
the business logic. The element lets you add, delete, and format the C# source
code of new functionality. The **purpose** of the configuration element of the
**Source code** type is to enable Creatio back-end development.

The items of the **Add** drop-down list in the toolbar of the **Configuration**
section workspace represent the source code schema you can add in Creatio IDE.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SourceCode/8.0/scr_AddList.png)

The **Source code** type schema in the **Type** drop-down list in the toolbar of
the **Configuration** section workspace represents the configuration element of
the **Source code** type. A schema is the basis of Creatio configuration.

View the **type** of the source code schema in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SourceCode/8.0/scr_TypeList.png)

## Implement the source code​

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).

2. **Select a user-made package** to add the schema.

3. **Add a source code schema**. To do this, click **Add** → **Source code** in
   the section list toolbar. This opens the Source Code Designer.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SourceCode/8.0/scr_AddList.png)

4. **Fill out the schema properties**.

| Property | Property description | Code\* | The schema name. Starts with the prefix. Learn more: [Manage configuration elements](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-6). Can contain Latin characters and digits. | Title\* | The localizable schema title. The title of the configuration element schema is generated automatically and matches the value of the **Code** property without the prefix. | Package | The user-made package where you create the schema. The property is populated automatically and non-editable. | Description | The localizable schema description. |
| -------- | -------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ | ----------- | ----------------------------------- |

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SourceCode/8.0/scr_source_code_properties.png)

5. **Apply the changes**.

If needed, use
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_edit_button.png)
in the properties area to **change the schema properties**.

6. **Fill out the additional properties** (optional). To do this, use
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_add_button.png)
   in the properties area. For source code schema the additional schema property
   is **Localizable strings**.

7. **Implement the functionality**. The name of the class declared in the source
   code must match the schema name in the **Code** property.

Creatio displays the type of the **error**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_error_icon.png)
or **warning**
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_warning_icon.png)
– if any – to the left of the row number. Hover over the error type to view a
tooltip with the error description.

8. **Publish the schema**.

## Implement a replacing class​

The **Source code** schema type represents the replacing class. Learn more about
replacing configuration elements:
[Replace configuration elements](https://academy.creatio.com/documents?ver=8.1&id=15105).
The class replacement principle, including the creation and use of replaced
class instances in the configuration, has unique features.

To implement a replacing class:

1. **Repeat steps 1-6** of the procedure to
   [implement the source code](https://academy.creatio.com/documents?ver=8.1&id=15108&anchor=title-2123-8).

2. **Implement the functionality**. The name of the class declared in the source
   code must match the schema name in the **Code** property.
   1. Create the class to inherit the replaced class.

   2. Add the `[Override]` attribute to the class. Learn more about the
      attribute:
      [`[Override]` attribute](https://academy.creatio.com/documents?ver=8.1&id=15221&anchor=title-1238-6).

   3. Implement the functionality that distinguishes the replacing class from
      the replaced class. For example, implement properties and methods that
      expand the functionality of the replaced class, method overloads of the
      replaced class, etc.

   4. Add the `override` modifier to the replacing class’s properties and
      methods.

In a base class, you can replace only virtual methods or implement abstract
methods. The replacing properties and methods declared without the `override`
keyword are unavailable before the compilation. The
[Ninject](http://www.ninject.org/) open-source dependency injection framework
binds and injects type dependencies only during the execution.

     5. Add the `virtual` modifier to the replaced class’s properties and methods to replace.

3. **Publish the schema**.

## Use hot keys​

To display the index of available hot keys:

1. **Open the Source Code Designer**.
2. **Click**
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/8.0/scr_Info_Button.png)
   on the toolbar.

| Hot key | Action | Ctrl+A | Select all | Ctrl+Z | Undo | Shift+Ctrl+Z | Redo | Ctrl+F | Find | F3  | Find next | Shift+F3 | Find previous | Shift+Ctrl+F | Replace | Shift+Ctrl+R | Replace all | Ctrl+Y | Delete line | Alt+Left | Go to line start | Alt+Right | Go to line end | Alt+G | Jump to line | F11 | Fullscreen code editor | Esc | Exit fullscreen mode | Ctrl+Space | Call autocomplete | Ctrl+S | Save the changes |
| ------- | ------ | ------ | ---------- | ------ | ---- | ------------ | ---- | ------ | ---- | --- | --------- | -------- | ------------- | ------------ | ------- | ------------ | ----------- | ------ | ----------- | -------- | ---------------- | --------- | -------------- | ----- | ------------ | --- | ---------------------- | --- | -------------------- | ---------- | ----------------- | ------ | ---------------- |

---

## See also​

[Creatio IDE overview](https://academy.creatio.com/documents?ver=8.1&id=15101)

[Replace configuration elements](https://academy.creatio.com/documents?ver=8.1&id=15105)

---

## Resources​

[Official Ninject website](http://www.ninject.org/)

[Back-end development](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/category/back-end-development)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/e-learning/development-creatio-platform)

- Implement the source code
- Implement a replacing class
- Use hot keys
- See also
- Resources
- E-learning courses
