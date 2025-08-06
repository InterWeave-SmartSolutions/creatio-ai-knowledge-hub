# Set up logging of incoming HTTP requests for .NET 6 | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 504 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/logging/logging-of-http-requests-net-core

## Description

You can set up logging of incoming HTTP requests in Creatio .NET 6.

## Key Concepts

configuration, detail

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/logging/logging-of-http-requests-net-core)**
(8.3).

Version: 8.1

On this page

Level: beginner

Important

You can set up logging of incoming HTTP requests in Creatio **.NET 6**.

Creatio lets you use the following logging **types** of incoming HTTP requests:

- standard logging
- extended logging

## Standard logging of incoming HTTP requests​

Standard logging lets you log incoming HTTP requests. The `Request.log` file in
the `Logs` directory of the Creatio root directory stores standard logs.

To **set up standard logging** :

1. Open the `appsettings.json` configuration file in the Creatio root directory.
2. Move to the `Standard` block. Standard logging is enabled by default (the
   `Enabled` flag is set to `true`).
3. Add HTTP response codes into the `StatusCodes` flag. Creatio will log the
   requests that receive the specified response codes. If you turn on the
   `Enabled` flag and leave the `StatusCodes` flag empty, Creatio logs all
   incoming HTTP requests.

Example that configures standard logging (appsettings.json file)

    "RequestLogging": {
        "Standard": {
            "Enabled": true,
            "StatusCodes": [ 200, 300, 302 ]
        },
        ...
    }


You can analyze the logs using the Log Parser Studio utility because the log
format is similar to the IIS log format.

## Extended logging for incoming HTTP requests​

Extended logging lets you retrieve detailed information about logs for incoming
HTTP requests. The `ExtendedRequest.log` file in the `Logs` directory of the
Creatio root directory stores extended logs. Creatio saves data about the
response body of an incoming HTTP request automatically when extended logging is
turned on.

To **set up extended logging** :

1. Open the `appsettings.json` configuration file in the Creatio root directory.

2. Move to the `Extended` block. Extended logging is turned off by default (the
   `Enabled` flag is set to `false`).

3. Set the `Enabled` flag to `true` to turn on logging.

4. If you want to retrieve information about the HTTP request body in the log,
   set the `LogRequestBody` flag to `true` (`false` by default).

5. Set the size of the displayed request/response body (the first N bytes) in
   the `MaxBodySizeBytes` flag.

Important

Extended logging affects performance if Creatio receives a large number of
requests or you set a large value of the `MaxBodySizeBytes` flag.

6. Add HTTP response codes into the `StatusCodes` flag. Creatio will log the
   requests that receive the specified response codes. If you turn on the
   `Enabled` flag and leave the `StatusCodes` flag empty, Creatio logs all
   incoming HTTP requests.

Example that configures extended logging (appsettings.json file)

    "RequestLogging": {
        ...,
        "Extended": {
            "Enabled": true,
            "LogRequestBody": false,
            "MaxBodySizeBytes": 500,
            "StatusCodes": [ 400, 401, 403 ]
        }
    }

You can use standard and extended logging simultaneously with different values
of the `StatusCodes` flag. If the `StatusCodes` flag values for standard and
extended logging match, Creatio duplicates the logs for incoming HTTP requests
in the `Request.log` and `ExtendedRequest.log` files with different details.

- Standard logging of incoming HTTP requests
- Extended logging for incoming HTTP requests
