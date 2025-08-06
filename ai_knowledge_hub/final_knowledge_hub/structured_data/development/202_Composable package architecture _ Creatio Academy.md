# Composable package architecture | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 626 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/packages/composable-architecture

## Description

Creatio has started transfer to composable architecture. During the transition
period, Creatio includes:

## Key Concepts

freedom ui, classic ui, section, package, contact, account, case, customization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/composable-architecture)**
(8.3).

Version: 8.1

On this page

Level: beginner

Creatio has started transfer to composable architecture. During the transition
period, Creatio includes:

- composable package architecture
- classic package architecture

## Classic package architecture​

Classic architecture contains packages version 8.0.5 and earlier. For example,
`ProductCore`, `Base`, etc. View the classic package architecture in the figure
below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/StudioCreatio/8.0/scr_ClassicPackageArchitecture.png)

We recommend using composable architecture packages as classic architecture
packages are obsolete. After the transition to composable architecture, classic
architecture packages packages will be removed.

## Composable package architecture​

As part of transition, Creatio includes a number of new packages for composable
architecture. Composable architecture does not contain classic architecture
packages but has similar packages that have the `Crt` prefix. This is a vendor
prefix Creatio uses for packages and package content developed using Angular.
Packages that have the `Crt` prefix contain app functionality that is identical
to packages in classic architecture. Use composable architecture packages when
you implement Freedom UI apps. Learn more in a separate article:
[Freedom UI app types](https://academy.creatio.com/documents?ver=8.1&id=2417).
Classic UI app functionality developed using ExtJS is stored in dedicated
packages.

View the composable architecture packages in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/StudioCreatio/8.0/scr_ComposablePackageArchitecture.png)

During the transition period, Creatio includes both architectures. Composable
and classic architecture packages are connected via the `Base` classic package.
View the connection chart between composable and classic architecture packages
in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/StudioCreatio/8.0/scr_ComposableAndClassicArchitectureSchema.png)

If Creatio has composable apps installed, the composable and classic
architecture package connection chart remains the same. Composable apps depend
on the `CrtCore` package of composable architecture and do not depend on classic
architecture packages. For example, view the connection chart between composable
architecture packages, **Customer 360** composable app, and classic architecture
packages in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/StudioCreatio/8.0/scr_ArchitecturesAndAppSchema.png)

## Transition process from classic to composable architecture​

The transition period has the following special features:

- During the transition period, existing instances contain composable and
  classic architecture packages when you update Creatio. Existing Creatio
  instances automatically receive composable architecture packages when updating
  the version. Creatio instance includes classic architecture packages to ensure
  backward compatibility.
- When you update a version, existing Creatio instances automatically receive
  the composable apps released for your base product app. For example,
  **Customer 360** is the first composable app released for Creatio. The app
  lets you manage contacts and accounts using **Contacts** and **Accounts**
  Freedom UI sections. Base product apps include these sections. As a result,
  existing Creatio instances receive the **Customer 360** app automatically when
  updating the version. Unlike **Customer 360** app, which is used by base
  product apps, only existing instances of Service base product app receive the
  **Case Management** composable app when updating the version. Learn more about
  base product apps in a separate article:
  [Freedom UI app types](https://academy.creatio.com/documents?ver=8.1&id=2417&anchor=title-2532-3).
- Existing instances contain Freedom UI and Classic UI sections when you update
  Creatio. If the names of Freedom UI and Classic UI sections are the same when
  you update an existing Creatio instance, Creatio adds the `Classic UI` suffix
  to the name of Classic UI section. For example, **Contacts Classic UI**. You
  can work with both section types in existing Creatio instances. We recommend
  using a transition period to transfer your customizations of Classic UI
  sections to the new app.
- New Creatio instances receive Freedom UI and Classic UI sections for three
  months after the release of a composable app. New Creatio instances receive
  only Freedom UI sections three months after the release.
- Once the transition process ends, new Creatio instances will no longer receive
  classic architecture packages. New Creatio instances will receive composable
  apps and composable architecture packages.

---

## See also​

[Freedom UI app types](https://academy.creatio.com/documents?ver=8.1&id=2417)
(user documentation)

- Classic package architecture
- Composable package architecture
- Transition process from classic to composable architecture
- See also
