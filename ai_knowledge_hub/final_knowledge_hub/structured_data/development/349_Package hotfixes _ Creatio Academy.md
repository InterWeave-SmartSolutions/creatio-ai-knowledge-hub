# Package hotfixes | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 368
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/delivery/hotfix-mode

## Description

Use package hotfixes when users cannot work until you deliver a bug-fix package,
and regular delivery takes too long.

## Key Concepts

configuration, section, role, system setting, package, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Use package hotfixes when users cannot work until you deliver a bug-fix package,
and regular delivery takes too long.

Package hotfixes let system administrators (users who belong to the "System
administrators" role) execute the following actions:

- Fix critical bugs and problems with functionality detected in the production
  environment.
- Minimize risks when detecting security issues and potential vulnerabilities in
  the production environment.

Important

Creatio logs package unlock and lock actions and saves data to the Audit log.

To make package hotfixes:

1. **Open the Configuration section**. Instructions:
   [Open the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2).

2. **Select the package** to make a hotfix.

3. **Unlock the package** for hotfix. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Settings.png)
   in the package workspace → **Unlock for hotfix**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_UnlockForHotfix.png)

As a result, Creatio executes the following actions:

     * Unlock the package.

     * Change the icon of the unlocked package to ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_UnlockPackageIcon.png).

     * Move the unlocked package to the top of the **All packages** group.

     * Save data about unlocking the package to the Audit log.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_UnlockPackageAction.png)

4. **Fix the critical bugs and problems** with functionality.

note

Out of the box, the package is unlocked for 30 minutes. You can change how long
to keep the package unlocked for hotfix in the **Duration of package hotfix
status** (`PackageHotfixTimeout` code) system setting.

5. **Lock the package** after hotfix. To do this, click
   ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Settings.png)
   in the package workspace → **Lock after hotfix**.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_LockAfterHotfix.png)

As a result, Creatio executes the following actions:

     * Lock the package.

     * Change the icon of the locked package to ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_LockPackageIcon.png).

     * Display packages in the **All packages** group alphabetically.

     * Save data about locking the package to the Audit log.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/HotFixMode/8.1/scr_LockPackageAction.png)

6. **Deliver changes** to the development environment. Otherwise, the changes
   will be lost during the next update of the production environment.
   - If the hotfix changes were implemented in a **self-developed package** ,
     make identical changes in the development environment and deliver the
     changes as usual.
   - If the hotfix changes were implemented in the **package of another
     maintainer** , contact maintainer support to notify them about problems
     with the functionality.

Creatio changes the icon of locked package to
![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/SectionConfigurationGeneralInfo/scr_Package_Blocked.png)
in production environment when you deliver the changes as usual.

---

## See also​

[Delivery management process](https://academy.creatio.com/documents?ver=8.3&id=15202)

[Compile an app on a web farm](https://academy.creatio.com/documents?ver=8.3&id=2410)
(user documentation)

[Update guide](https://academy.creatio.com/documents?ver=8.3&id=2495)

- See also
