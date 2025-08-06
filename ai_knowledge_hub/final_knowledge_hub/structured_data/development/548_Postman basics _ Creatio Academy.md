# Postman basics | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 175 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/integrations-and-api/using-postman/overview

## Description

Postman is a toolset for API testing. It is a development environment that lets
you create, test, manage, and publish API documentation.

## Key Concepts

integration, odata

## Use Cases

building applications, custom development, API integration, third-party
integration, data synchronization

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/using-postman/overview)**
(8.3).

Version: 8.1

Level: intermediate

**Postman** is a toolset for API testing. It is a development environment that
lets you create, test, manage, and publish API documentation.

Working with requests in Postman consists of the following general stages:

- Adding a request
- Setting up the request
- Executing the request
- Saving the request

A collection of requests lets you execute several requests consecutively. Any
collection of requests to Creatio must include a `POST` request to
[`AuthService.svc`](https://academy.creatio.com/documents?ver=8.1&id=15404) and
a user request for working with data. Using collections facilitates faster
testing of large sets of requests.

Working with collections of requests in Postman consists of the following
general stages:

- Adding a collection of requests
- Adding requests to the collection
- Setting up variables for the request collection
- Executing the collection of requests

We recommend using Postman for testing queries when developing integrations with
Creatio via
[OData 3](https://academy.creatio.com/documents?ver=8.1&id=15431&anchor=title-1398-2)
or
[OData 4](https://academy.creatio.com/documents?ver=8.1&id=15431&anchor=title-1398-1).
More information about working with Postman is available in the
[Postman documentation](https://learning.postman.com/docs/postman/launching-postman/introduction/).
