# Customize toggle panels | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 736 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/platform-customization/freedom-ui/toggle-panel

## Description

Toggle panel layout element lets you add a tab area to the page. Compared to the
similar Tabs element, toggle panel has the following special features:

## Key Concepts

page schema, configuration, freedom ui, section, operation, notification,
low-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/toggle-panel)**
(8.3).

Version: 8.2

On this page

Level: beginner

**Toggle panel** layout element lets you add a tab area to the page. Compared to
the similar **Tabs** element, toggle panel has the following special features:

- Toggle panel is controlled by buttons you can place anywhere on the page.
- You can click the active tab button to hide the panel. Click any tab button to
  display the panel again. The panel is hidden by default.

This lets you save more workspace by placing elements that are usually only
needed on demand, such as a **Feed** or **Attachments** component. Learn more:
[Toggle panel](https://academy.creatio.com/documents?ver=8.2&id=2376&anchor=title-2230-8)
(user documentation).

Creatio lets you add the **Toggle panel** component in the Freedom UI Designer
and set it up in the source code of the Freedom UI page using low-code tools
only. Learn more:
[ButtonTogglePanel component](https://academy.creatio.com/documents?ver=8.2&id=15176).

Out of the box, all tabs are closed. If you open a dedicated tab while working
with section records, Creatio saves previously opened tab for all record pages.

Since version 8.2.1, Creatio lets you display a notification mark for a
dedicated tab of **Toggle panel** component. For example, you can permanently
display the notification mark or display it when the value of some attribute in
the Freedom UI page schema is changed. For example, display the notification
mark on the **Next steps** tab that includes activities and tasks for the
current record when activities and tasks are changed. Creatio displays the
notification mark on the top right corner of the tab.

To display a notification mark for a dedicated tab:

1. **Set up a toggle panel** to display a notification mark for a dedicated tab
   if needed.
   1. Add a toggle panel to the working area of the Freedom UI Designer if
      needed.
   2. Add a tab for which to display a notification mark if needed. To do this,
      click
      ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/icons/8.2/btn_add.png)
      and fill out the tab properties.

2. **Specify properties** of the notification mark.
   1. Go to the `viewConfigDiff` schema section → element whose `type` property
      value is `crt.ButtonToggleGroup`.
   2. Add the `badgeConfig` configuration object.
   3. Fill out the properties of the notification mark. Instructions:
      [ButtonTogglePanel component](https://academy.creatio.com/documents?ver=8.2&id=15176&anchor=badgeConfig).

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        /* Custom toggle panel. */
        {
            "operation": "insert",
            "name": "SomeButtonToggleGroup",
            "values": {
                ...,
                "type": "crt.ButtonToggleGroup",

                /* Properties of the notification mark. */
                "badgeConfig": {
                    "color": "accent",
                    "offset": -4
                },
            },
            ...
        },
        ...
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

3. **Set up how to display the notification mark**.

Creatio lets you permanently display the notification mark or display the
notification mark based on the attribute value.

Permanently display the notification mark

     1. Go to the `viewConfigDiff` schema section → element whose `type` property value is `crt.TabContainer` and for which to display a notification mark.
     2. Add the `badge` configuration object whose `visible` property value is set to `true`.

View an example that permanently displays the notification mark below.

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        /* Custom toggle panel. */
        {
            "operation": "insert",
            "name": "SomeTabContainer",
            "values": {
                ...,
                "type": "crt.TabContainer",

                /* The property that flags the notification mark as visible. */
                "badge": {
                    "visible": true
                },
            },
            ...
        },
        ...
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

Display the notification mark based on the attribute value

     1. Add an attribute. Instructions: [Set up the field display condition](https://academy.creatio.com/documents?ver=8.2&id=15379&anchor=viewModelConfigDiff) (step 2).

     2. Bind the attribute to the tab.

        1. Go to the `viewConfigDiff` schema section → element whose `type` property value is `crt.TabContainer` and for which to display a notification mark.
        2. Bind the model attribute to the `badge` property. The value of this attribute controls whether the tab displays or hides the notification mark. Describe the business logic that changes the attribute value in the `handlers` schema section.

View an example that binds the `visible` property to the `$SomeAttribute`
attribute below.

viewConfigDiff schema section

    viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
        /* Custom toggle panel. */
        {
            "operation": "insert",
            "name": "SomeTabContainer",
            "values": {
                ...,
                "type": "crt.TabContainer",

                /* The property that flags the notification mark as visible. Bound to the "SomeAttribute" attribute. */
                "badge": "$SomeAttribute",
            },
            ...
        },
        ...
    ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

---

## See also​

[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?ver=8.2&id=2376)
(user documentation)

[Customize fields (Freedom UI)](https://academy.creatio.com/documents?ver=8.2&id=15379)

- See also
