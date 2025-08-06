# Manage an existing additional feature | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 788 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/interface-control-tools/existing-feature/overview

## Description

Feature toggle is a software development technique that manages the additional
feature status in an app. Learn more: Feature toggle (Wikipedia). The Feature
toggling page includes the list of out-of-the-box additional features and custom
additional features, regardless of whether you added them using the Feature
toggling page or Source code schema. Feature toggle lets you use continuous
integration while preserving the working capacity of the application and hiding
features you are still developing. Creatio stores the additional features in the
database.

## Key Concepts

section, integration, database, role

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

**Feature toggle** is a software development technique that manages the
additional feature status in an app. Learn more:
[Feature toggle](https://en.wikipedia.org/w/index.php?title=Feature_toggle&oldid=1072248468)
(Wikipedia). The **Feature toggling** page includes the list of out-of-the-box
additional features and custom additional features, regardless of whether you
added them using the **Feature toggling** page or **Source code** schema.
Feature toggle lets you use continuous integration while preserving the working
capacity of the application and hiding features you are still developing.
Creatio stores the additional features in the database.

## Open the Feature toggling page​

To open the **Feature toggling** page, **enter the** `CreatioURL/0/Flags`
**URL** in the browser address bar. For example,
`https://mycreatio.com/0/Flags`.

**As a result** , the browser will open the **Feature toggling** page.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/FeatureToggle/8.1/scr_FeatureTogglingPage.png)

| Column | Column description | Code | Code of the additional feature. | Is enabled | The status of the additional feature for all users or user groups. | Is enabled for current user | The status of the additional feature for current user. | Source | Source of the additional feature.Available values | DbFeatureProvider | Records of the `[Feature]` database table. | web.config | Boolean key values from the `<appSettings>` section of the `Web.config` file in Creatio root directory. | Metadata | Additional features added in the source code using the class that inherits from `FeatureMetadata`. | GlobalAppSettings | Boolean properties of the `Terrasoft.Core.GlobalAppSettings` class. Learn more: [.NET class reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.GlobalAppSettings.html). |
| ------ | ------------------ | ---- | ------------------------------- | ---------- | ------------------------------------------------------------------ | --------------------------- | ------------------------------------------------------ | ------ | ------------------------------------------------- | ----------------- | ------------------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

The types of additional feature source are sorted by priority in descending
order.

Description| Description of the additional feature.

The **rules** that determine the status of the additional feature are as
follows:

- If you add an additional feature using the **Feature toggling** page, Creatio
  automatically populates the property using the "DbFeatureProvider" value.

- If you change the status of the additional feature using the **Feature
  toggling** page, refresh the page to apply the changes. Back-end changes to
  the status do not require you to refresh the browser page.

- If an additional feature is not added in Creatio, it is disabled.

- If the status of an additional feature is specified in multiple sources, the
  resulting status is based on the source priority.

View the examples of the additional feature status determined based on multiple
sources below. Can be "1" (enabled) or "0" (disabled).

| Feature source | Resulting feature status | DbFeatureProvider | web.config | Metadata or GlobalAppSettings | 1   | 0   | 0   | 1   | 0   | 1   | 0   | 0   | Not available | 1   | 0   | 1   | Not available | 0   | 1   | 0   |
| -------------- | ------------------------ | ----------------- | ---------- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | ------------- | --- | --- | --- |

## Manage the status of an additional feature​

Important

Changes to the status of an additional feature can affect Creatio operability.
We recommend changing the feature status only if the support team approves it or
you need to test a custom additional feature.

When you change the status of an additional feature, Creatio adds the feature to
the database and changes the **Source** column value to "DbFeatureProvider"
regardless of the way you added the feature.

You can manage the status of an additional feature of the following users:

- all Creatio users
- a system Creatio user or organizational role

### Change the status of an additional feature for all users​

1. **Open the Feature toggling page**. To do this, enter the
   `CreatioURL/0/Shell#Section/AppFeature_ListPage` URL in the browser address
   bar.
2. **Select or clear the Is enabled checkbox** of the additional feature whose
   status to change.
3. **Save the changes**.
4. **Refresh all open pages** of the Creatio instance to apply the updated
   status of the additional feature.

### Change the status of an additional feature for a system user or organizational role​

1. **Open the Feature toggling page**. To do this, enter the
   `CreatioURL/0/Shell#Section/AppFeature_ListPage` URL in the browser address
   bar.
2. **Open the page of the additional feature** whose status to change.
3. **Select the system user or organizational role** to change the feature
   status. To do this, go to the **Admin unit** → click **New** → select the
   system user or organizational role.
4. **Select or clear the Feature state checkbox**.
5. **Save the changes**.
6. **Refresh all open pages** of the Creatio instance to apply the updated
   status of the additional feature.

Important

If the additional feature is enabled for a user, for a user group that includes
the user, or the user is a manager of a user for whom the feature is enabled,
Creatio prevents disabling the additional feature.

Additionally, Creatio lets you manage the status of an additional feature for a
system user using the WorkspaceConsole utility. Instructions:
[Change the feature status](https://academy.creatio.com/documents?ver=8.3&id=15207&anchor=title-2138-17).

---

## See also​

[Manage an existing additional feature](https://academy.creatio.com/documents?ver=8.3&id=15631)

[Implement a custom additional feature](https://academy.creatio.com/documents?ver=8.3&id=15634)

---

## Resources​

[UserConnection class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.UserConnectionProperties.html)
(.NET classes reference)

[Feature toggle](https://en.wikipedia.org/w/index.php?title=Feature_toggle&oldid=1072248468)
(Wikipedia)

[Terrasoft.Core.GlobalAppSettings](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.GlobalAppSettings.html)
(.NET classes reference)

- Open the Feature toggling page
- Manage the status of an additional feature
  - Change the status of an additional feature for all users
  - Change the status of an additional feature for a system user or
    organizational role
- See also
- Resources
