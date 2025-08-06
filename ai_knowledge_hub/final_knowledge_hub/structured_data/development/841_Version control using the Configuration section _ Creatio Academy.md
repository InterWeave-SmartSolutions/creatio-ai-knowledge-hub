# Version control using the Configuration section | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1421 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/version-control-system/configuration-version-control

## Description

Creatio IDE lets you work with the SVN version control system.

## Key Concepts

configuration, section, integration, sql, database, system setting, package,
contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/version-control-system/configuration-version-control)**
(8.3).

Version: 8.1

On this page

Level: beginner

Creatio IDE lets you work with the SVN version control system.

Important

Use the SVN version control system only to transfer changes between
[development environments](https://academy.creatio.com/documents?ver=8.1&id=15201).
Do not use SVN on a
[pre-production](https://academy.creatio.com/documents?ver=8.1&id=15201&anchor=title-2124-2)
or
[production](https://academy.creatio.com/documents?ver=8.1&id=15201&anchor=title-2124-3)
environment. This can render Creatio inoperable or decrease its performance.
Learn more in a separate article:
[Version control in Subversion](https://academy.creatio.com/documents?ver=8.1&id=15142).

The
[out-of-the-box Creatio IDE tools](https://academy.creatio.com/documents?ver=8.1&id=15203)
let you execute the following actions:

- install package from the SVN repository
- update package from the SVN repository
- commit package to the SVN repository

You cannot work with the SVN version control system using the out-of-the-box
Creatio IDE tools when the
[file system development mode](https://academy.creatio.com/documents?ver=8.1&id=15111)
is turned on. By default, the file system development mode is turned off.

SVN integration is enabled in Creatio by default. To set up SVN integration,
modify the value of the `defPackagesWorkingCopyPath` setting’s
`connectionString` attribute in the `ConnectionStrings.config` configuration
file. This setting contains the path to the directory that stores working
copies.

ConnectionStrings.config

    <add name="defPackagesWorkingCopyPath" connectionString="TEMP\APPLICATION\WORKSPACE\TerrasoftPackages" >

Creatio makes and uses a working copy of each user-made package with versioning
enabled in SVN integration mode. The working copy contains user-made packages
organized as a set of directories and files. The Creatio SVN client synchronizes
this data with an SVN repository. We recommend specifying the path to a
permanent directory in the `defPackagesWorkingCopyPath` system setting. The OS
might clear the temporary directory specified by default. Do not specify
`...\Terrasoft.WebApp\Terrasoft.Configuration\Pkg` as the repository of working
package copies in Creatio .NET Framework.

## Install a package from the SVN repository​

**Package installation** involves adding the package and its dependencies from
the SVN repository.

Install the package in the following **cases** :

- Multiple developers work on the package functionality.
- You need to transfer the changes between
  [environments](https://academy.creatio.com/documents?ver=8.1&id=15201).

If you use **Creatio in the cloud** , we recommend contacting Creatio support to
install the package.

To **install a package from the SVN repository** in Creatio on-site:

1. Back up the database.

This is required because it is not possible to roll back to the previous version
using the SVN version control system.

2. [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).

3. Select **Install package from repository** in the **SVN repositories** group
   of the action menu.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPackageFromStorage(7.17)/scr_menu1.png>)

4. Select the SVN repository as well as name and version of the package to
   install → **Install**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPackageFromStorage/7.17/scr_select_dialog.png)

Creatio applies bound data and sets dependencies automatically as part of the
package installation.

In some cases, the changes are not applied automatically. If this happens, apply
the changes manually.

To **apply the changes manually** to an installed package:

     1. [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).
     2. Generate source codes for configuration elements that require it.
     3. Compile the configuration.
     4. Update the database structure.
     5. Install SQL scripts if needed.
     6. Install bound data.

note

You can check whether to update the database structure, SQL scripts, and bound
data in the **Needs to be installed in database** and **Needs to be updated in
database** properties. A dialog will appear if an error occurs.

5. Click **Compile all**. This is required to
   [generate static content](https://academy.creatio.com/documents?ver=8.1&id=15126&anchor=title-1197-8).

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPackageFromStorage(7.17)/7.17/scr_compile_all.png>)

When you install a user-made package, Creatio checks its dependencies and
additionally sets or updates the dependency packages of the current package. For
example, when you install the **sdkUserMadePackage** package from the SVN
repository, the **sdkDependentPackage** dependent package is installed as well.
This also changes the Creatio package hierarchy. If the **sdkUserMadePackage**
package was installed previously, it is changed.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPackageFromStorage/7.17/scr_dependent.png)

When you instal a user-made package from the SVN repository, Creatio changes the
**package hierarchy** as follows:

1. The dependencies of the installed package are defined. View the dependencies
   in the `DependsOn` property of the package properties.

Package properties

         {
             "Descriptor": {
                 "UId": "8bc92579-92ee-4ff2-8d44-1ca61542aa1b",
                 "PackageVersion": "7.18.0",
                 "Name": "sdkUserMadePackage",
                 "ModifiedOnUtc": "\/Date(1522671879000)\/",
                 "Maintainer": "Customer",
                 "Description": "Package created by user",
                 "DependsOn": [{
                         "UId": "51b3ed42-678c-4da3-bd16-8596b95c0546",
                         "PackageVersion": "7.18.0",
                         "Name": "sdkDependentPackage"
                     },
                     {
                         "UId": "e14dcfb1-e53c-4439-a876-af7f97083ed9",
                         "PackageVersion": "7.18.0",
                         "Name": "SalesEnterprise"
                     }
                 ]
             }
         }


2. The installation of the dependent packages into the configuration is
   verified. If the packages are installed, Creatio updates them, otherwise, it
   installs them.

Important

If the dependencies are not found in SVN repositories (e. g., the SVN repository
is not registered in the repository list or is inactive), a message about
package installation error appears. The package dependency hierarchy is updated
when a package is installed. As such, add the SVN repositories that contain
dependent packages to the configuration and activate these repositories.

3. When a package is installed, Creatio installs or updates only the
   dependencies installed in the SVN version control system. Packages installed
   from \*.zip archives and pre-installed packages are not updated.

Install the packages on which the user-made package or its dependencies depend
before you install the user-made package. Installation fails if the workspace
lacks any pre-installed dependency package installed from a \*.zip archive.

## Update a package from the SVN repository​

**Package update** involves uploading the changes in both the package and
package
[dependencies](https://academy.creatio.com/documents?ver=8.1&id=15121&anchor=title-2105-3)
from the SVN repository into the Creatio. The dependencies of the updated
package are defined as part of the update. View the dependencies in the
`DependsOn` property of the package properties.

Update the package in the following **cases** :

- Multiple developers work on the package functionality.
- You need to transfer the changes between
  [environments](https://academy.creatio.com/documents?ver=8.1&id=15201).
- You are going to commit the changes.

To **update a package from the SVN repository** :

1. [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).

2. Select **Update from repository** in the package menu.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/UpdatePackageFromStorage(7.17)/pkg_updatet_mnu.png>)

This starts the update of the selected package and dependent packages from the
active SVN repositories.

Important

If the package dependencies are located in inactive SVN repositories, a message
about package update error appears. The package dependency hierarchy is updated
when a package is updated. As such, activate the SVN repositories that can
contain dependent packages.

3. Click **Compile all**. This is required to
   [generate static content](https://academy.creatio.com/documents?ver=8.1&id=15126&anchor=title-1197-8).

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPackageFromStorage(7.17)/7.17/scr_compile_all.png>)

## Commit a package to the SVN repository​

**Package committing** involves saving the package changes to the SVN
repository. Only the package for which you execute the commit action is
committed to the SVN repository. Changes to other configuration packages are not
committed.

Commit the package in the following **cases** :

- You [create](https://academy.creatio.com/documents?ver=8.1&id=15122) a
  user-made package.
- You add new configuration elements to the package.
- You modify the existing package configuration elements.
- You delete the package configuration elements.
- You
  [modify the package properties](https://academy.creatio.com/documents?ver=8.1&id=15122).

The **repository** appears next to the package name. Hold the pointer over the
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage/scr_repository.png)
icon to view the **name of the connected repository**.

The following data is displayed for **uncommitted user-made packages** :

- Package name.
- Name of the SVN repository where to commit the package. The revision number of
  the package in the SVN repository is not specified and added after the package
  is committed.

Uncommitted user-made packages are locked by default.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage/scr_repository_name.png)

The following data is displayed for **committed user-made packages** :

- Package name.
- SVN repository name.
- Last revision number of the package in the SVN repository

The display style of a committed user-made package that remains unchanged is the
same as a base package.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage/scr_repository_revision.png)

If you change a user-made package, for example, add schemas or change
properties, Creatio displays
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage/scr_repository_icon.png)
next to the package name.

Important

If you remove a configuration element from a package, the package looks like it
was not changed.

To **commit a package to the SVN repository** :

1. [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.1&id=15101&anchor=title-2093-2).

2. Select **Commit to repository** in the package menu.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage(7.17)/pkg_commit_mnu.png>)

This opens the change committing dialog.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CommitPackageToStorage(7.17)/pre_commit_info.png>)

3. Add a comment to the package commit in the required **Description** field. We
   recommend describing the changes in the package compared to the last commit.
   The changes in the commit package are displayed in the bottom.

After you click the **Commit changes** button, the package is commited and
changes become available to other Creatio users.

Important

The package is committed to the SVN repository specified in the package
properties. You can only commit a package to an active SVN repository.

After the package is committed to the SVN repository, the package as well as its
configuration elements are unlocked. The configuration elements also become
editable for other Creatio users.

---

## See also​

[Version control in Subversion](https://academy.creatio.com/documents?ver=8.1&id=15142)

[Environment overview](https://academy.creatio.com/documents?ver=8.1&id=15201)

[Delivery in Creatio IDE](https://academy.creatio.com/documents?ver=8.1&id=15203)

- Install a package from the SVN repository
- Update a package from the SVN repository
- Commit a package to the SVN repository
- See also
