# Integrate chat channels | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 497 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/chat-channels-integration

## Description

Chats let your company's contact center agents process messages from popular
chat messengers in Creatio. Learn more: Set up chat processing (user
documentation).

## Key Concepts

integration, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/chat-channels-integration)**
(8.3).

Version: 8.0

On this page

Level: intermediate

Chats let your company's contact center agents process messages from popular
chat messengers in Creatio. Learn more:
[Set up chat processing](https://academy.creatio.com/documents?ver=8.0&id=2382)
(user documentation).

A **chat channel** is a source from which Creatio receives customer messages.

Creatio lets you integrate the following **chat channels** :

- Facebook Messenger
- Telegram
- WhatsApp

## Integrate a Facebook Messenger channel​

Before you start the integration, take the following steps:

1. **Make sure Creatio cloud services are available**.
2. **Make sure Facebook services are available**.

Learn more:
[Set up Facebook Messenger integration](https://academy.creatio.com/documents?ver=8.0&id=2384)
(user documentation).

Creatio interacts with Facebook pages on behalf of the Creatio Social app that
accesses the cloud services. The following actions are performed on the cloud
service level:

- Subscribe to new incoming messages from the Facebook page.
- Bind the subscription to the Creatio instance.

After the **Facebook page receives an incoming message** , Creatio cloud
services forward it to the Creatio client. If the Creatio instance is
unavailable, the services queue the message to resend it later.

The **Creatio instance sends outgoing messages** directly without using the
cloud services.

View the interaction diagram of Creatio on-site and a Facebook Messenger channel
in the figure below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ChatChannels/8.1/scr_FacebookMessenger.png)

## Integrate a Telegram channel​

Before you start the integration, take the following steps:

1. **Create an API for each Telegram chatbot**.
2. **Specify the API in Creatio settings**.

Creatio does not use proxy services for Telegram integration. Learn more:
[Set up Telegram integration](https://academy.creatio.com/documents?ver=8.0&id=2354)
(user documentation).

The **Creatio instance receives an incoming message** using long polling. Learn
more:
[Long polling](https://en.wikipedia.org/w/index.php?title=Push_technology&oldid=1052758691#Long_polling)
(Wikipedia). The instance sends repeated requests to Telegram API to check for
new messages. View the template string for Telegram API requests below.

Template string for Telegram API requests

    https://api.telegram.org/bot{token}/getUpdates

Where `token` is the token you used to register the channel.

The **Creatio instance sends outgoing messages** directly to Telegram service
URLs.

View the interaction diagram of Creatio on-site and a Telegram channel in the
figure below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ChatChannels/8.1/scr_Telegram.png)

## Integrate a WhatsApp channel​

Before you start the integration, take the following steps:

1. **Make sure Creatio cloud services are available**.
2. **Sign up for Twilio**.
3. **Purchase a Twilio phone number** to send and receive messages.

Learn more:
[Set up WhatsApp integration](https://academy.creatio.com/documents?ver=8.0&id=2355)
(user documentation).

After the **Twilio phone number receives an incoming message** , Creatio cloud
services forward it to the Creatio client. If the Creatio instance is
unavailable, the services queue the message to resend it later.

The **Creatio instance sends outgoing messages** directly without using the
cloud services.

View the interaction diagram of Creatio on-site and a WhatsApp channel in the
figure below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/ChatChannels/8.1/scr_WhatsApp.png)

---

## See also​

[Set up chat processing](https://academy.creatio.com/documents?ver=8.0&id=2382)
(user documentation)

[Set up Facebook Messenger integration](https://academy.creatio.com/documents?ver=8.0&id=2384)
(user documentation)

[Set up Telegram integration](https://academy.creatio.com/documents?ver=8.0&id=2354)
(user documentation)

[Set up WhatsApp integration](https://academy.creatio.com/documents?ver=8.0&id=2355)
(user documentation)

---

## Resources​

[Long polling](https://en.wikipedia.org/w/index.php?title=Push_technology&oldid=1052758691#Long_polling)
(Wikipedia)

- Integrate a Facebook Messenger channel
- Integrate a Telegram channel
- Integrate a WhatsApp channel
- See also
- Resources
