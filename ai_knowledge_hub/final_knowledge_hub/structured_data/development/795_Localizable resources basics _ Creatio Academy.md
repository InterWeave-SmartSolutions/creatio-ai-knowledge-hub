# Localizable resources basics | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1803 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/localizable-resources/overview

## Description

Localizable resources are resources required to display Creatio UI in the user's
profile language. Localizable resources include images and localizable strings.

## Key Concepts

configuration, section, detail, database, operation, package, contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

**Localizable resources** are resources required to display Creatio UI in the
user's profile language. Localizable resources include images and localizable
strings.

Localizable resources are a part of Creatio configuration resources. Creatio
resources are contained in
[packages](https://academy.creatio.com/documents?ver=8.3&id=15121) and bound to
the base schema. When you request resources from a specific schema, Creatio
collects them based on package hierarchy, levels, and positions.

Localizable resources utilize the concepts of primary and additional language.

The **primary language** (primary language culture) is the default Creatio UI
language.

The **additional language** (additional language culture) is the Creatio UI
language that was changed in the user profile and is different from the primary
language.

To **change the primary language** , activate the new language. Learn more about
activating the UI language:
[Manage UI languages](https://academy.creatio.com/documents?ver=8.3&id=1624&anchor=title-2568-1)
(user documentation).

The Section and Detail Wizards, Process and Case Designers, and the
**Translation** section use every language installed in Creatio. In other cases,
only activated languages (i. e., languages for which the **Active** checkbox is
selected) are available. This separation decreases the task execution time, for
example, logging in, opening the record page, etc. Learn more in the user
documentation:
[Manage UI languages](https://academy.creatio.com/documents?ver=8.3&id=1624),
[Localize UI via the **Translation** section](https://academy.creatio.com/documents?ver=8.3&id=1684).

Creatio provides the following localizable resource **types** :

- simple localizable resources
- bound localizable resources

## Display localizable resources​

Creatio displays localizable resources based on the following:

- display mode
- display method

### Display modes of localizable resources​

Creatio implements the following **display modes of localizable resources** :

- design-time mode
- run-time mode

The package hierarchy is applied when displaying localizable resources.

#### Design-time mode​

The **purpose** of design-time mode is to display localizable resources in
Designers and Wizards. In this mode, the localizable resource hierarchy of
configuration element schemas is built only up to the level of the package that
contains the scheme with the requested resources. Creatio builds the hierarchy
based on the localizable package resources that are added to the hierarchy via
[direct connections](https://academy.creatio.com/documents?ver=8.3&id=15246&anchor=title-3515-2).

The example mechanism that displays localizable resources is provided below. The
example uses the `ChildResource: ChildValue` resource of the `ChildSchema`
schema in the `DependentPackage` package. View the package hierarchy in the
figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ConfigurationLocalizableResources/7.18/scr_hierarchy_en.png)

The **resulting resources** for the `ChildSchema` schema in design-time mode are
as follows:

- `BaseResource: BaseValue`
- `ChildResource: ChildValue`

In design-time mode, resources do not depend on the following:

- resources of the `PackageWithReplacedResource1` and
  `PackageWithReplacedResource2` packages because these packages are not
  involved in the hierarchy
- resources of the `PackageWithReplacedChildResource1` and
  `PackageWithReplacedChildResource2` packages because these packages are lower
  in the hierarchy compared to the requested schema

If a start package (the package from which the resource collection starts) is
specified for the requested schema, Creatio generates the resulting set of
resources up to the level of the specified package.

The **resulting resources** for the `ChildSchema` schema up to the level of the
`BottomPackage` package in design-time mode are as follows:

- `BaseResource: BaseValue`
- `ChildResource: ReplacedChildValue2`
- `ChildResource1: Value1`
- `ChildResource2: Value2`

The `ChildResource` value is changed to `ReplacedChildValue2` because the
original resource was replaced in packages that are one level below in the
hierarchy (`Level 2`). The position and name of the package are considered.
Package that has a higher position value is prioritized. Packages that have the
same position value are sorted in alphabetical order.

#### Run-time mode​

The **purpose** of run-time mode is to display localizable resources in Creatio
sections, excluding Designers and Wizards. **Unlike** run-time mode, design-time
mode includes package resources that are not part of the hierarchy in the
resulting resource index when requesting a schema.

The **resulting resources** for the `ChildSchema` schema in run-time mode are as
follows:

- `BaseResource: ReplacedBaseValue2`
- `Resource1: Value1`
- `Resource2: Value2`
- `ChildResource: ReplacedChildValue2`
- `ChildResource1: Value1`
- `ChildResource2: Value2`

### Display methods of localizable resources​

Creatio implements the following **display methods of localizable resources** :

- if a **primary language is active** in the user profile, Creatio displays the
  localizable resource value in the primary language
- if an **additional language is activated** in the user profile and the
  **localizable resource value in this language exists** , Creatio displays the
  localizable resource value in the additional language.
- if an **additional language is activated** in the user profile and the
  **localizable resource value in this language does not exist** , Creatio
  displays the localizable resource value in the primary language

The following **classes** implement the mechanism that displays localizable
resources:

- `Terrasoft.Common.LocalizableString`. Manages localizable strings.
- `Terrasoft.Common.LocalizableImage`. Manages localizable images.

To retrieve the localizable resource values, use the following **properties and
methods** :

- The `Value` property. Returns the localizable object value for the current
  language. If Creatio cannot find the localizable object value for the current
  language, the value for the primary language is returned.
- The `HasValue` property. Returns a flag that specifies whether the localizable
  object has a value for the current language. If Creatio cannot find the
  localizable object value for the current language, the value for the primary
  language is returned.
- The `GetCultureValue()` method. Returns the localizable object value for the
  current language. If Creatio cannot find the localizable object value for the
  current language, the value for the primary language is returned.
- The `HasCultureValue()` method. Returns a flag that specifies whether the
  localizable object has a value for the requested language regardless of the
  primary language.

View the description of the `Terrasoft.Common.LocalizableString` class in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.LocalizableString.html).
View The description of the `Terrasoft.Common.LocalizableImage` class in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.LocalizableImage.html).

## Store localizable resources​

The storing features depend on the localizable resource type.

### Store simple localizable resources​

Creatio can store simple localizable resources in the following **repositories**
:

- **Database**. Stores resources required for Creatio operation. The main
  repository for localizable resources.
- **SVN repository**. Stores resources that must be installed into Creatio or
  transferred among
  [development environments](https://academy.creatio.com/documents?ver=8.3&id=15201&anchor=title-3270-1).
  Pre-export the localizable resources to the SVN repository.

#### Store simple localizable resources in the database​

The `[SysLocalizableValue]` database table stores localizable resources in text
format as "key-value" pairs. Each record is bound to a package and base schema
ID.

View the primary columns of the `[SysLocalizableValue]` database table below.

| Column | Description | Id  | Record ID. | SysPackageId | Package ID. | SysSchemaId | Base schema ID. Populated only for configuration resources. | ResourceManager | Resource manager name. Populated only for core resources. | SysCultureId | Language culture ID. | ResourceType | Resource type. | IsChanged | Flag that specifies whether the user changed the localizable resource. | Key | Localizable resource key. | Value | String resource value. | ImageData | Graphic resource value. |
| ------ | ----------- | --- | ---------- | ------------ | ----------- | ----------- | ----------------------------------------------------------- | --------------- | --------------------------------------------------------- | ------------ | -------------------- | ------------ | -------------- | --------- | ---------------------------------------------------------------------- | --- | ------------------------- | ----- | ---------------------- | --------- | ----------------------- |

If an additional language culture is activated in the user profile, Creatio adds
a corresponding record to the `[SysLocalizableValue]` database table when you
add a localizable resource. Users that have other language cultures can access
the added localizable resource using the **mechanism that duplicates the
resource to the primary language culture**. The purpose of the mechanism is to
create a similar localizable resource record that has a link to the primary
language culture. If the value of the current localizable resource is not
specified for other language cultures, the value of the primary language culture
is displayed.

The `[SysPackageResourceChecksum]` database table stores a **checksum** for each
set of schema resources in the package – schema – culture chain. The checksum
lets you identify resource changes when the package is updated. The checksum
separates schemas from resources, which lets you create translation packages.

#### Store simple localizable resources in the SVN repository​

The `Resources` directory of the SVN repository stores localizable package
resources. Use the directory to create a translation package. A **translation
package** is a package that contains only localizable resources and does not
contain configuration element schemas. A translation package can contain
localizable resources for a schema in a different package.

To store localizable schema resources that have the same name but different
managers, for example, `Entity` and `ClientUnit`, the schema Manager name
without the `SchemaManager` prefix are added to the localizable resources names
of the package. Creatio stores the localizable resources in exported schemas as
\*.xml files.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ConfigurationLocalizableResources/7.18/pkg_resources.png)

### Store bound localizable resources​

The repositories for bound localizable resources and
[simple localizable resources](https://academy.creatio.com/documents?ver=8.3&id=15271&anchor=title-2180-8)
are similar.

#### Store bound localizable resources in the database​

The `[SysPackageDataLcz]` database table stores bound localizable resources.

View the primary columns of the `[SysPackageDataLcz]` database table below.

| Column | Description | Id  | Record ID. | SysPackageSchemaDataId | Binding ID from the `[SysPackageSchemaData]` database table. | SysCultureId | Language culture ID. | Data | Bound localizable data. |
| ------ | ----------- | --- | ---------- | ---------------------- | ------------------------------------------------------------ | ------------ | -------------------- | ---- | ----------------------- |

The storage of bound localizable resources has the following **special
features** :

- If a schema **contains bound localizable resources** , Creatio saves data to
  the `[SysPackageDataLcz]` database table.
- If a schema **does not contain bound localizable resources** , Creatio saves
  data to the `[SysPackageSchemaData]` database table.

A record of the `[SysPackageDataLcz]` database table contains the following
**data** :

- link to the corresponding record ID from the `[SysPackageSchemaData]` database
  table
- link to the corresponding language culture ID from the `[SysCulture]` database
  table

For example, if the Creatio instance uses English and Ukrainian language
cultures, each record of the `[SysPackageSchemaData]` database table corresponds
to two records of the `[SysPackageDataLcz]` database table.

#### Store bound localizable resources in the SVN repository​

The `Data` directory of the SVN repository stores bound localizable resources.

`Data` **directory structure** :

- The `data.json` file. Non-localizable resources.
- The `Localization` directory. Bound localizable resources. The directory
  contains the corresponding files for the language cultures. The file names
  follow this pattern: `data.LanguageCultureCode.json`, for example,
  `data.en-US.json`.

View an example that displays the structure of the stored bound localizable
resources below. The example uses the `Periodicity` schema in the `TryItPackage`
package.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BindDataStructure/7.18/svn_bind_data.png)

## Install bound localizable resources​

The installation of bound localizable resources has the following **special
features** :

- If the schema **does not contain bound localizable resources** , Creatio
  installs the resources into the primary table of the `Entity` object.
- If the schema **contains bound localizable resources** (i. e., the
  `[SysPackageDataLcz]` database table contains the appropriate records),
  Creatio installs the resources into the primary database table of the
  corresponding schema and into the localization table.

The template for the localization table name is as follows:
`[SysPrimaryTableNameLcz]`.

For example, the installation order of the bound localizable resources for the
`ContactType` scheme is as follows:

- non-localizable data is installed into the `[ContactType]` database table
- localizable data is installed into the `[ContactType]` and
  `[SysContactTypeLcz]` database tables

note

Creatio does not add another `Sys` prefix for the localization table that
matches the system table (i. e., the name starts with the `Sys` prefix). For
example, the localization table for the `[SysTestSchema]` database table is
named `[SysTestSchemaLcz]`, not `[SysSysTestSchemaLcz]`.

---

## See also​

[Packages basics](https://academy.creatio.com/documents?ver=8.3&id=15121)

[Manage UI languages](https://academy.creatio.com/documents?ver=8.3&id=1844)
(user documentation)

[Localize UI via the Translation section](https://academy.creatio.com/documents?ver=8.3&id=1684)
(user documentation)

[Data access through ORM](https://academy.creatio.com/documents?ver=8.3&id=15246)

[Environment overview](https://academy.creatio.com/documents?ver=8.3&id=15201)

---

## Resources​

[LocalizableString class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.LocalizableString.html)
(.NET classes reference)

[LocalizableImage class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.LocalizableImage.html)
(.NET classes reference)

- Display localizable resources
  - Display modes of localizable resources
  - Display methods of localizable resources
- Store localizable resources
  - Store simple localizable resources
  - Store bound localizable resources
- Install bound localizable resources
- See also
- Resources
