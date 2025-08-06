# Debug Mobile Creatio | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 308
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/mobile-development/debugging-mobile-app/general-procedure

## Description

1.  Run Mobile Creatio to debug using one of the following ways:

## Key Concepts

mobile app, contact

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: intermediate

1. **Run Mobile Creatio** to debug using one of the following ways:

Mobile device

     1. Receive an `app-debug.apk` file of the Mobile Creatio app to debug. To do this, contact Creatio support (`support@creatio.com`).
     2. Install the Mobile Creatio on your mobile device.
     3. Run the app on the mobile device.
     4. Connect the mobile device to your PC via USB.

Mobile app emulator

Set up the mobile app emulator. Instructions:
[Set up the mobile app emulator](https://academy.creatio.com/documents?ver=8.0&id=15029).

2. **Open Google Chrome** on the PC.

3. **Open the Inspect with Chrome Developer Tools tab**. To do this, enter the
   `chrome://inspect/#devices` URL in the browser address bar. This opens the
   **Devices** tab that includes the list of connected devices. The link to
   Mobile Creatio is `com.creatio.mobileapp`.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/DebugMobileApp/8.0/scr_ConnectedDevices.png)

4. **Display the connected device** (optional).

If the connected device is missing from the **Devices** tab, check the device
authorization. To do this:

     1. Download Android Debug Bridge (adb). [Download](https://developer.android.com/studio/releases/platform-tools).

     2. Open the command line.

     3. Go to the directory that contains the `adb.exe` file. To do this, run the command below.

            cd [Path to the directory that contains the adb.exe file]


     4. Open the list of connected devices. To do this, run the command below.

            adb.exe devices


     5. If you see `unauthorized` status for the mobile device, authorize the device.

        1. Disconnect the USB cable.
        2. Revoke USB debugging permissions on your device.
        3. Reconnect the USB cable.
        4. Set **Trust this computer?** to "Yes."

5. **Click the inspect link** under the link to Mobile Creatio. This opens an
   app debugging window.

6. **Open the Sources tab**.

7. **Find functionality** to debug. Most of the classes are in the
   `android_asset/www/js/terrasoft-all-combined.js` file.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/SetUpTheEmulator/scr_sources_tab.png)

8. **Debug Mobile Creatio**.

---

## See also​

[Set up the mobile app emulator](https://academy.creatio.com/documents?ver=8.0&id=15029)

---

## Resources​

[Official Android Studio website](https://developer.android.com/studio)

- See also
- Resources
