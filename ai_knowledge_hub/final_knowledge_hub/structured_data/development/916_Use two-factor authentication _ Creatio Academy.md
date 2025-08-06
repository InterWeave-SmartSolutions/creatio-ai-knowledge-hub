# Use two-factor authentication | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 490 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.2/creatio-basics/use-two-factor-authentication

## Description

Two-factor authentication (2FA) functionality lets you secure your identity by
adding a verification code sent via email/SMS or generated in an authenticator
app when you log in to Creatio or change your password. 2FA also lets you
recover your password on your own.

## Key Concepts

configuration, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/creatio-basics/use-two-factor-authentication)**
(8.3).

Version: 8.2

On this page

Two-factor authentication (2FA) functionality lets you secure your identity by
adding a verification code sent via email/SMS or generated in an authenticator
app when you log in to Creatio or change your password. 2FA also lets you
recover your password on your own.

Fig. 1 2FA form

![Fig. 1 2FA form](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/use_two-factor_authentication/scr_2fa_form.png)

note

If you enter the verification code incorrectly multiple times, your user account
will be temporarily locked out or deactivated.

In general, 2FA setup is performed by the system administrator. However, you
might need to take some steps on your own depending on the configuration.

## Connect an authenticator app​

If authenticator app is the primary 2FA method in Creatio, you need to connect
an authenticator app when you first log in. To do this:

1. **Install an authenticator app** to your mobile device. You can use any app
   of your choice, for example, Google Authenticator, Microsoft Authenticator.

2. **Scan the QR code** displayed in Creatio using the app.

3. **Enter the code** generated in the app in Creatio (Fig. 2).

Fig. 2 Enter the app verification code

![Fig. 2 Enter the app verification code](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/use_two-factor_authentication/scr_connect_authenticator_app.png)

4. **Click** **Connect**.

**As a result** , Creatio will connect the authenticator app. You can disconnect
it on the user profile page, for example, if you lose access to the device or
want to use a different app.

note

If authenticator app is enabled but is not the primary 2FA method, you can
connect the app on your own on **Authentication settings** tab of the user
profile page.

## Disconnect an authenticator app​

If you want to use a different device or a different authenticator app, you can
temporarily disconnect the authenticator app from your account. To do this:

1. **Open** the user profile page.
2. **Open** the **Authentication settings** tab.
3. **Click** **Disconnect authenticator app**. This opens a window.
4. **Enter** the verification code from the authenticator app in the
   **Verification code** field → **Verify**.

**As a result** , Creatio will disconnect the authenticator app from your
account.

If you lose access to the device or delete your authenticator app, ask the
system administrator to disconnect the authenticator app for you.

## Generate recovery codes​

If the system administrator enables this option, you can generate a set of
personal one-time recovery codes and use them to pass 2FA in case you lose
access to the main 2FA option. To do this:

1. **Open** the user profile page.
2. **Open** the **Authentication settings** tab.
3. **Click** **Generate recovery codes**. This opens a window.
4. **Pass 2FA**.

**As a result** , Creatio will generate a set of one-time recovery codes. We
recommend backing them up in a secure manner.

You will be able to re-generate recovery codes or delete them in the future.
Doing so invalidates the previous set of codes.

---

## See also​

[Set up two-factor authentication](https://academy.creatio.com/documents?id=2538)

- Connect an authenticator app
- Disconnect an authenticator app
- Generate recovery codes
- See also
