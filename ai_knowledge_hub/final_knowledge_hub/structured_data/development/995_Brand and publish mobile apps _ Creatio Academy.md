# Brand and publish mobile apps | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1860 **URL:**
https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/mobile-application-branding/brand-and-publish-mobile-apps-built

## Description

You can use your logos and names to brand a mobile app built on Mobile Creatio
using the SDKConsole utility.

## Key Concepts

workflow, section, system setting, package, mobile app, notification, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

On this page

Level: advanced

You can use your logos and names to brand a mobile app built on Mobile Creatio
using the **SDKConsole utility**.

**General procedure** to set up the SDKConsole utility:

1. Perform the preliminary setup. Read more >>>
2. Install and set up the SDKConsole utility. Read more >>>
3. Run the SDKConsole utility. Read more >>>

## 1\. Perform the preliminary setup​

1. **Ensure you can publish the app**.
   - For **iOS** app, you must be enrolled into Apple Developer program. Learn
     more:
     [Apple Developer Program](https://developer.apple.com/programs/enroll/).
   - For **Android** app, you must have a Google Play developer account. Learn
     more:
     [Google Play Console](https://developer.android.com/distribute/console).

2. **Enable Firebase Cloud Messaging** to send push notifications.
   1. Sign in to [Firebase website](https://firebase.google.com/).

   2. Click **Go to console**.

   3. Create a project in the console.
      - For **iOS** app:
        [Create a Firebase project](https://firebase.google.com/docs/ios/setup#create-firebase-project)
        (official vendor documentation).
      - For **Android** app:
        [Create a Firebase project](https://firebase.google.com/docs/android/setup#create-firebase-project)
        (official vendor documentation).

   4. Register your iOS and/or Android app in the project.
      - For **iOS** app:
        [Register your app with Firebase](https://firebase.google.com/docs/ios/setup#register-app)
        (official vendor documentation).
      - For **Android** app:
        [Register your app with Firebase](https://firebase.google.com/docs/android/setup#register-app)
        (official vendor documentation).

   5. Download the config files for the app and save them to your local machine.
      - For **iOS** app:
        [Get config file for your iOS app](https://support.google.com/firebase/answer/7015592?hl=en&sjid=15581299455747132795-EU#ios&zippy=%2Cin-this-article)
        (official vendor documentation).
      - For **Android** app:
        [Get config file for your Android app](https://support.google.com/firebase/answer/7015592?hl=en&sjid=15581299455747132795-EU#android&zippy=%2Cin-this-article)
        (official vendor documentation).

   6. Specify additional settings to receive Firebase push notifications
      (on-site only).
      - For **iOS** app:
        [If your Apple devices aren't getting Apple push notifications](https://support.apple.com/en-us/102266)
        (official vendor documentation).
      - For **Android** app:
        [Android Enterprise Network Requirements](https://support.google.com/work/android/answer/10513641?hl=en)
        (official vendor documentation).

   7. Retrieve the service account key. To do this, open the Firebase project →
      click
      ![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/Mobile/icn_firebase.png)
      → **Project settings** → **Cloud Messaging** tab → **Firebase Cloud
      Messaging API (V1)** → **Manage Service Accounts**.

   8. Create a service account if needed. Learn more:
      [Firebase Service Accounts Overview](https://firebase.google.com/support/guides/service-accounts)
      (official vendor documentation).

   9. Create a new service account key. To do this, select a service account →
      **Keys** tab → **Add key** → **Create new key** → **JSON** → **Create** →
      save the generated JSON file to your local machine.

   10. Open the uploaded file and copy the content.

View an example of the file content below.

Example of the file content

            {
                "type": "service_account",
                "project_id": "your-project-id",
                "private_key_id": "your-private-key-id",
                "private_key": "-----BEGIN PRIVATE KEY-----\nyour-service-account-key\n-----END PRIVATE KEY-----\n",
                "client_email": "your-client-email",
                "client_id": "your-client-Id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test1-806%40your-project-id.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }


Where `your-project-id`, `your-private-key-id`, `your-service-account-key`,
`your-client-email`, `your-client-Id` are parameter values generated by Firebase
Cloud Messaging.

     11. Open the **System settings** section in Creatio. To do this, click ![](https://academy.creatio.com/docs/sites/en/files/images/NoCodePlatform/Manage_Apps/btn_system_designer_8_shell.png) in the top right → **System setup** → **System settings**.

     12. Save the copied content to the "FirebaseAccountService" (`FirebaseAccountService` code) system setting.

3. **Install Java development kit**.
   - For **iOS** app, install Java development kit version 8.
     [Download the file](https://www.oracle.com/java/technologies/downloads/#java8).
   - For **Android** app, install Java development kit version 17.
     [Download the file](https://www.oracle.com/java/technologies/downloads/#java17).

4. **Register your app with App Store Connect** (iOS app only). Instructions:
   [App Store Connect workflow](https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-workflow)
   (official vendor documentation).

5. **Install the APNs certificates into Firebase** (iOS app only).
   1. Open the
      [Certificates page](https://developer.apple.com/account/ios/certificate/).
   2. Add and install development and production
      `Apple Push Notification service SSL` certificates into your Mac.
   3. Generate, download and install provisioning profiles.
   4. Upload the \*.p12 files exported from **Keychain Access** in the Firebase
      settings on the **Cloud Messaging** tab.

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots/Mobile/scr_apns_certificates.png)

6. **Install J2ObjC** (iOS app only). The native functionality of the Mobile
   Creatio app is partly written in Java. The J2ObjC utility for Java code to
   Objective-C translation is required for shared use on iOS. Learn more:
   [J2ObjC overview](https://developers.google.com/j2objc/) (official vendor
   documentation). To install J2ObjC:
   1. Download the J2ObjC release version archive (2.0.5) to a Mac.
      [Download the file](https://github.com/google/j2objc/releases/download/2.0.5/j2objc-2.0.5.zip)
      (GitHub).
   2. Unpack the archive into your user home directory
      (`MacintoshHD/Users/MyUser/`). The unpacked archive must contain the
      `dist` directory.
   3. Rename the unpacked archive directory to `j2objc`.

## 2\. Install and set up the SDKConsole utility​

1. **Send the email address** that is or will be associated with your GitLab
   account to Creatio support (`support@creatio.com`).

2. **Sign up for the SDKConsole project** using the link received from the
   Creatio support. This accesses the SDKConsole project.

3. **Sign up for GitLab** using the link received from the Creatio support and
   follow the instructions.

If you sign in using a third-party service, make sure that you have a password
set up for your GitLab account. To do this, click the profile icon in the top
right → **Edit profile** → **Password**.

4. **Install the SDKConsole utility**.

Install the SDKConsole utility on Mac

The utility supports iOS and Android on Mac. You will be requested to enter an
administrator password on your Mac during the installation. If you do not know
or remember the password, ask your system administrator or the owner of the
Mac. 1. Install XCode. [Download the file](https://developer.apple.com/xcode/).

     2. Install Git. [Download the file](https://git-scm.com/download/mac).

     3. Download the current version of the SDKConsole utility to a directory to which you have all permissions. To download the utility, run the following Git command.

            git clone https://gitlab.com/bpmonlinemobileteam/sdkconsole.git SDKConsole


     4. Open terminal and go to the directory where the SDKConsole utility is located.

     5. Install brew. To do this, run the following command at the terminal.

            ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)


     6. Run the `./install` command at the terminal.

     7. If the command was successful, install fastlane utility plugins. To do this, run the `./install_plugins` command at the terminal. When asked whether fastlane should modify the Gemfile, enter `y`.

Install the SDKConsole utility on Windows

The utility supports only Android on Windows. 1. Install or update Node.js® and
npm package manager if needed. [Download the file](https://nodejs.org/en/).

     2. Install Git. [Download the file](https://git-scm.com/download/win).

     3. Install Android Studio. [Download the file](https://developer.android.com/studio).

     4. Download the current version of the SDKConsole utility to any directory. To do this, run the following Git command.

            git clone https://gitlab.com/bpmonlinemobileteam/sdkconsole.git SDKConsole


     5. Open the command prompt and go to the directory where the SDKConsole utility is located.

     6. Run the `npm install` command at the command prompt.

5. **Update the SDKConsole utility** if needed.
   1. Back up the `SDK.config` file that contains the user settings. That way
      you will not have to reconfigure the utility.
   2. Download the current version of the SDKConsole utility from the Git
      repository.
   3. Unpack the archive into the directory where the SDKConsole utility is
      located.
   4. Move the `SDK.config` backup to the utility directory.

6. **Configure the SDKConsole utility**. To do this, configure the settings in
   the `SDK.config` file. Learn more:
   [SDKConsole utility settings](https://academy.creatio.com/documents?id=15969).
   Make sure that you do not use a single backslash (`\`) in your file paths.

View an example of the `SDK.config` file below.

Example of the SDK.config file

         {
             "name": "Creatio beta",
             "web_resources_path": "res/web",
             "tasks": ["prepare", "build", "deploy"],
             "use_extended_logging": true,
             "server_url": "https://mysite.creatio.com/",
             "iOS": {
                 "repository_path": "https://gitlab.com/bpmonlinemobileteam/ios.git",
                 "source_path": "",
                 "google_service_info_file": "",
                 "launch_storyboard_image_path": "res//LaunchStoryboard.png",
                 "app_identifier": "com.myapp.mobile",
                 "app_icon_path": "../res/AppIcon.png",
                 "version_number": "7.13.9",
                 "build_number": "2",
                 "app_store_login": "some@gmail.com",
                 "certificate_path": "/Users/your_user_dir/ios_distribution.cer",
                 "certificate_password": "private_key_password_of_certificate",
                 "apple_2FA_specific_password": "apple_specific_password",
                 "testflight_changelog": "My what's new"
             },
             "Android": {
                 "build_type": "debug",
                 "repository_path": "https://gitlab.com/bpmonlinemobileteam/android.git",
                 "source_path": "",
                 "google_service_info_file": "",
                 "package_name": "com.myapp.mobile",
                 "version_number": "1.1.1",
                 "build_number": 2,
                 "native_resources_path": "res/android/res",
                 "key_file": "C:/hybrid/platforms/android/androidappkey",
                 "store_password": "android_app_distribution_password",
                 "key_alias": "some_key_alias",
                 "key_password": "key_password"
             }
         }


## 3\. Run the SDKConsole utility​

### Run the SDKConsole utility on Mac​

1. Open **Terminal** in the directory where the SDKConsole utility is located.
2. Run the `./build` **command**.

**As a result** , depending on the `tasks` parameter value specified in the
`SDK.config` file, the SDKConsole utility can execute different actions listed
in the table below.

| `tasks` parameter value | Result of the SDKConsole utility execution | prepare | Brands your iOS and/or Android project. You get a ready project, but you need to build and publish the app manually in AppStore and/or Google Play. | build | Builds the project and saves an assembled _.ipa iOS app file and/or _.apk Android app file to the utility directory. | deploy | iOS only. Immediately publishes the app to TestFlight using the authentication parameters specified in the `SDK.config` file. |
| ----------------------- | ------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |

If something goes wrong while the SDKConsole utility is running on Mac, you will
receive one of the errors listed below.

**Error**. The `Unable to determine Android SDK directory` error on Mac.

**Solution**.

1. Open **Terminal**.

2. Run the following commands at the terminal.
   echo "export ANDROID_HOME=~/Library/Android/sdk;export
   PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools:$ANDROID_HOME/platforms;" >>
   ~/.bash_profile source ~/.bash_profile  


---

**Error**. The
`Couldn't find the specified scheme 'bpm'online'. Please make sure that the scheme is shared...`
error when running the build for an iOS project on Mac.

**Solution**. Re-build the app. If this does not help, take the following steps:

1. Open the iOS project (`BPMonlineMobile.xcworkspace`) in XCode.
2. Select the current build scheme. If the `[bpm'online]` scheme is not
   selected, select it in the list.
3. Click the current scheme once more and select **Edit scheme...** in the list.
4. Select the **Shared** checkbox.
5. Close XCode.
6. Run the `./build` command at the Terminal.

---

**Error**. Remove the `permission denied` message for my build in the Mac
Terminal.

**Solution**. Run the following command at the Terminal.

    chmod -R +x build

---

**Error**. The
`Tool 'agvtool' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance`
error on Mac.

**Solution**. Run the following command at the Terminal.

    sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

---

**Error**. The `function fs.copyFileSync is undefined` error during the build on
Mac.

**Solution**. Run the following commands at the Terminal.

    brew link --overwrite node
    brew postinstall node

### Run the SDKConsole utility on Windows​

1. Open the **command line**.
2. Go to the **directory where the SDKConsole utility is located**.
3. Run the `node SDKConsole.js` **command**.

**As a result** , depending on the `tasks` parameter value specified in the
`SDK.config` file, the SDKConsole utility can execute different actions listed
in the table below.

| `tasks` parameter value | Result of the SDKConsole utility execution | prepare | Brands your Android project. You get a ready project, but you need to build and publish the app manually in Google Play. | build | Builds the project and saves an assembled \*.apk Android app file to the utility directory. |
| ----------------------- | ------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------ | ----- | ------------------------------------------------------------------------------------------- |

If something goes wrong while the SDKConsole utility is running on Windows, you
will receive the error listed below.

**Error**. The `Unable to determine Android SDK directory` error on Windows.

**Solution**. Specify the `ANDROID_HOME` environment variable where you need to
provide the path to the Android SDK specified during the installation of Android
Studio.

---

## Resources​

[Apple Developer Program](https://developer.apple.com/programs/enroll/)
(official Apple documentation)

[Google Play Console](https://developer.android.com/distribute/console)
(official Google documentation)

[Official Firebase website](https://firebase.google.com/)

[Official Firebase documentation for Apple platforms](https://firebase.google.com/docs/ios/setup)

[Official Firebase documentation for Android](https://firebase.google.com/docs/android/setup)

[Java development kit version 8 (for iOS app)](https://www.oracle.com/java/technologies/downloads/#java8)
(official Oracle documentation)

[Java development kit version 17 (for Android app)](https://www.oracle.com/java/technologies/downloads/#java17)
(official Oracle documentation)

[Official J2ObjC command-line tool documentation](https://developers.google.com/j2objc/)

- 1\. Perform the preliminary setup
- 2\. Install and set up the SDKConsole utility
- 3\. Run the SDKConsole utility
  - Run the SDKConsole utility on Mac
  - Run the SDKConsole utility on Windows
- Resources
