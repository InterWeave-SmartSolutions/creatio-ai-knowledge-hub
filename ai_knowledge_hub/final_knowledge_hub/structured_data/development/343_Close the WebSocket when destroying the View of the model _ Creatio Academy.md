# Close the WebSocket when destroying the View of the model | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 207
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/platform-customization/freedom-ui/close-the-websocket

## Description

To close the WebSocket when destroying the View of the model, add a custom
implementation of the crt.HandleViewModelDestroyRequest system request handler
to the handlers schema section. The handler is executed when the View of the
model is destroyed (for example, when you open another page). Designed to
destroy resources. We do not recommend writing asynchronous code in the handler
(server calls, timeouts, etc.) except for reading the value of attributes.

## Key Concepts

freedom ui, section

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

Level: intermediate

To **close the WebSocket when destroying** the `View` of the **model** , add a
custom implementation of the `crt.HandleViewModelDestroyRequest` system request
handler to the `handlers` schema section. The handler is executed when the
`View` of the model is destroyed (for example, when you open another page).
Designed to destroy resources. We do not recommend writing asynchronous code in
the handler (server calls, timeouts, etc.) except for reading the value of
attributes.

View an example of the `crt.HandleViewModelDestroyRequest` request handler that
closes the custom `SomeWebSocket` WebSocket below.

Freedom UI cannot destroy a `View` model and loads the last page state when you
re-open a previously loaded module. Use the `crt.HandleViewModelPauseRequest`
handler called every time you open a different page. The
`crt.HandleViewModelDestroyRequest` and `crt.HandleViewModelPauseRequest`
handlers use the same data.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandleViewModelPauseRequest",
            /* Custom implementation of a system request handler. */
            handler: async (request, next) => {
                /* Close the SomeWebSocket WebSocket */
                (await request.$context.SomeWebSocket).close();
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        }
    ]/**SCHEMA_HANDLERS*/,
