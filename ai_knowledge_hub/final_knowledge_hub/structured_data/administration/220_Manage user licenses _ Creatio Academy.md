# Manage user licenses | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 836
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/licensing/manage-user-licenses

## Description

Only licensed users have access to Creatio functionality.

## Key Concepts

section, role, operation, account

## Use Cases

system administration, user management, security setup

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/administration/licensing/manage-user-licenses)**
(8.3).

Version: 8.0All Creatio products

On this page

Only licensed users have access to Creatio functionality.

Set up licensing in the **License manager** section (Fig. 1).

Fig. 1 The License manager section

![Fig. 1 The License manager section](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing.png)

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

1. Generate a license request file and send it to the Creatio technical support
   team.
2. The support team will send a file for you to upload to Creatio.

This procedure is also **required when updating Creatio on-site**.

### Generate a license request​

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

2. Click "**License manager** " under "Users and administration".

3. Click **Actions** → **Request**.

4. Enter the company ID for licensing. Creatio provides the ID after the
   purchase. Alternatively, request it from Creatio support.

5. Click **Generate a license request file** (Fig. 2). This will generate a
   \*.tlr license request file.

Fig. 2 Generating a license request

![Fig. 2 Generating a license request](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_wnd_license_request.gif)

6. Fill out the **License Version** field with the Creatio version to which you
   are going to update.

7. Send the license request file to Creatio technical support team. In response,
   the team will send you a file that contains the information about purchased
   licenses.

You can also request licenses from the **System users** section by clicking
**Request licenses** in the **Actions** menu (Fig. 3).

Fig. 3 Generating a license request

![Fig. 3 Generating a license request](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_user_license_request.gif)

**As a result** , the license request will be sent to Creatio support.

### Upload licenses to Creatio​

1. Save the license file received from the technical support team.

2. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

3. Click "**License manager** " under "Users and administration".

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

## Distribute or recall licenses for multiple users​

To enable new employees to log in or use specific functions, their user accounts
must be licensed. A system administrator can redistribute the available licenses
at any time. The number of active and available licenses is displayed on the
product licensing page and depends on the license type.

**Distribute licenses** in the **License manager** or **System users** sections.
If you need to distribute licenses to several user accounts at once, use the
**License manager** section:

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.
2. Click **License manager** under **Users and administration**.
3. Click **Actions** → **Select multiple records**.
4. Select the needed users in the list.
5. Click **Actions** → **Grant licenses** / **Recall licenses**. This opens a
   window.
6. Select the Creatio products to grant or recall licenses. Select the needed
   checkboxes and click **Select**.

**As a result** , the selected licenses will be distributed or recalled for the
selected user accounts.

## Add a portal user account​

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

2. Click **License manager** under **Users and administration**.

3. Select the user to distribute a license in the section list. On the
   **Licenses** tab of the user page, select the products for licensing (Fig.
   6).

Fig. 6 Select products for licensing

![Fig. 6 Select products for licensing](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/licensing/BPMonlineHelp/licensing_manage/scr_chapter_licensing_user_page_select.png)

Similarly, you can recall the licenses.

4. Save and close the page.

**As a result** , the selected licenses will be distributed or recalled for the
user account.

## Delete licenses from Creatio​

Sometimes, deleting licenses is required. For example, you need to switch
Creatio to the demo mode.

To **delete licenses from Creatio** :

1. Click the
   ![](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/btn_system_designer_8_shell.png)
   button → System Designer.

2. Click "**License manager** " under "Users and administration".

3. Click **Actions** → **Delete** (Fig. 7).

Fig. 7 Deleting licenses

![Fig. 7 Deleting licenses](https://academy.creatio.com/docs/sites/en/files/images/Setup_and_Administration/creatio_licensing/scr_chapter_licensing_delete_license.gif)

**As a result** , Creatio will delete all licenses.

---

## See also​

[Creatio licensing](https://academy.creatio.com/documents?id=1264)

[Marketing Creatio licensing](https://academy.creatio.com/documents?id=2073)

- Add licenses to Creatio
  - Generate a license request
  - Upload licenses to Creatio
- Distribute or recall licenses for multiple users
- Add a portal user account
- Delete licenses from Creatio
- See also
