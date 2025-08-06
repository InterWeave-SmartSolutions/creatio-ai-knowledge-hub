# Close the WebSocket when destroying the View of the model | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 313
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/close-the-websocket

## Description

To close the WebSocket when destroying the View of the model, add a custom
implementation of the crt.HandleViewModelDestroyRequest system query handler to
the handlers schema section. The handler is executed when the View of the model
is destroyed (for example, when you open another page). Designed to destroy
resources. We do not recommend writing asynchronous code in the handler (server
calls, timeouts, etc.) except for reading the value of attributes.

## Key Concepts

freedom ui, section

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/close-the-websocket)**
(8.3).

Version: 8.0

Level: intermediate

To **close the WebSocket when destroying** the `View` of the **model** , add a
custom implementation of the `crt.HandleViewModelDestroyRequest` system query
handler to the `handlers` schema section. The handler is executed when the
`View` of the model is destroyed (for example, when you open another page).
Designed to destroy resources. We do not recommend writing asynchronous code in
the handler (server calls, timeouts, etc.) except for reading the value of
attributes.

View an example of the `crt.HandleViewModelDestroyRequest` query handler that
closes the custom `SomeWebSocket` WebSocket below.

For Creatio version 8.0.6 and later

Freedom UI cannot destroy a `View` model and loads the last page state when you
re-open a previously loaded module. Since version 8.0.6, use the
`crt.HandleViewModelPauseRequest` handler called every time you open a different
page. The `crt.HandleViewModelDestroyRequest` and
`crt.HandleViewModelPauseRequest` handlers use the same data.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandleViewModelPauseRequest",
            /* Custom implementation of a system query handler. */
            handler: async (request, next) => {
                /* Close the SomeWebSocket WebSocket */
                (await request.$context.SomeWebSocket).close();
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        }
    ]/**SCHEMA_HANDLERS*/,

For Creatio version 8.0-8.0.5

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandleViewModelDestroyRequest",
            /* Custom implementation of a system query handler. */
            handler: async (request, next) => {
                /* Close the SomeWebSocket WebSocket */
                (await request.$context.SomeWebSocket).close();
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        }
    ]/**SCHEMA_HANDLERS*/,
