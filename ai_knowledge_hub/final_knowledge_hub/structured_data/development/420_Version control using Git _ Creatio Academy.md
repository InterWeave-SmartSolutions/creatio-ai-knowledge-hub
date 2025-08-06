# Version control using Git | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 895 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/version-control-system/git

## Description

This article covers how to get started with Git in Creatio. The article starts
with explaining the basics of Git, then moves on to the specifics of Git use in
Creatio and Git setup. After you read the article, you will know what Git is,
and have your Creatio instance set up and ready to go.

## Key Concepts

workflow, configuration, section, integration, sql, database, package, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/version-control-system/git)**
(8.3).

Version: 8.1

On this page

Level: intermediate

This article covers how to get started with Git in Creatio. The article starts
with explaining the basics of Git, then moves on to the specifics of Git use in
Creatio and Git setup. After you read the article, you will know what Git is,
and have your Creatio instance set up and ready to go.

**Git** is a distributed version control system. The major **difference**
between Git and other version control system is the approach to data management.
Git **stores data** similar to a series of file system snapshots. Each time you
commit changes, i. e., save the state of your project, Git creates a snapshot of
your files at the moment and saves a link to the snapshot. If the files were not
changed, Git does not save them again but creates a link to the previously saved
identical file version. Git stores data as a stream of snapshots. CVS,
Subversion, Perforce, Bazaar, and other version control systems store data as a
set of files and index of individual file changes over time. This approach is
usually called delta-based version control.

The **file statuses in Git** are as follows:

- `committed`. The file has already been saved to the local repository.
- `modified`. The file was changed, but is yet to be committed to the local
  repository.
- `staged`. The file was changed and marked to be included in the next commit.

View the instructions for installing and working with the Git version control
system in the official
[Git documentation](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control).

You can also work with Git using any convenient GUI, such as
[Sourcetree](https://www.sourcetreeapp.com/).

## Special features of working with Git in Creatio​

Creatio IDE lets you work with the Subversion (SVN) version control system using
built-in development tools. However, the built-in SVN integration mechanism is
disabled when file system development mode is enabled. In this case, you can use
any version control system. We recommend using Git.

The Git version control system is **recommended** for the following Creatio
apps:

- Apps whose functionality is developed in the file system.

- Creatio on-site.

We recommend using SVN for Creatio in the cloud. Learn more about working with
SVN in a separate article:
[Version control in Subversion](https://academy.creatio.com/documents?ver=8.1&id=15142).

## General workflow in Git​

### 1\. Create a package​

1. Click the
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_system_designer.png)
   button to open the System Designer.

2. Click **Advanced settings** in the **Admin area** block.

3. Click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateNewPackage/scr_pkg_create_button.png)
   in the package workspace.

4. Fill out the **package properties** :
   - Set **Name** to "sdkPackageInFileSystem."

Create a package without binding it to the repository.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/GitInCreatio(7.17)/scr_git_package.png>)

5. Click **Create and add dependencies** and add the
   [package dependencies](https://academy.creatio.com/documents?ver=8.1&id=15121&anchor=title-2105-3).

6. Create the configuration elements in the user-made package.

### 2\. Export the package to the file system​

1. Configure Creatio to work in the file system. Learn more in a separate
   article:
   [External IDEs](https://academy.creatio.com/documents?ver=8.1&id=15111&anchor=title-2098-4).

2. Select **Download packages to file system** in the **File system development
   mode** group of the action menu.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreatingPackageInFileSystem(7.17)/scr_download_to_fs.png>)

As a result, the packages will be downloaded along the
`..\Terrasoft.WebApp\Terrasoft.Configuration\Pkg` path to the directory whose
name matches the package name.

### 3\. Add the source code​

Use an [external IDE](https://academy.creatio.com/documents?ver=8.1&id=15111) to
work with the source code of client or server schemas.

### 4\. Commit changes to the Git repository​

1. Click **Stage All** and select the files to commit.
2. Click **Pull** and download changes made by other users from the global
   repository.
3. Click **Commit** and commit the changes to the local repository.
4. Click **Push** and commit the changes to the global repository.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/GitInCreatio/7.17/scr_git_sourcetree.png)

### 5\. Install the package into Creatio​

1. Click the
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TryIt/scr_system_designer.png)
   button to open the System Designer.

2. Click **Advanced settings** in the **Admin area** block.

3. Select **Update packages from file system** in the **File system development
   mode** group of the action menu.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPkgFromSvnInFileSystemMode(7.17)/scr_updating.png>)

As a result, the package will be added to Creatio.

### 6\. Generate source codes​

To **generate source codes** , select **Generate where it is needed** in the
**Source code** group of the action menu.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPkgFromSvnInFileSystemMode/7.17/scr_generate_source_code.png)

### 7\. Compile the changes​

To **compile the changes** , click **Compile** on the toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPkgFromSvnInFileSystemMode/7.17/scr_compile.png)

You can check whether you need to update the database structure, install SQL
scripts, and bind data in the **Status** column of the **Configuration** section
workspace.

### 8\. Update the database structure​

To **update the database structure** , select **Update DB structure where it is
needed** in the **Actualize items** group of the action menu.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/InstallPkgFromSvnInFileSystemMode/7.17/scr_update_db.png)

### 9\. Install SQL scripts and bound data (optional)​

If the package contains bound SQL scripts or data, take appropriate steps to
execute or install them.

After the installation, the implemented package functionality will become
available in Creatio.

Users might need to clear the browser cache and refresh the page to apply the
changes.

---

## See also​

[Version control in Subversion](https://academy.creatio.com/documents?ver=8.1&id=15142)

[Packages basics](https://academy.creatio.com/documents?ver=8.1&id=15121)

[External IDEs](https://academy.creatio.com/documents?ver=8.1&id=15111)

---

## Resources​

[Official Git documentation](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)

[Official Sourcetree website](https://www.sourcetreeapp.com/)

---

## E-learning courses​

[Tech Hour - W5H of teamwork - Git and Creatio](https://www.youtube.com/watch?v=Qy7BsGrxbB0&list=PLnolcTT5TeE3v8WGd3VqlZSd2D02GWSGa&index=5)

- Special features of working with Git in Creatio
- General workflow in Git
  - 1\. Create a package
  - 2\. Export the package to the file system
  - 3\. Add the source code
  - 4\. Commit changes to the Git repository
  - 5\. Install the package into Creatio
  - 6\. Generate source codes
  - 7\. Compile the changes
  - 8\. Update the database structure
  - 9\. Install SQL scripts and bound data (optional)
- See also
- Resources
- E-learning courses
