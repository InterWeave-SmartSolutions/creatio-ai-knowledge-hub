# Manage the Mobile Creatio app using Microsoft Intune admin center | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 797 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/mobile-development/customization/mobile-creatio-for-intune

## Description

One of the administrator priorities is to ensure end users have access to the
apps they need for their work. To do this, administrators can use Microsoft
Intune to manage the custom apps that users use. This functionality also
facilitates additional data protection while managing devices. Learn more:
official vendor documentation.

## Key Concepts

role, operation, package, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.2

On this page

Level: intermediate

One of the administrator priorities is to ensure end users have access to the
apps they need for their work. To do this, administrators can use Microsoft
Intune to manage the custom apps that users use. This functionality also
facilitates additional data protection while managing devices. Learn more:
[official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/apps/app-management).

Before you start managing the app in Microsoft Intune, sign in to the
[Microsoft Intune admin center](https://intune.microsoft.com/) and make sure
your user has the "Application administrator" role.

## 1\. Create a group to manage users and add users to the group​

Instructions:
[official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/fundamentals/quickstart-create-group).

For example, create the "Mobile users" group.

## 2\. Add the app to the Microsoft Intune admin center​

You can add the Mobile Creatio app to the Microsoft Intune admin center in the
following ways:

- using app package file for the Android app
- using App Store for the iOS app

### Add the Android app​

Add the Android app to the Microsoft Intune admin center. To do this:

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_AddTheAndroidApp.gif)

1. **Receive app package file** for the Android app. To do this, contact Creatio
   support (`support@creatio.com`).

2. Click **Apps** → **All apps** → **Add**.

3. **Select the app type**.

| Property | Property value | App type | Line-of-business app |
| -------- | -------------- | -------- | -------------------- |

Click **Select**.

4. **Fill out the app properties**.

| Property | Property value | **App information** tab | Select file | Click **Select app package file** → ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_add_file.png) → select the _.apk or _.ipa file of the Mobile Creatio app → **OK** | Publisher | An arbitrary value. For example, "Creatio." | Target platform | Android device administrator | Category | Business | **Assignments** tab | Available with or without enrollment | Click **Add group** → select your group → **Select** |
| -------- | -------------- | ----------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------- | --------------- | ---------------------------- | -------- | -------- | ------------------- | ------------------------------------ | ---------------------------------------------------- |

5. Click **Create**.

**As a result** , your Mobile Creatio app on the Android platform will be added
to the Microsoft Intune admin center.

### Add the iOS app​

Add the iOS app to the Microsoft Intune admin center using App Store. To do
this:

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_AddTheIosApp.gif)

1. Click **Apps** → **All apps** → **Add**.

2. **Select the app type**.

| Property | Property value | App type | iOS store app |
| -------- | -------------- | -------- | ------------- |

Click **Select**.

3. **Fill out the app properties**.

| Property | Property value | **App information** tab | Select app | Click **Search the App Store** → **Mobile Creatio for Intune** → **Select** | Category | Business | **Assignments** tab | Available with or without enrollment | Click **Add group** → select your group → **Select** |
| -------- | -------------- | ----------------------- | ---------- | --------------------------------------------------------------------------- | -------- | -------- | ------------------- | ------------------------------------ | ---------------------------------------------------- |

4. Click **Create**.

**As a result** , your Mobile Creatio app on the iOS platform will be added to
the Microsoft Intune admin center.

## 3\. Create the app compliance policy​

To create a compliance policy:

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_CreateThePolicy.gif)

1. Click **Devices** → **Compliance** → **Create policy**.

2. **Create a policy**.

| Property | Property value | Platform | "Android device administrator" or "iOS/iPadOS" |
| -------- | -------------- | -------- | ---------------------------------------------- |

Click **Create**.

3. **Fill out the policy properties**.

| Property | Property value | **Basics** tab | Name | An arbitrary value. For example, "Android" or "iOS." | **Assignments** tab | Included groups | Click **Add groups** → select your group → **Select** |
| -------- | -------------- | -------------- | ---- | ---------------------------------------------------- | ------------------- | --------------- | ----------------------------------------------------- |

4. Click **Create**.

**As a result** , the compliance policy for the Mobile Creatio app will be
created.

## 4\. Set up the app protection policies​

To set up the app protection policies:

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_CreateAnAppProtectionPolicy.gif)

1. Click **Apps** → **App protection policies** → **Create policy** →
   **Android** or **iOS/iPadOS**.

2. **Fill out the policy properties**.

| Property | Property value | **Basics** tab | Name | An arbitrary value. For example, "Android" or "iOS." | **Apps** tab | Custom apps | Click **Select custom apps** → select your app → **Select** | **Assignments** tab | Included groups | Click **Add groups** → select your group → **Select** |
| -------- | -------------- | -------------- | ---- | ---------------------------------------------------- | ------------ | ----------- | ----------------------------------------------------------- | ------------------- | --------------- | ----------------------------------------------------- |

3. Click **Create**.

**As a result** , the Mobile Creatio app protection policies will be configured.

If needed, you can set up an **additional data protection policy**. For example,
restrict Copy/Paste operation. To do this:

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/MobileIntune/8.1/scr_AdditionalProtection.gif)

1. Click **Apps** → **App protection policies** → select the policy →
   **Properties** → **Edit** the **Data protection** properties.

2. **Edit the data protection properties**.

| Property | Property value | **Data protection** tab → **Data transfer** block | Restrict cut, copy, and paste between other apps | Blocked | Cut and copy character limit for any app | 10  |
| -------- | -------------- | ------------------------------------------------- | ------------------------------------------------ | ------- | ---------------------------------------- | --- |

3. Click **Review + save**.

4. Click **Save**.

**As a result** , the Mobile Creatio app protection policy will include the
additional settings.

## 5\. Set up the device management​

**For Android devices** , set up device administrator enrollment. Instructions:
[official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/enrollment/android-enroll-device-administrator).

**For iOS devices** , add an MDM Push certificate. Instructions:
[official vendor documentation](https://learn.microsoft.com/en-us/mem/intune/enrollment/apple-mdm-push-certificate-get).

---

## Resources​

[Official Microsoft Intune documentation](https://learn.microsoft.com/en-us/mem/intune/)

- 1\. Create a group to manage users and add users to the group
- 2\. Add the app to the Microsoft Intune admin center
  - Add the Android app
  - Add the iOS app
- 3\. Create the app compliance policy
- 4\. Set up the app protection policies
- 5\. Set up the device management
- Resources
