# Handle the response of an external web service | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 416 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/freedom-ui/web-service

## Description

@creatio-devkit/common includes the sdk.HttpClientService service that sends
HTTP requests.

## Key Concepts

freedom ui, section, web service, case, customization

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

`@creatio-devkit/common` includes the `sdk.HttpClientService` service that sends
HTTP requests.

To handle the response of an external web service:

1. **Add the dependencies**. Instructions:
   [Display the value of a system variable](https://academy.creatio.com/documents?ver=8.0&id=15380&anchor=amd-dependencies)
   (similarly to step 2). Instead of the `sdk.SysValuesService` service, use the
   `sdk.HttpClientService` service that sends HTTP requests.

2. **Add an attribute**. Instructions:
   [Set up the field display condition](https://academy.creatio.com/documents?ver=8.0&id=15379&anchor=viewModelConfig)
   (step 2).

3. **Bind an attribute to the label**. Instructions:
   [Set up the field display condition](https://academy.creatio.com/documents?ver=8.0&id=15379&anchor=viewConfigDiff)
   (similarly to step 3). Instead of the `visible` property, use the `caption`
   property that handles the text displayed in the element.

4. **Implement the base request handler**.
   1. Go to the `handlers` schema section.

   2. Add a custom implementation of the `crt.HandlerViewModelInitRequest` base
      request handler.
      1. Create an instance of the HTTP client from `@creatio-devkit/common`.
      2. Specify the URL to retrieve required data. If a web service request is
         sent using a non-absolute path (without `https://` or `http://`
         prefixes), this is a request to an internal Creatio web service. In
         this case, Creatio automatically adds the address of the current app to
         the link.
      3. Send a `GET` request.
      4. Retrieve required data from the response and specify data in the
         corresponding attribute.

View an example of a `crt.HandleViewModelInitRequest` request handler that sends
a request to the `https://SomeUrl` web service, receives the `someValue`
parameter from the response body, and specifies the parameter in the
`SomeAttribute` attribute, below.

handlers schema section

    handlers: /**SCHEMA_HANDLERS*/[
        {
            request: "crt.HandleViewModelInitRequest",
            /* Custom implementation of a system request handler. */
            handler: async (request, next) => {
                /* Create an instance of the HTTP client from "@creatio-devkit/common." */
                const httpClientService = new sdk.HttpClientService();
                /* Specify the URL to retrieve required data. */
                const endpoint = "https://SomeUrl";
                /* Send a GET request. The HTTP client converts the response body from JSON to a JS object automatically. */
                const response = await httpClientService.get(endpoint);
                /* Retrieve the "someValue" parameter from the response body and specify it in the "SomeAttribute" attribute. */
                request.$context.SomeAttribute = response.body.someValue;
                /* Call the next handler if it exists and return its result. */
                return next?.handle(request);
            }
        }
    ]/**SCHEMA_HANDLERS*/,

---

## See also​

[Freedom UI page customization basics](https://academy.creatio.com/documents?ver=8.0&id=15370)

[Customize fields (Freedom UI)](https://academy.creatio.com/documents?ver=8.0&id=15379)

- See also
