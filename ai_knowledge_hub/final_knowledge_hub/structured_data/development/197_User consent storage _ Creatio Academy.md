# User consent storage | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 552 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/platform-customization/freedom-ui/user-consents

## Description

Creatio stores the user consents in the database. You can add the name,
description, text, and expiration date of user consents from any third-party
system or service to Creatio manually or by implementing custom business logic.
Using user consent storage, system administrators can do the following:

## Key Concepts

section, lookup, database, notification

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/user-consents)**
(8.3).

Version: 8.2

On this page

Level: beginner

Creatio stores the user consents in the database. You can add the name,
description, text, and expiration date of user consents from any third-party
system or service to Creatio manually or by implementing custom business logic.
Using user consent storage, system administrators can do the following:

- View a list of user consents.
- View user consent history.
- Track history of a dedicated user consent using the user consent code.
- Manage a dedicated user consent in custom functionality using the user consent
  code.

For example, you can display a notification about the need to renew a user
consent several days before its expiration date.

## View a list of user consents​

1. **Open the Lookups section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **Lookups**.

2. **Create a lookup**.
   1. Click **New lookup**.

   2. Fill out the lookup properties.

| Property | Property value | Name | Consent | Object | Consent |
| -------- | -------------- | ---- | ------- | ------ | ------- |

     3. Save the changes.

3. **Open the Consent lookup**.

**As a result** :

- The name of a user consent will be displayed in the **Name** property.
- The description of a user consent will be displayed in the **Description**
  property.
- The content of a user consent will be displayed in the **Consent text**
  property.
- The code of a user consent will be displayed in the **Code** property.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/UserConsents/8.2/scr_consent_lookup.png)

## View user consent history​

1. **Open the Lookups section**. To do this, click
   ![](https://academy.creatio.com/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png)
   in the top right → **System setup** → **Lookups**.

2. **Create a lookup**.
   1. Click **New lookup**.

   2. Fill out the lookup properties.

| Property | Property value | Name | User consent history | Object | User consent history |
| -------- | -------------- | ---- | -------------------- | ------ | -------------------- |

     3. Save the changes.

3. **Open the User consent history lookup**.

**As a result** :

- The expiration date of a user consent will be displayed in the **Consent
  expiration date** property.
- The code of a user consent will be displayed in the **Consent code** property.
  The **Consent code** column values of the `UserConsentHistory` object will
  match the **Code** column values of the `Consent` object.
- The acceptance date of a user consent will be displayed in the **Acceptance
  date** property.
- The user who accepted a user consent will be displayed in the **Accepted by**
  property.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/UserConsents/8.2/scr_user_consent_history_lookup.png)

To **renew term of the user consent** (the **Consent expiration date** property
value), implement custom business logic that populates the **Consent expiration
date** property using the date specified in the **Acceptance date** property.
For example, the **Consent expiration date** property value is 6 months later
than the **Acceptance date** property value. Display a notification about the
need to renew a term of the user consent a few days before it expires. After
renewal, update the values of the **Consent expiration date** and **Acceptance
date** properties automatically.

## Manually add a user consent to Creatio​

1. If needed, **create a new lookup** based on the `Consent` object. Read
   more >>>
2. **Open the lookup**.
3. **Add the lookup value**. To do this, click **New**.
4. **Fill out the properties of the lookup value** using the user consent from
   any third-party system or service.
5. **Save the changes**.

**As a result** , a user consent will be added to Creatio.

- View a list of user consents
- View user consent history
- Manually add a user consent to Creatio
