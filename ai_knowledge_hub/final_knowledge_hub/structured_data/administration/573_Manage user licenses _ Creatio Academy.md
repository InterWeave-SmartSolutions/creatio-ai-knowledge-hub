# Manage user licenses | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 1374
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/licensing/manage-user-licenses

## Description

You need to issue licenses to each new Creatio user. Only licensed users can log
in to Creatio and access the corresponding functionality. For example, users who
were not issued a "Creatio marketing" license, will not be able to use functions
that are specific to Marketing Creatio, such as the Email and the Campaigns
sections. Out of the box, Creatio system administrators have permission to
distribute licenses to user accounts.

## Key Concepts

section, role, operation, system setting, synchronization, campaign, account

## Use Cases

system administration, user management, security setup

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/administration/licensing/manage-user-licenses)**
(8.3).

Version: 8.1

On this page

You need to issue licenses to each new Creatio user. Only licensed users can log
in to Creatio and access the corresponding functionality. For example, users who
were not issued a "Creatio marketing" license, will not be able to use functions
that are specific to Marketing Creatio, such as the **Email** and the
**Campaigns** sections. Out of the box, Creatio system administrators have
permission to distribute licenses to user accounts.

Important

To enable licensing a user account, Creatio must have available licenses that
were not distributed among other users.

Set up licensing in the **License manager** section (Fig. 1).

Fig. 1 License manager section

![Fig. 1 License manager section](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing.png)

If the licenses expire, the license manager page opens for a user that has the
"System administrators" role automatically when they log in to Creatio.

note

Viewing, distributing, and recalling licenses requires permissions to the
"Manage user licenses" (the "CanManageLicUsers" code) system operation. Learn
more:
[Set up system operation permissions](https://academy.creatio.com/documents?id=2000).

To **license Creatio** :

1. Add licenses to Creatio. Read more >>>
2. Distribute the available licenses among the user accounts. Read more >>>

When working with Creatio, you might need to manage user licenses, e. g., to
distribute licenses to a new employee or recall licenses from a resigned
employee. You can use the **System users** section as well as **License
manager** section for this purpose. In the **System users** section, you can
manage licenses of a single or multiple accounts.

## Add licenses to Creatio​

The licensing process is similar for all types of licenses used in Creatio.

When purchasing licenses, extending available licenses, and updating Creatio
on-site:

1. Generate a license request file and send it to Creatio support.
2. The support team will send a file for you to upload to Creatio.

This procedure is also **required when updating Creatio on-site**.

### Generate a license request​

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

2. Click **License manager** under **Users and administration**.

3. Click **Actions** → **Request**.

4. Enter the company ID for licensing. Creatio provides the ID after the
   purchase. Alternatively, request it from Creatio support.

5. Click **Generate a license request file** (Fig. 2). This will generate a
   \*.tlr license request file.

Fig. 2 Generating a license request

![Fig. 2 Generating a license request](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_wnd_license_request.gif)

6. Fill out the **License Version** field using the Creatio version to which you
   are going to update.

7. Send the license request file to Creatio support. In response, the team will
   send you a file that contains the information about purchased licenses.

You can also request licenses from the **System users** section by clicking
**Request licenses** in the **Actions** menu (Fig. 3).

Fig. 3 Generating a license request

![Fig. 3 Generating a license request](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/creatio_licensing/8_1/scr_user_license_request.png)

**As a result** , the license request will be sent to Creatio support.

### Upload licenses to Creatio​

1. Save the license file received from the support team.

2. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → **System Designer**.

3. Click **License manager** under **Users and administration**.

4. Click **Actions** → **Upload** (Fig. 4).

Fig. 4 Uploading a license file to Creatio

![Fig. 4 Uploading a license file to Creatio](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing00002.png)

5. Specify the path to the license file you saved earlier.

You can also upload licenses from the **System users** section by clicking
**Upload licenses** in the **Actions** menu (Fig. 5).

Fig. 5 Upload a license file to Creatio

![Fig. 5 Upload a license file to Creatio](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing00002_user.png)

**As the result** , the new licenses will be uploaded to Creatio. The total
license number might increase, and the available licenses will be extended.

## Distribute or recall licenses manually for multiple users​

To enable new employees to log in or use specific functions, their user accounts
must be licensed. A system administrator can redistribute the available licenses
at any time. The number of active and available licenses is displayed on the
product licensing page and depends on the license type.

**Distribute licenses** in the **License manager** or **System users** sections.
If you need to distribute licenses to multiple user accounts at once, use the
**License manager** section:

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → **System Designer**.
2. Click **License manager** under **Users and administration**.
3. Click **Actions** → **Select multiple records**.
4. Select the needed users in the list.
5. Click **Actions** → **Grant licenses** / **Recall licenses**. This opens a
   window.
6. Select the Creatio products to grant or recall licenses. Select the needed
   checkboxes and click **Select**.

**As a result** , the selected licenses will be distributed or recalled for the
selected user accounts.

## Distribute or recall licenses manually for one user​

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

2. Click **License manager**.

3. Select the user to distribute a license in the section list. On the
   **Licenses** tab of the user page, select the products for licensing (Fig.
   6).

Fig. 6 Select products for licensing

![Fig. 6 Select products for licensing](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/creatio_licensing/8_1/scr_chapter_licensing_user_page_select.png)

Similarly, you can recall the licenses.

4. Save and close the page.

**As a result** , the selected licenses will be distributed or recalled for the
user account.

## Distribute or recall licenses automatically for multiple users​

note

This functionality is available for Creatio 8.1.3 and later.

Creatio supports role-based license distribution approach to speed up the
issuance of licenses to users. This functionality enables system administrators
to create rules for automatic license distribution based on the user role. That
makes it possible to provide different user groups with different set of
licenses automatically.

Roles inherit licenses through full hierarchy in company's organizational
structure. For example, if you have a "Support" role that has "1st-line
support", "2nd-line support" and "3rd-line support" child roles, than all users
who do not belong directly to the "Support" role but are included to the one of
the child roles will be provided with licenses from the "Support" and "All
employees" roles. You can manage this mechanism using the "Turn on license
inheritance from parent roles" ("UseFullHierarchyDuringLicenseDistribution"
code) system setting.

