# Implement a custom additional feature | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 2194
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/platform-customization/interface-control-tools/overview

## Description

Feature toggle is a software development technique that manages the additional
feature status in an app. The Feature toggling page includes the list of
out-of-the-box additional features and custom additional features, regardless of
whether you added them using the Feature toggling page or Source code schema.
Feature toggle lets you use continuous integration while preserving the working
capacity of the application and hiding features you are still developing. Learn
more: Manage an existing additional feature.

## Key Concepts

configuration, integration, database, role, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/interface-control-tools/overview)**
(8.3).

Version: 8.2

On this page

Level: intermediate

**Feature toggle** is a software development technique that manages the
additional feature status in an app. The **Feature toggling** page includes the
list of out-of-the-box additional features and custom additional features,
regardless of whether you added them using the **Feature toggling** page or
**Source code** schema. Feature toggle lets you use continuous integration while
preserving the working capacity of the application and hiding features you are
still developing. Learn more:
[Manage an existing additional feature](https://academy.creatio.com/documents?ver=8.2&id=15631).

**General procedure** to implement a custom additional feature differs in the
front-end and back-end.

## 1\. Add a custom additional feature​

Creatio lets you add a custom additional feature in both the front-end and
back-end. If during development you need to add an additional feature that
exists in the front-end to the back-end and vice versa, make sure that you use
the same feature code. An additional feature exists in both front-end and
back-end simultaneously.

### Add a custom additional feature in the front-end​

Add a custom additional feature in the front-end in the following cases:

- You intend to **use the feature only in the front-end**.
- You have **no intent to customize the app using C# code**.
- You have **no need to compile the app**.

Otherwise, add a custom additional feature in the back-end. Read more >>>

If you choose to add a custom additional feature in the front-end, take into
account the following specifics:

- To migrate apps between environments, additionally **bind the additional
  feature and its value** to the app.
- If you use an additional feature in both front-end and back-end
  simultaneously, you **cannot use typified methods in C# code**. Therefore, the
  compiler will not be able to check the spelling of the feature code.

To add a custom additional feature in the front-end:

1. Open the **Feature toggling** page. Instructions:
   [Open the Feature toggling page](https://academy.creatio.com/documents?ver=8.2&id=15631&anchor=title-3459-7).

2. **Add an additional feature**.

3. **Fill out the feature properties**.

| Property | Property description | Code\* | Code of the custom additional feature to add. | Source | Non-editable. Source of the custom additional feature to add. Creatio automatically populates the property using the "DbFeatureProvider" value. | Description | Description of the custom additional feature to add. | Is enabled | The status of the custom additional feature for all users. Instructions: [Change the status of an additional feature for all users](https://academy.creatio.com/documents?ver=8.2&id=15631&anchor=title-3459-3). | State for current user | The status of the custom additional feature for current user. Instructions: [Change the status of an additional feature for a system user or organizational role](https://academy.creatio.com/documents?ver=8.2&id=15631&anchor=title-3459-8). |
| -------- | -------------------- | ------ | --------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

4. **Save the changes**.

**As a result** , Creatio will add the custom additional feature to the
**Feature toggling** page list. The source of the feature will be set to
"DbFeatureProvider."

### Add a custom additional feature in the back-end​

Add a custom additional feature in the back-end in the following cases:

- You intend to **use the feature in both front-end and back-end
  simultaneously**.
- You intend to **use typified methods in C# code**.
- You have **no need to manage the status of an additional feature for a Creatio
  system user or organizational role**.

Otherwise, add a custom additional feature in the front-end. Read more >>>

If you choose to add a custom additional feature in the back-end, take into
account the following specifics:

- You need to **implement the Source code schema**.
- You need to **compile the app**.

Creatio lets you omit adding a custom additional feature in the back-end in one
of the following cases:

- The out-of-the-box value of a custom additional feature is disabled.
- You need to use the custom additional feature only in the front-end.

To add a custom additional feature in the back-end:

1. If needed, **implement a Source code schema**. Instructions:
   [Implement the source code](https://academy.creatio.com/documents?ver=8.2&id=15108&anchor=title-2123-8).

2. **Add an additional feature**.
   1. Declare a custom class that inherits from the `FeatureMetadata` class.
   2. Specify the values of the feature properties.

View the template to add the custom additional feature in the back-end below.

Template to add the custom feature (back-end)

    #region Class: SomeCustomFeature
    internal class SomeCustomFeature : FeatureMetadata {

        #region Constructors: Public
        public SomeCustomFeature() {
            IsEnabled = true;
            Description = "Some feature description";
        }
        #endregion

    }
    #endregion

Additionally, Creatio lets you **group multiple additional features**. For
example, group additional features by the company that implemented them or by
the app functionality that they affect. To do this:

     1. Declare a grouping class.
     2. Declare a custom class that inherits from the `FeatureMetadata` class. Declare a class for each feature. This lets you reduce the time required to implement the business logic that retrieves the feature statuses.
     3. Specify the property values for each feature.

View the template to group the custom additional features in the back-end below.

Template to group the custom features (back-end)

    namespace Terrasoft.SomeFunctionality {

        using Creatio.FeatureToggling;

        #region Class: SomeModuleFeatures
        public class SomeModuleFeatures {

            #region Class: SomeCustomFeature1
            public class SomeCustomFeature1 : FeatureMetadata {

                #region Constructors: Public
                public SomeCustomFeature1() {
                    IsEnabled = true;
                    Description = "Some feature 1 description";
                }

                #endregion

            }

            #endregion

            #region Class: SomeCustomFeature2
            public class SomeCustomFeature2 : FeatureMetadata {

                #region Constructors: Public
                public SomeCustomFeature2() {
                    IsEnabled = true;
                    Description = "Some feature 2 description";
                }

                #endregion

            }

            #endregion

        }

        #endregion

    }

3. **Publish the schema**.

## 2\. Implement the business logic of the feature​

You can implement the business logic of the custom feature in the front-end or
in the back-end.

### Implement the business logic of the feature in the front-end​

1. **Implement a view model schema**. Instructions:
   [View model schema](https://academy.creatio.com/documents?ver=8.2&id=15106&anchor=title-2123-15).

2. **Implement the method** that defines the behavior of the custom additional
   feature.
   1. Implement the conditional operator that checks the feature status (i. e.
      the `[FeatureState]` column value from the `[AdminUnitFeatureState]`
      database table) and specifies Creatio behavior for each feature status.

   2. Implement the following methods.

| Method | Method description | getIsEnabled() | Checks whether the custom feature is disabled. Retrieves the feature code. The business logic to execute depends on the retrieved value. | getIsDisabled() | Checks whether the custom feature is disabled. Retrieves the feature name. The business logic to execute depends on the retrieved value. |
| ------ | ------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

View the template to implement the behavior of the custom additional feature in
the front-end below.

Template to implement the custom feature behavior (front-end)

    /* Method that implements the business logic based on the value of the custom additional feature. */
    someMethod: function() {

        /* Check whether the custom feature is enabled. */
        if (Terrasoft.Features.getIsEnabled("SomeCustomFeature")) {
            /* Implement the business logic to execute if the custom feature is enabled. */
            ...
        }

        /* Check whether the custom feature is disabled. */
        if (Terrasoft.Features.getIsDisabled("SomeCustomFeature")) {
            /* Implement the business logic to execute if the custom feature is disabled. */
            ...
        }

        /* Implement the business logic of the method using the retrieved value of the custom additional feature. */
        ...
    }

3. **Save the changes**.

4. **Refresh the page**.

5. **Bind the additional feature and its value** to the app.
   1. Create a **Data** schema type. Instructions:
      [Implement a data binding](https://academy.creatio.com/documents?ver=8.2&id=15117&anchor=title-3942-1).

   2. Fill out the schema properties.

| Element to bind | Property value | Binding description | Additional feature | Feature | Binding an additional feature to an app implies binding the additional feature code and additional feature status for all Creatio users. | Status of the additional feature | AdminUnitFeatureState | Optional. Binding a status of the additional feature to an app implies binding the additional feature status for a Creatio system user or organizational role. |
| --------------- | -------------- | ------------------- | ------------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |

     3. Select data to bind to the app.

| Tab | Tab description | Columns setting | Select the columns that contain object data. | Bound data | Select the records to bind to the app. Use the filter by object name to search for corresponding data. |
| --- | --------------- | --------------- | -------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------ |

     4. Save the changes.

**As a result** , the business logic of the custom additional feature will be
implemented in the front-end and associated app functionality will be based on
the feature status.

### Implement the business logic of the feature in the back-end​

1. **Define the needed namespaces** that let you use the `Feature toggle`
   functionality in the source code schemas. To do this, define the
   `Terrasoft.Configuration.FeatureUtilities` and `Creatio.FeatureToggling`
   namespaces.

2. **Implement the method** that defines the behavior of the custom additional
   feature.
   1. Implement the conditional operator that checks the feature status (i. e.
      the `[FeatureState]` column value from the `[AdminUnitFeatureState]`
      database table) and specifies Creatio behavior for each feature status.

   2. Implement the following methods.

Method| Method description| GetIsEnabled()| Checks whether the custom feature is
enabled. Retrieves one of the following values: _ Feature code for the dedicated
custom additional feature. _ Name of the grouping class that groups multiple
custom additional features. The business logic to execute depends on the
retrieved value.| GetIsEnabled<>()| Typified method. Checks whether the custom
feature is enabled. Unlike the `GetIsEnabled()` method, it additionally checks
whether the functionality is implemented correctly. Retrieves one of the
following values: _ Name of the grouping class that groups multiple custom
additional features. _ Name of the dedicated custom additional feature from
grouping class that groups multiple custom additional features. The business
logic to execute depends on the retrieved value.| GetIsDisabled()| Checks
whether the custom feature is disabled. Retrieves the feature code. The business
logic to execute depends on the retrieved value.| GetIsDisabled<>()| Typified
method. Checks whether the custom feature is disabled. Unlike the
`GetIsDisabled()` method, it additionally checks whether the functionality is
implemented correctly. Retrieves one of the following values: _ Name of the
grouping class that groups multiple custom additional features. _ Name of the
dedicated custom additional feature from grouping class that groups multiple
custom additional features. The business logic to execute depends on the
retrieved value.  
---|---

View the template to implement the behavior of the custom additional feature in
the back-end below.

Template to implement the custom additional feature (back-end)

    /* The namespace that lets you manage the feature statuses. */
    using Terrasoft.Configuration;
    using Creatio.FeatureToggling;
    ...
    /* Method that implements the business logic based on the value of the custom additional feature. */
    public void SomeMethod() {

        /* Check whether the dedicated custom feature is enabled. */
        if (Features.GetIsEnabled("SomeCustomFeature")) {
            /* Implement the business logic to execute if the dedicated custom feature is enabled. */
            ...
        }

        /* Check whether the dedicated custom feature is disabled. */
        if (Features.GetIsDisabled("SomeCustomFeature")) {
            /* Implement the business logic to execute if the dedicated custom feature is disabled. */
            ...
        }

        /* Implement the business logic of the method using the retrieved value of the dedicated custom additional feature. */
        ...
    }

View the template to implement the behavior of multiple custom additional
features that are grouped by grouping class in the back-end below.

Template to implement the grouped multiple custom additional features (back-end)

    /* The namespace that lets you manage the feature statuses. */
    using Terrasoft.Configuration;
    using Creatio.FeatureToggling;
    ...
    /* Method that defines the feature. */
    public void SomeMethod() {

        /* Check whether all grouped multiple custom additional features are enabled. */
        if (Features.GetIsEnabled<SomeModuleFeatures>()) {
            /* Implement the business logic to execute if all grouped multiple custom additional features are enabled. */
            ...
        }

        /* Check whether all grouped multiple custom additional features are disabled. */
        if (Features.GetIsDisabled<SomeModuleFeatures>()) {
            /* Implement the business logic to execute if all grouped multiple custom additional features are disabled. */
            ...
        }

        /* Check whether the dedicated custom feature from the grouping class is enabled. */
        if (Features.GetIsEnabled<SomeModuleFeatures.SomeCustomFeature1>()) {
            /* Implement the business logic to execute if the dedicated custom feature is enabled. */
            ...
        }

        /* Check whether the dedicated custom feature from the grouping class is disabled. */
        if (Features.GetIsDisabled<SomeModuleFeatures.SomeCustomFeature1>()) {
            /* Implement the business logic to execute if the dedicated custom feature is disabled. */
            ...
        }

        /* Implement the business logic of the method using the retrieved value of the custom additional feature. */
    ...
    }

3. **Publish the schema**.

**As a result** , the dedicated custom additional feature or multiple custom
additional features that are grouped by the grouping class will be implemented
in the back-end and associated app functionality will be based on the feature
status.

---

## See also​

[Manage an existing additional feature](https://academy.creatio.com/documents?ver=8.2&id=15631)

[Configuration elements of the Client module type](https://academy.creatio.com/documents?ver=8.2&id=15106)

[Configuration elements of the Source code type](https://academy.creatio.com/documents?ver=8.2&id=15108)

- 1\. Add a custom additional feature
  - Add a custom additional feature in the front-end
  - Add a custom additional feature in the back-end
- 2\. Implement the business logic of the feature
  - Implement the business logic of the feature in the front-end
  - Implement the business logic of the feature in the back-end
- See also
