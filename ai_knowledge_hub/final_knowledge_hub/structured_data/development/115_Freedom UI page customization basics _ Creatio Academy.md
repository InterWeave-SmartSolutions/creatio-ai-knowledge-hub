# Freedom UI page customization basics | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 604 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/page-customization-basics/overview

## Description

Configure the business logic of Freedom UI pages in the validators, converters,
and handlers schema sections. We recommend using no-code tools to set up
business logic. Learn more: Overview of Freedom UI Designer and its elements
(user documentation).

## Key Concepts

page schema, configuration, freedom ui, section, web service, no-code,
customization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/page-customization-basics/overview)**
(8.3).

Version: 8.0

On this page

Level: beginner

Configure the business logic of Freedom UI pages in the `validators`,
`converters`, and `handlers` schema sections. We recommend using **no-code
tools** to set up business logic. Learn more:
[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?ver=8.0&id=2376)
(user documentation).

If no-code tools are not sufficient to implement your customization, we
recommend setting up business logic in the source code of the Freedom UI page
schema. Learn more:
[Freedom UI page schema](https://academy.creatio.com/documents?ver=8.0&id=15106&anchor=title-2123-10),
[Structure of a Freedom UI page](https://academy.creatio.com/documents?ver=8.0&id=15346).

For example, you can implement the following **business logic** of a Freedom UI
page:

- condition that displays the element
- condition that locks the element
- condition that populates the element
- condition that makes element required
- validate the element data
- convert the element data
- element filtering
- Creatio data requesting
- handle the result of a web service
- page navigation

## General procedure to customize Freedom UI page​

1. **Set up the page UI**.
   1. Create an app based on the corresponding template. Instructions:
      [Create an app manually](https://academy.creatio.com/documents?ver=8.0&id=2377&anchor=title-2232-6)
      (user documentation).
   2. Add one or more elements whose business logic to set up. Instructions:
      [Set up the app UI](https://academy.creatio.com/documents?ver=8.0&id=2379)
      (user documentation).

2. **Set up the page business logic**.

Configure the business logic in the Client Module Designer.

     1. Open the source code of the Freedom UI page. To do this, click ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/ClientModule/8.0/scr_SourceCode_button.png).
     2. Perform the setup in the corresponding schema sections of the Freedom UI page schema. Learn more: [Client schema (Freedom UI)](https://academy.creatio.com/documents?ver=8.0&id=15342).

**Request handlers** are the preferred way to customize the page. Request
handlers are items of the `HandlerChain` mechanism that lets you describe
business logic as an action request and chain of handlers. You can manage data
sources using the `handlers` schema section. Learn more:
[handlers schema section](https://academy.creatio.com/documents?ver=8.0&id=15368).

Creatio lets you organize request handlers in event chains. For example, trigger
the base Creatio save handler first and execute the custom page logic later upon
the page saver request.

To **limit the scope of a request handler** , fill out the `scopes` property of
the client module with the names of the client schemas for which the handler
must work.

## Close the WebSocket when destroying the View of the model​

To close the WebSocket when destroying the `View` of the model:

1. **Go to the** `handlers` **schema section**.

2. **Add a custom implementation of the** `crt.HandleViewModelDestroyRequest`
   **base request handler**.

Creatio executes the handler when the `View` of the model is destroyed (for
example, when you open another page). Designed to destroy resources. We do not
recommend writing asynchronous code in the handler (server calls, timeouts,
etc.) except for reading the value of attributes.

View an example of the `crt.HandleViewModelDestroyRequest` request handler that
closes the custom `SomeWebSocket` WebSocket below.

handlers schema section

         handlers: /**SCHEMA_HANDLERS*/[
             {
                 request: "crt.HandleViewModelDestroyRequest",
                 /* The custom implementation of the system request handler. */
                 handler: async (request, next) => {
                     /* Close the "SomeWebSocket" WebSocket */
                     (await request.$context.SomeWebSocket).close();
                     /* Call the next handler if it exists and return its result. */
                     return next?.handle(request);
                 }
             }
         ]/**SCHEMA_HANDLERS*/,


---

## See also​

[Overview of Freedom UI Designer and its elements](https://academy.creatio.com/documents?ver=8.0&id=2376)
(user documentation)

[Configuration elements of the Client module type](https://academy.creatio.com/documents?ver=8.0&id=15106)

[Structure of a Freedom UI page](https://academy.creatio.com/documents?ver=8.0&id=15346)

[Manage apps](https://academy.creatio.com/documents?ver=8.0&id=2377) (user
documentation)

[Set up the app UI](https://academy.creatio.com/documents?ver=8.0&id=2379) (user
documentation)

[Client schema (Freedom UI)](https://academy.creatio.com/documents?ver=8.0&id=15342)

- General procedure to customize Freedom UI page
- Close the WebSocket when destroying the View of the model
- See also
