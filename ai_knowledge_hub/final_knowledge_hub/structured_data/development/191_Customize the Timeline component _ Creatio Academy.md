# Customize the Timeline component | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 714 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/overview

## Description

Use the Timeline component to enable users to view the history of communication
regarding the record as well as records linked to it in chronological order.
Users can like and comment feed records in the timeline. Learn more: Overview of
Freedom UI Designer and its elements (user documentation).

## Key Concepts

configuration, freedom ui, database, package, case, no-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

Use the **Timeline** component to enable users to view the history of
communication regarding the record as well as records linked to it in
chronological order. Users can like and comment feed records in the timeline.
Learn more:
[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?ver=8.3&id=2376&anchor=title-2230-104)
(user documentation).

## Customize an object column to display in the Timeline component​

Out of the box, the timeline displays the primary display value and creation
date of linked records. You can customize the columns to display in the timeline
addon of the relevant object using no-code tools.

To customize an object column to display in the Timeline component:

1. Make sure that the object includes the column to customize and the **Show in
   Timeline component by default checkbox is selected**. Otherwise, preconfigure
   the object.
   1. Create an object schema or replacing object schema. To do this, follow the
      instructions:
      [Object](https://academy.creatio.com/documents?ver=8.3&id=15107). For
      example, create a replacing schema of the `Case` object.

   2. Add a column.
      1. Click
         ![add_button](https://academy.creatio.com/docs/sites/default/files/inline-images/scr_add_button.png)
         in the context menu of the **Columns** node of the object structure.
         This opens a menu.
      2. Select a column type.
      3. Fill out the column properties in the Object Designer.

For example, add the **Some custom column** column (`UsrCustomColumn` code).

     3. Display an additional object in the **Timeline** component.

        1. Open the **Timeline** node of the object structure.
        2. Select the **Show in Timeline component by default** checkbox.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TimelineCustomColumns/8.0/scr_ShowInTimelineComponentByDefault_checkbox.png)

     4. Save the changes. This adds the `UsrCaseTimelineEntity` addon schema.

2. **Set up the column layout** of the relevant object in the `Timeline`
   component.
   1. Open the `UsrCaseTimelineEntity` addon schema.

   2. Open the **Modifications package** node of the addon structure.

   3. Set up the column layout of the `Case` object in the `Timeline` component.
      To do this, add the column configuration object to the `ColumnLayouts`
      array of column configuration objects.

| Property | Property value | ColumnName | Code of the column in the `Case` object | ColumnLayout | Column layout |
| -------- | -------------- | ---------- | --------------------------------------- | ------------ | ------------- |

View an example that sets up the **Some custom column** column of the `Case`
object below.

Example that sets up the Some custom column column of the Case object

            {
              "MetaData": {
                "Schema": {
                  ...,
                  "AD4": {
                    "SchemaName": "Case",
                    "TypeColumnUId": "00000000-0000-0000-0000-000000000000",
                    "TimelineEntityValues": [
                      {
                        ...,
                        "ColumnLayouts": [
                          {
                            "ColumnName": "UsrCustomColumn",
                            "ColumnLayout": "{\"column\": 1,\"row\": 2,\"colSpan\": 12,\"rowSpan\": 1}"
                          },
                          ...
                        ]
                      }
                    ]
                  }
                }
              }
            }


The `UsrCustomColumn` starts on column 1 row 2 and spans 12 columns 1 row.

     4. Save the changes.

3. **Update addons**.
   1. Open the `Case` replacing object schema.
   2. Open the **Timeline** node of the object structure.
   3. Clear and select the **Show in Timeline component by default** checkbox.
   4. Save the changes.

4. **Add the Timeline component** to the Freedom UI page. If the page already
   includes the component, re-add it.

**As a result** , the **Some custom column** column of the `Case` object will be
displayed in the **Timeline** component on the Freedom UI page.

## Customize an icon of the Timeline component tile​

1. **Set up the icon** of the relevant object in the `Timeline` component.
   1. Open the `UsrCaseTimelineEntity` addon schema.

   2. Open the **Modifications package** node of the addon structure.

   3. Add the `IconId` property to the configuration object.

| Property | Property value | IconId | Icon ID from the `[SysImage]` database table |
| -------- | -------------- | ------ | -------------------------------------------- |

View an example that sets the tile icon of the `Case` object below.

Example that sets the tile icon of the Case object

            {
              "MetaData": {
                "Schema": {
                  ...,
                  "AD4": {
                    "SchemaName": "Case",
                    ...,
                    "IconId": "78B0D4C5-891D-49A3-A364-0AFC10F2A93A"
                    ...
                  }
                }
              }
            }


To **change the tile icon** , add another value from the `[SysImage]` database
table to the `IconId` property.

     4. Save the changes.

2. **Update addons**.
   1. Open the `Case` replacing object schema.
   2. Open the **Timeline** node of the object structure.
   3. Clear and select the **Show in Timeline component by default** checkbox.
   4. Save the changes.

3. **Add the Timeline component** to the Freedom UI page. If the page already
   includes the component, re-add it.

**As a result** , the tile icon of the `Case` object will be displayed in the
**Timeline** component on the Freedom UI page.

---

## See also​

[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?ver=8.3&id=2376)
(user documentation)

[Object](https://academy.creatio.com/documents?ver=8.3&id=15107)

- Customize an object column to display in the Timeline component
- Customize an icon of the Timeline component tile
- See also
