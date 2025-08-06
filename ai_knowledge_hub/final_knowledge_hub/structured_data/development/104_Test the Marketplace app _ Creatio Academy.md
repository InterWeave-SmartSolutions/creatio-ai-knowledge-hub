# Test the Marketplace app | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 392 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/app-development/test-the-app

## Description

Test the software solution before you publish it to verify its operability. Test
the solution in the pre-production environment.

## Key Concepts

package, account, marketplace

## Use Cases

building applications, custom development, API integration

## Content

On this page

Level: intermediate

Test the software solution before you publish it to verify its operability. Test
the solution in the pre-production environment.

Developing and implementing a Marketplace app is the same as the Creatio app.
Learn more about developing and implementing a Creatio instance:
[Delivery management process](https://academy.creatio.com/documents?id=15202).

Perform the testing as part of the Marketplace app delivery. The **steps** to
deliver the app are as follows:

1. Register a pre-production environment.
2. Transfer the Marketplace app to the pre-production environment.

## 1\. Register a pre-production environment​

Use the pre-production environment to test the Marketplace app functionality.

To **register a testing environment app** , order a trial of the product app
that is selected as a development environment (i. e. the app specified on the
**Development site** tab).

You can order a trial in the following **ways** :

- on the trial order page via the [link](https://www.creatio.com/trial/creatio)
- using the Developer profile

To **order a trial using the Developer profile** :

1. Open the Developer profile.

2. Click **Applications** → **Test environment** on the properties panel.

3. Click the link to order a trial.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/TestingMarketplaceApplication/8.0/scr_order_trial.png)

4. Select the relevant product on the opened page and click **Try it free**.

5. Log in to an existing Creatio account or create a new account.

As a result, the pre-production environment is ready to use. The user receives
an email with the activation/deactivation dates of the testing environment app
and a link to the testing environment app to the email address specified when
registering.

## 2\. Transfer the Marketplace app to the pre-production environment​

Transfer the Marketplace app to the pre-production environment to test its
operability.

To **transfer the Marketplace app to the pre-production environment** :

1. Export packages that contain the Marketplace app as a _.zip archive.
   Instructions:
   [Delivery management process](https://academy.creatio.com/documents?id=15202&anchor=title-2068-3).
   If the Marketplace app functionality is implemented in multiple packages,
   combine the exported _.gz archives of packages into a single \*.zip archive.
2. Import a _.zip archive of Marketplace app packages or a single _.gz package
   archive into the testing environment app. Instructions:
   [Delivery management process](https://academy.creatio.com/documents?id=15202&anchor=title-2068-4).
3. Verify the operability of the developed functionality. If you find an error,
   improve the functionality by fixing it. After that, repeat steps 1–2.

---

## See also​

[Delivery management process](https://academy.creatio.com/documents?id=15202)

---

## Resources​

[Creatio trial order page](https://www.creatio.com/trial/creatio)

[Marketplace updates](https://academy.creatio.com/docs/8.x/dev/development-for-creatio-marketplace/category/marketplace-updates)

- 1\. Register a pre-production environment
- 2\. Transfer the Marketplace app to the pre-production environment
- See also
- Resources
