# Sales rep visit actions | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 409 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.0/more-apps/field-management/sales-rep-visit-actions

## Description

Field Management for Creatio manages sales rep’s "to-do" list during the visits
and records results of each activity For that, the field staff member uses a
mobile device with Creatio mobile app. We recommend that sales reps use tablets
for the best experience when working in the field. Visit pages are most
informative when viewed in horizontal layout.

## Key Concepts

section, detail, lookup, role, mobile app, synchronization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/overview/platform-overview)** (8.3).

Version: 8.0

On this page

Field Management for Creatio manages sales rep’s "to-do" list during the visits
and records results of each activity For that, the field staff member uses a
mobile device with Creatio mobile app. We recommend that sales reps use tablets
for the best experience when working in the field. Visit pages are most
informative when viewed in horizontal layout.

Important

Only the users with the "Field employees" role can use the field features in the
mobile app.

The list of actions that must be performed during a visit is stored on the
**Visit actions** detail of the visit page. For example, according to the rule
of the visit, the sales rep has to perform the following actions: check-in,
presentation, order placement and check-out. Use the **Field visit rules**
lookup to customize the list of visit actions.

To perform an action during a visit:

1. Open the visit page.

2. On the **Visit actions** detail, set the switcher next to the needed action
   to the "Completed" position.

The switcher of a completed action is highlighted in blue.

As a result, the visit action will be considered completed. You can finish the
visit once all required actions are completed (you can skip optional visit
actions). A field employee cannot complete a required action unless all
preceding required actions on the agenda have been completed. Once the last
required action is completed, the visit is considered finished. The action that
is not required can be skipped.

All visit actions are available in the
[offline mode](https://academy.creatio.com/documents?id=1390#title-773-5) of the
mobile app. When working offline, you do not need to maintain constant Internet
connection. It is required to periodically synchronize the mobile application
with the main application to save the changes made when using the mobile device
on the Creatio server.

To synchronize the mobile application with the main application:

1. Make sure that the mobile device has established an Internet connection.

2. Open the **Settings** section of the mobile application.

3. On the opened page, click the **Synchronization** button.

As a result, the data from the primary application will be displayed in the
mobile app and the primary application will display the records that were
created using the mobile app.

---

## See also​

[Install Field Management for Creatio](https://academy.creatio.com/documents?id=1374)

[Set up visit rules and actions for sales reps](https://academy.creatio.com/documents?id=2332)

[Schedule sales rep visits](https://academy.creatio.com/documents?id=2333)

[Check-in verification for sales reps](https://academy.creatio.com/documents?id=2335)

- See also
