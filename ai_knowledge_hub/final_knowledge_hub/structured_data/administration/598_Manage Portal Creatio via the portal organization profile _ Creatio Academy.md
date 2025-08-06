# Manage Portal Creatio via the portal organization profile | Creatio Academy

**Category:** administration **Difficulty:** beginner **Word Count:** 812
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.0/more-apps/portal/manage-portal-via-organization-profile

## Description

This article covers how a portal administrator can manage portal users and their
access permissions. Primary Creatio application administrators can manage users
and access permissions on the portal as well. Learn more: Manage Creatio Portal
in the main application.

## Key Concepts

detail, integration, role, system setting, contact, account

## Use Cases

third-party integration, data synchronization, system connectivity

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/overview/platform-overview)** (8.3).

Version: 8.0All Creatio products

On this page

This article covers how a portal administrator can manage portal users and their
access permissions. Primary Creatio application administrators can manage users
and access permissions on the portal as well. Learn more:
[Manage Creatio Portal in the main application](https://academy.creatio.com/node/2085/).

note

Since Creatio version 8.0.9 "Portal user" user type and "All portal users" root
role were renamed to "External user" and "All external users," respectively.

## Add portal users​

To add new portal users:

1. Click your profile picture in the top right → **Organization profile**.

2. Go to the **Portal users** detail → click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_add_tab_1.png)
   → enter the emails of the users to invite. Creatio validates any entered
   email automatically. Click **Create portal users** (Fig. 1).

If Creatio matches the entered emails to any existing contacts, it will add
portal users linked to those contacts. If Creatio finds no matching contacts,
they will be created automatically, based on the emails. For any new contacts,
the **Full name** field will contain the email local part, i. e. the text before
"@."

Fig. 1 Adding portal users as a portal administrator

![Fig. 1 Adding portal users as a portal administrator](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/gif_chapter_portal_adding_new_user_on_portal.gif)

3. Creatio will prompt you to send email invitations to the new portal users.
   You can close the prompt and send the invitations later.

As a result, new portal users will be added to the portal. The users will need
to click the link in the invitation email to log in to the portal for the first
time. Once on the portal, each user will be able to set a password.

## Send invitations to portal users​

You can invite new users to the portal. Potential users receive an email
invitation with a one-time link they can use to access the portal for the first
time and set up their password.

note

The email integration must be set up, and a valid mailbox must be specified in
the "SSP registration mailbox" ("SSPRegistrationMailbox" code)
[system setting](https://academy.creatio.com/node/286/) in the primary Creatio
application for you to be able to send email invitations. Learn more:
[Working with emails](https://academy.creatio.com/node/749/).

If a new portal user forgets to set their password after the first login, you
will need to re-send the invite. To do this:

1. Select the needed users in the **Portal users** detail.

2. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_marketing_plans_detail_menu_1.png)
   and select **Send invites** (Fig. 2):

Fig. 2 Send a portal invitation

![Fig. 2 Send a portal invitation](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_porta_portal_user_invitation.png)

## Set up access permissions for portal users​

You can grant permissions to other portal users within your organization.

To assign the invited user all functional roles available to the organization:

1. Click your profile picture in the top right → **Organization profile**.

2. Go to the **Portal users** detail → click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_add_tab_2.png)
   → enter the emails of the users to invite.

3. In the user registration window, select the roles to assign to the invited
   users (Fig. 3). Click **Create portal users**.

In this example, the users will obtain all permissions of the portal
administrator, as well as permissions assigned to the "Portal managers" role.

Fig. 3 Assign permissions to the new portal users

![Fig. 3 Assign permissions to the new portal users](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_porta_portal_user_functional_roles.png)

You can assign roles to the existing users as well. The list of available roles
is shown on the **Portal users** detail (Fig. 4).

Fig. 4 The portal user roles

![Fig. 4 The portal user roles](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_porta_portal_user_all_functional_roles.png)

## Promote a portal user to an administrator​

You can grant portal administrator privileges to any user within your
organization. To do this:

1. Click your profile picture in the top right → **Organization profile**.

2. Go to the **Portal users** detail and select **Administrator for organization
   on the portal** checkbox (Fig. 5) for the users you want to assign
   administrator privileges.

Fig. 5 Assign the portal administrator privileges

![Fig. 5 Assign the portal administrator privileges](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_porta_portal_administrators2.png)

## Deactivate portal users​

Deactivate a portal user account to restrict the corresponding user from
accessing the portal. To do this:

1. Click your profile picture in the top right → **Organization profile**.

2. Go to the **Portal users** detail → clear the **Active** checkbox next to the
   users whom you want to deactivate (Fig. 6).

Fig. 6 Deactivate the portal users

![Fig. 6 Deactivate the portal users](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_porta_portal_users_deactivation.png)

As a result, the user will be suspended and will not be able to access the
portal. You can reactivate a user at any time.

## Change the service information on the portal​

The portal in Service Creatio, enterprise edition, lets you view all service
agreements of your company. To do this, click your profile picture in the top
right → **Organization profile** → **Maintenance** (Fig. 7).

Fig. 7 The company’s service agreements

![Fig. 7 The company’s service agreements](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/portal/manage_portal_via_organization_profile/scr_chapter_portal_organization_page_maintaince.png)

You can add, modify and delete your company’s addresses (actual, legal and
shipping) as well. All changes must be saved.

---

## See also​

[Manage Portal Creatio in the main application](entity:node/2085)

- Add portal users
- Send invitations to portal users
- Set up access permissions for portal users
- Promote a portal user to an administrator
- Deactivate portal users
- Change the service information on the portal
- See also