Automatic role-based license distribution works for Creatio instances during
**LDAP synchronization** or **Single-Sign-On provisioning**.

To set up a new license distribution method you need to **bind the list of
licenses to the role** :

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → **System Designer**.

2. Open the **Organizational roles** or **Functional roles** section.

3. Select the role to provide users with licenses.

4. Open **Licenses** tab.

5. Click
   ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/user_access_management/BPMonlineHelp/adding_users/btn_com_add_tab.png)
   on the **Licenses to distribute with roles** expanded list title.

6. Select licenses to distribute for users in the role.

7. Click **Select**.

**As a result** , selected licenses will be bound to the role and automatically
redistributed for all users included to the role during the LDAP synchronization
process or JIT provisioning via SSO. If the user is **excluded from the role**
in LDAP or SSO, the licenses will be removed accordingly. Licenses are
redistributed automatically every time user role is changed or list of licenses
bound to the role is changed.

Similarly, you can recall the licenses.

## Redistribute licenses for user roles​

If you want to redistribute licenses among users without waiting for them to
re-login via LDAP or SSO you can do it in the **Organizational roles** or
**Functional roles** section.

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → **System Designer**.

2. Open the **Organizational roles** or **Functional roles** section.

3. Select the role to redistribute licenses.

4. Click **Actions** → **Redistribute licenses for the role**.

Fig. 7 Redistribute licenses for the role

![Fig. 7 Redistribute licenses for the role](https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/creatio_licensing/8_1/scr_chapter_licensing_redistribite.png)

5. Specify whether to keep or remove licenses that were issued to users
   manually.

6. Click **OK**.

7. Repeat steps 3-6 for all the roles to redistribute licenses.

**As a result** , the licenses will be redistributed for all the users within
selected roles. If you do not take away user licenses that provide access to the
product, the redistribution process will not have any impact on the user
experience in Creatio.

## Delete licenses from Creatio​

Sometimes, deleting licenses is required. For example, you need to switch
Creatio to the demo mode.

To **delete licenses from Creatio** :

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → **System Designer**.

2. Click **License manager** under **Users and administration**.

3. Click **Actions** → **Delete** (Fig. 7).

Fig. 8 Deleting licenses

![Fig. 8 Deleting licenses](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_delete_license.gif)

**As a result** , Creatio will delete all licenses.

---

## See also​

[Creatio licensing](ihttps://academy.creatio.com/documents?id=1264)

[Marketing Creatio licensing](ihttps://academy.creatio.com/documents?id=2073)

- Add licenses to Creatio
  - Generate a license request
  - Upload licenses to Creatio
- Distribute or recall licenses manually for multiple users
- Distribute or recall licenses manually for one user
- Distribute or recall licenses automatically for multiple users
- Redistribute licenses for user roles
- Delete licenses from Creatio
- See also
