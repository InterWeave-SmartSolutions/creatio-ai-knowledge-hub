# FeatureUtilities class | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 494
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/interface-control-tools/existing-feature/references/featureutilities-class

## Description

The Terrasoft.Configuration namespace.

## Key Concepts

configuration, database

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

The `Terrasoft.Configuration` namespace.

The `Terrasoft.Configuration.FeatureUtilities` class provides a set of extension
methods to the `UserConnection`class. These methods let you use the
`Feature Toggle` functionality in the source code schemas of Creatio back-end.
The `FeatureUtilities` class also declares the enumeration of feature statuses
(the `[FeatureState]` column of the `[AdminUnitFeatureState]` database table).

note

Use the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.FeatureUtilities.html)
to access the `FeatureUtilities` class.

## Methods​

    static int GetFeatureState(this UserConnection source, string code)

Returns the feature status.

Parameters

| source | The user connection. | code | The feature code. |
| ------ | -------------------- | ---- | ----------------- |

    static int GetFeatureState(this UserConnection source, string code, Guid sysAdminUnitId)

Returns the feature status.

Parameters

| source | The user connection. | code | The code of the feature. | sysAdminUnitId | The unique record ID. |
| ------ | -------------------- | ---- | ------------------------ | -------------- | --------------------- |

    static bool GetIsFeatureEnabledForAnyUser(this UserConnection source, string code)

Returns the feature status for any user.

Parameters

| source | The user connection. | code | The code of the feature. |
| ------ | -------------------- | ---- | ------------------------ |

    static bool GetIsFeatureEnabledForAllUsers(this UserConnection source, string code)

Returns the feature status for all users.

Parameters

| source | The user connection. | code | The code of the feature. |
| ------ | -------------------- | ---- | ------------------------ |

    static Dictionary<string, int> GetFeatureStates(this UserConnection source)

Returns all feature statuses.

Parameters

| source | The user connection. |
| ------ | -------------------- |

    static List<FeatureInfo> GetFeaturesInfo(this UserConnection source)

Returns data about all features and their statuses.

Parameters

| source | The user connection. |
| ------ | -------------------- |

    static void SetFeatureState(this UserConnection source, string code, int state, bool forAllUsers = false)

Sets the feature status.

Parameters

| source | The user connection. | code | The code of the feature. | state | The new status of the feature. | forAllUsers | Sets the status of the feature for all users. |
| ------ | -------------------- | ---- | ------------------------ | ----- | ------------------------------ | ----------- | --------------------------------------------- |

    static void SafeSetFeatureState(this UserConnection source, string code, int state, bool forAllUsers = false)

Sets the feature status or creates the feature if it does not exist.

Parameters

| source | The user connection. | code | The code of the feature. | state | The new status of the feature. | forAllUsers | Sets the status of the feature for all users. |
| ------ | -------------------- | ---- | ------------------------ | ----- | ------------------------------ | ----------- | --------------------------------------------- |

    static void CreateFeature(this UserConnection source, string code, string name, string description)

Creates the feature.

Parameters

| source | The user connection. | code | The code of the feature. | name | The name of the feature. | description | The description of the feature. |
| ------ | -------------------- | ---- | ------------------------ | ---- | ------------------------ | ----------- | ------------------------------- |

    static bool GetIsFeatureEnabled(this UserConnection source, string code)

Checks if the feature is turned on.

Parameters

| source | The user connection. | code | The code of the feature. |
| ------ | -------------------- | ---- | ------------------------ |

    static bool GetIsFeatureEnabled(this UserConnection source, string code, Guid sysAdminUnitId)

Checks if the feature is turned off.

Parameters

| source | The user connection. | code | The code of the feature. | sysAdminUnitId | The unique record ID. |
| ------ | -------------------- | ---- | ------------------------ | -------------- | --------------------- |

## FeatureState enumeration​

The `FeatureState` enumeration defines the feature statuses (the
`[FeatureState]` column of the `[AdminUnitFeatureState]` database table).

| Disabled | 0   | The feature is turned off. | Enabled | 1   | The feature is turned on. | Established | 2   | The feature is established. |
| -------- | --- | -------------------------- | ------- | --- | ------------------------- | ----------- | --- | --------------------------- |

- Methods
- FeatureState enumeration
