# Set up the mobile app emulator | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 625 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/mobile-development/debugging-mobile-app/overview

## Description

The Mobile Creatio is a hybrid app (i.&nbsp;e., a mobile app packaged in a
native UI). Learn more: Mobile app basics.

## Key Concepts

package, mobile app, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: beginner

The **Mobile Creatio** is a hybrid app (i. e., a mobile app packaged in a native
UI). Learn more:
[Mobile app basics](https://academy.creatio.com/documents?ver=8.0&id=15851).

**Mobile app debugging** is verification that the custom functionality of the
Mobile Creatio works as expected.

Keep in mind the following **limitations** when you create an emulator using
Android Studio:

- You can only run the emulator created in Android Studio on a CPU that supports
  **Intel Virtualization Technology (VT-x)**. VT-x technology can be disabled by
  default. Contact the system administrator to enable it. Learn more:
  [Wikipedia](https://en.wikipedia.org/w/index.php?title=X86_virtualization&oldid=1120646014#Intel-VT-x).
- You cannot run the emulator created in Android Studio on a virtual machine.

## 1\. Create the mobile app emulator​

1. **Download and install Android Studio**.
   [Download](https://developer.android.com/studio/).

2. **Set up Android Studio**.
   1. Select the **Custom** setup type → click **Next**.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_custom_setup_type.png)

     2. Install the latest version of Android SDK. To do this, select the **Android SDK Platform** checkbox → click **Next**.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_install_android_sdk.png)

     3. Verify the settings → click **Next**.

     4. Sign the **License agreement**. To do this, read the agreement → select the **Accept** checkbox → click **Finish**. The installation of chosen components might take some time.

     5. Click **Finish**. This opens the **Welcome to Android Studio** window.

3. **Receive an** `app-debug.apk` **file** of the Mobile Creatio app to debug.
   To do this, contact Creatio support (`support@creatio.com`).

4. **Create a project**.
   1. Open the **Projects** tab.
   2. Download the `app-debug.apk` file. To do this, click **More Actions** →
      **Profile or Debug APK** → select the `app-debug.apk` file → **OK**. The
      project creation might take some time.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_download_the_apk_file.png)

5. **Create an emulator**. To do this, go to the Android Studio's toolbar →
   click
   ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_open_menu_button.png)
   → **Tools** → **Device Manager**.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_create_emulator.png)

6. **Create device**.
   1. Go to the **Device Manager** panel → click
      ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_add_device_button.png)
      → **Create Virtual Device**. This opens the **Add Device** window.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_create_device.png)

     2. Select device. To do this, select the **Phone** form factor → select the mobile device → click **Next**. For example, select Pixel 9.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_select_device.png)

     3. Change the recommended settings of the selected virtual device if needed.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_change_settings.png)

     4. Click **Finish**.

**As a result** , the emulator will be added to the **Device Manager** panel.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_created_emulator.png)

## 2\. Run Mobile Creatio using the mobile app emulator​

1. **Run an emulator**. To do this, go to the **Device Manager** panel → select
   created emulator → click
   ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_run_emulator_button.png).
   For example, run the Pixel 9 emulator.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_run_emulator.png)

The emulator startup might take some time. As a result, the emulator will be
run.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_emulator_on_device.png)

2. **Run Mobile Creatio** using the emulator. To do this, go to the toolbar →
   click
   ![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_run_mobile_creatio_button.png).

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_run_mobile_creatio.png)

If Android Studio displays the `Please select Android SDK` error when you run
Mobile Creatio using the emulator, **install the missing components**.

     1. Restart Android Studio.
     2. Click the **Install missing platform and fix project** link. This opens the **SDK QuickFix Installation** window and runs the installation. The installation might take some time.
     3. Click **Finish**.

The emulator startup might take some time.

As a result, Mobile Creatio will be run using the emulator created in Android
Studio.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/8.2/scr_mobile_creatio_on_device.png)

3. **Set up the Creatio application server on IIS** if you need to connect to
   Mobile Creatio on-site. Instructions:
   [Set up Creatio application server on IIS](https://academy.creatio.com/documents?ver=8.0&id=2142)
   (user documentation).

4. **Log in to Mobile Creatio** using the same user credentials as the main
   Creatio app.

After that, you can **debug Mobile Creatio**. Instructions:
[Debug Mobile Creatio](https://academy.creatio.com/documents?ver=8.0&id=15904&anchor=title-2545-2).

---

## See also​

[Work with mobile app basics](https://academy.creatio.com/documents?ver=8.0&id=15851)

[Set up Creatio application server on IIS](https://academy.creatio.com/documents?ver=8.0&id=2142)
(user documentation)

[Debug Mobile Creatio](https://academy.creatio.com/documents?ver=8.0&id=15904)

---

## Resources​

[Official Android Studio website](https://developer.android.com/studio)

[Intel Virtualization Technology](https://en.wikipedia.org/w/index.php?title=X86_virtualization&oldid=1120646014#Intel-VT-x)
(Wikipedia)

- 1\. Create the mobile app emulator
- 2\. Run Mobile Creatio using the mobile app emulator
- See also
- Resources
