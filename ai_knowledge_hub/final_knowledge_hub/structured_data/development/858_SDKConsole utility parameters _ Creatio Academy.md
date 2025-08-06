# SDKConsole utility parameters | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 738 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/mobile-development/customization/mobile-application-branding/references/sdkconsole-utility-settings

## Description

Common parameters

## Key Concepts

configuration, section, detail, integration, package, mobile app, notification,
contact, account

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

Level: beginner

## Common parameters​

    name

Name of your app.

    web_resources_path

Path to the directory that contains the resources used in the app, i. e., the
logo and background on the login page.

    tasks

Actions the utility executes. This is a string array where you can specify a
combination of the tasks.

Available values

| prepare | Preparation/rebranding of your iOS/Android project. This step makes all the necessary changes. You will get a finished project you can publish in AppStore and Google Play. | build | Build the project. You will get an assembled _.ipa iOS app file and/or _.apk Android app file. | deploy | Publish the app to TestFlight. iOS only. |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------- | ------ | ---------------------------------------- |

    use_extended_logging

Show detailed logs in the terminal when the utility is running. The recommended
value is `true`. If set to `false`, the terminal displays only the currently
executed step without details.

    server_url

Default server. The server URL will be automatically specified on the login page
when you log in to the app for the first time.

    repository_path

Path to the GitLab repository that hosts the original Android/iOS project.

    source_path

Path to the local Windows/Mac directory where the original Android/iOS project
is located. If you specify this parameter the utility uses it in place of the
`repository_path` parameter.

    google_service_info_file

Path to the `GoogleService-Info.plist` (iOS) or `google-services.json` (Android)
file downloaded from the Firebase project. Required to connect to the Firebase
push notification service.

    version_number

App version in the following format: `0.0.1`.

    build_number

Build number (string). Always update the build number before you perform the
`deploy` task.

    launch_storyboard_image_path

Path to the image displayed when the app starts (2732x2732 px). iOS only.

    app_identifier

A unique app ID, for example, `com.myapp.mobile`. This is the Bundle ID
specified when you registered the app in App Store Connect. iOS only.

    app_icon_path

Path to the app icon (1024x1024 px). This is a master image the utility uses to
generate the required icons for current iOS devices. iOS only.

    app_store_login

Account (Apple ID) required to connect to App Store Connect / TestFlight. iOS
only.

    certificate_path

Path to the distribution certificate required when publishing to TestFlight. iOS
only.

    certificate_password

Certificate password. To restore the password, contact the certificate author.
iOS only.

    apple_2FA_specific_password

Specific password. iOS only.

Currently, all Apple accounts support two-factor authentication. To enable
third-party services to connect to Apple services, the `app-specific passwords`
were added. To get a specific password:

1. Open the [Apple ID](https://appleid.apple.com/#!&page=signin) URL while
   signed in to your Apple account.
2. Open the **Security** section → **Generate password...** command.
3. Follow the instructions to get a new password generated.


    testflight_changelog

Description of the published changes to TestFlight (what’s new). The description
is published for the primary app language set in App Store. iOS only.

    app_provision_name

Distribution provisioning name to sign the Creatio app target.

    callerid_app_provision_name

Distribution provisioning name to sign the `CallerId` target in the Creatio
project.

    build_type

Build type. Android only.

Available values

| debug | Build for debugging | release | Release build | bundleRelease | Release build for Google Play platform | release-unsigned | Unsigned build | intuneRelease | Build for Microsoft Intune integration |
| ----- | ------------------- | ------- | ------------- | ------------- | -------------------------------------- | ---------------- | -------------- | ------------- | -------------------------------------- |

    package_name

A unique app ID, for example, `com.myapp.mobile`. Android only.

    native_resources_path

Path to app resources, such as the app icon and the startup image. Learn more:
[official vendor documentation](https://developer.android.com/studio/write/create-app-icons#about).

Structure the contents of this directory similarly to the `res` folder in the
Android project. The directory can contain subdirectories that have drawable,
drawable-xhdpi, and other icons. Android only.

    key_file

Path to the key file (keystore) required to sign the app. Learn more:
[official vendor documentation](https://developer.android.com/studio/publish/app-signing).
Android only.

    store_password

Password for the keystore required to sign the app. Android only.

    key_alias

The key alias. Android only.

    key_password

The password of the alias from the `key_alias` parameter in the keystore.
Android only.

## Microsoft Intune parameters​

    intune_config

Configuration for building wrapped/integrated Intune app. The list of parameters
is based on the mobile OS.

Available values (Android only)

| app_wrapping_tool_script_path | Path to the directory that includes Intune wrapping tool. | build_tools_path | Path to the Android build tools usually installed with Android Studio. Learn more: [Launch the mobile app emulator created in Android Studio](https://academy.creatio.com/documents?ver=8.2&id=15029). |
| ----------------------------- | --------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

Available values (iOS only)

| intune_mam_packager_path | Path to the Intune wrapping tool. | intune_app_provision_file_path | Path to the distribution provisioning file. | intune_callerid_app_provision_file_path | Path to the `CallerId` distribution provisioning file. | intune_sha1 | SHA1 of Apple/iOS Distribution certificate. Instructions: official [macOS](https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request) and [Windows](https://learn.microsoft.com/en-us/xamarin/ios/deploy-test/app-distribution/app-store-distribution/?tabs=windows#creating-a-distribution-certificate) vendor documentation. |
| ------------------------ | --------------------------------- | ------------------------------ | ------------------------------------------- | --------------------------------------- | ------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

- Common parameters
- Microsoft Intune parameters
