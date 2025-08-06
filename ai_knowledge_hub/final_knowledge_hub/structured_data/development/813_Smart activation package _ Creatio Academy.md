# Smart activation package | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1009 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/packages/automatically-activated-package

## Description

Smart activation package is a manually created package that combines
functionality of multiple apps for compatibility between them in a single
Creatio instance. For example, you can implement the User requests tab for the
contact page in the Requests app using smart activation package and add the
dependencies from the Customer 360 app packages. If the Requests app into a
Creatio instance that contains the Customer 360 app, Creatio adds the new User
requests tab to the contact page.

## Key Concepts

configuration, section, operation, package, contact, marketplace, no-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/automatically-activated-package)**
(8.3).

Version: 8.1

On this page

Level: beginner

**Smart activation package** is a manually created package that combines
functionality of multiple apps for compatibility between them in a single
Creatio instance. For example, you can implement the **User requests** tab for
the contact page in the **Requests** app using smart activation package and add
the dependencies from the **Customer 360** app packages. If the **Requests** app
into a Creatio instance that contains the **Customer 360** app, Creatio adds the
new **User requests** tab to the contact page.

An app can include one or more smart activation packages. The package is
installed into the environment and activated automatically when all its
dependencies are available. Missing dependencies do not interfere with the
installation of the package/app that includes the package. Once all dependencies
are available, the package is automatically activated, and becomes accessible to
the user. If the dependencies are no longer available, the package is
automatically deactivated. Smart activation package lets you extend the
functionality of other composable apps and simultaneously preserve the
independence of the app that includes the smart activation package when the
associated apps are not installed. I. e., the smart activation package
functionality is inactive while the main packages of the app that includes the
installed smart activation package. For example, Marketplace developers can use
smart activation packages to extend base Creatio functionality or functionality
of other Marketplace apps.

View the layout examples of smart activation packages in the app structure
below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/AutomaticallyActivatedPackage/8.0/scr_PackageExamples.png)

## Operations with smart activation packages​

- Create a smart activation package. Read more >>>
- Change the type of existing package to smart activation package. Read more >>>
- Install a smart activation package. Read more >>>
- Deactivate a smart activation package. Read more >>>

### Create a smart activation package​

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).
2. **Create a package**. Instructions:
   [Create a user-made package using Configuration section](https://academy.creatio.com/documents?ver=8.1&id=15122)
   (steps 1–2).
3. **Select the Use smart activation checkbox**.
4. **Add the package dependencies** to select the app packages that activate the
   smart activation package. Instructions:
   [Define the package dependencies](https://academy.creatio.com/documents?ver=8.1&id=15122&anchor=title-1198-4).
5. **Create configuration elements** that extend functionality of other apps in
   the smart activation package. Operations with configuration elements of the
   smart activation package and other packages are the same. Instructions:
   [Creatio IDE overview](https://academy.creatio.com/documents?ver=8.1&id=15101).

**As a result** , Creatio will create a smart activation package that extends
existing functionality.

If you create a smart activation package in the current Creatio instance,
Creatio displays this package in the **Configuration** section and **Advanced
settings** tab in the No-Code Designer as a simple user-created package. If a
package inherits from a smart activation package, the smart activation package
behaves like a simple package. To prevent this, change the dependencies of the
smart activation package.

View the examples of dependencies for the smart activation package in the figure
below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/AutomaticallyActivatedPackage/8.0/scr_PackageDependencies.png)

### Change the type of existing package to smart activation package​

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).
2. **Select the package**. You can only change the type of user-created unlocked
   packages.
3. **Open the package properties**. Instructions:
   [Package workspace](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-11).
4. **Select the Use smart activation checkbox**.
5. **Change the package dependencies** if needed. Instructions:
   [Define the package dependencies](https://academy.creatio.com/documents?ver=8.1&id=15122&anchor=title-1198-4).

**As a result** , Creatio will change the type of existing package to smart
activation package.

Also, you can **disable the smart activation** for the package. To do this,
clear the **Use smart activation** checkbox on the **Package properties** page.

### Install a smart activation package​

To install a smart activation package, install an app that has one or more such
packages. You can install an app from Marketplace, from a file, or transfer an
app from another Creatio environment. Instructions:
[Manage apps](https://academy.creatio.com/documents?ver=8.1&id=2444) (user
documentation). **Before the installation** Creatio checks whether the app
contains smart activation packages and their dependencies. If dependencies
exist, Creatio installs smart activation packages separately.

**As a result** :

- If **the smart activation package extends an installed app** , Creatio will
  install and activate the smart activation package.
- If **the smart activation package extends an app that is not installed** ,
  Creatio will install the smart activation package without activating it and
  save the package to the Creatio file system.
- If you **install an app that the smart activation package extends** , Creatio
  will activate the smart activation package.

Creatio displays activated smart activation packages in the **Configuration**
section and on the **Advanced settings** tab in the No-Code Designer as simple
user-created packages. Creatio displays deactivated smart activation packages in
the file system.

Installation logs include installation data of smart activation packages. If
installation of the app that has a smart activation package ends with an error,
roll back your Creatio configuration to the state before the app was installed.
If the error occurs when you install an app that **updates an existing smart
activation package** , Creatio rolls back to the previous state of the smart
activation package. If the error occurs when you install an app that **adds a
new smart activation package** , Creatio rolls back to the previous state of the
configuration that did contain the smart activation package.

### Deactivate a smart activation package​

Consider deactivating a package using the following example. For example, the
Creatio instance includes the following apps:

1. App 1 that includes a set of packages and has no a smart activation package.
2. App 2 that includes a set of packages and a smart activation package that has
   dependencies on the packages from the app 1.

When user deletes the app 1, Creatio executes the following actions:

1. Deletes the app 1.
2. Deactivates the smart activation package from the app 2 as it no longer has
   the full set of required dependencies.

---

## See also​

[Creatio IDE overview](https://academy.creatio.com/documents?ver=8.1&id=15101)

[Packages basics](https://academy.creatio.com/documents?ver=8.1&id=15101)

[Manage apps](https://academy.creatio.com/documents?ver=8.1&id=2444) (user
documentation)

- Operations with smart activation packages
  - Create a smart activation package
  - Change the type of existing package to smart activation package
  - Install a smart activation package
  - Deactivate a smart activation package
- See also
