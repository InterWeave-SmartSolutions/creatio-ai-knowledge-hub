# Migrate an existing custom web service to .NET | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 459
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/back-end-development/web-services/migrating

## Description

You can migrate a .NET Framework custom web service that retrieves the scope
without inheriting the Terrasoft.Web.Common.BaseService base class to .NET. To
do this, adapt the custom web service.

## Key Concepts

configuration, web service, operation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/web-services/migrating)**
(8.3).

Version: 8.2

Level: intermediate

You can migrate a .NET Framework custom web service that retrieves the scope
without inheriting the `Terrasoft.Web.Common.BaseService` base class to .NET. To
do this, **adapt the custom web service**.

The `HttpContextAccessor` property of the `Terrasoft.Web.Common.BaseService`
provides unified access to context (`HttpContext`) both in .NET Framework and
.NET. The `UserConnection` and `AppConnection` properties let you retrieve the
user connection object and the connection object on the application level. This
lets you omit the `HttpContext.Current` property of the `System.Web` library.

Example that uses the properties of the Terrasoft.Web.Common.BaseService parent
class

    namespace Terrasoft.Configuration.UsrCustomNamespace {
        using Terrasoft.Web.Common;

        [ServiceContract]
        [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
        public class UsrCustomConfigurationService: BaseService {
            /* The web service method. */
            [OperationContract]
            [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, BodyStyle = WebMessageBodyStyle.Wrapped,
                ResponseFormat = WebMessageFormat.Json)]
            public void SomeMethod() {
                ...
                /* UserConnection is the BaseService property. */
                var currentUser = UserConnection.CurrentUser;
                /* AppConnection is the BaseService property. */
                var sdkHelpUrl = AppConnection.SdkHelpUrl;
                /* HttpContextAccessor is the BaseService property. */
                var httpContext = HttpContextAccessor.GetInstance();
                ...
            }
        }

    }


Creatio supports the following **scope retrieval options** for web services
developed without inheriting the `Terrasoft.Web.Common.BaseService` class:

- via the `IHttpContextAccessor` **interface** registered in `DI`
  (`ClassFactory`).

This option lets you view the explicit class dependencies for thorough automated
testing and debugging. Learn more about using the class factory:
[Replacing class factory](https://academy.creatio.com/documents?ver=8.2&id=15221).

- via the `HttpContext.Current` **static property**.

Add the `Terrasoft.Web.Http.Abstractions` namespace to the source code using the
`using` directive. The `HttpContext.Current` static property implements unified
access to `HttpContext`. To adapt the web service code to .NET, replace the
`System.Web` namespace using `Terrasoft.Web.Http.Abstractions`.

Important

Do not use specific access implementations to request context peculiar to .NET
Framework (the `System.Web` library) or .NET (the `Microsoft.AspNetCore.Http`
namespace) in the configuration.

Example that adapts the web service to .NET

    namespace Terrasoft.Configuration.UsrCustomNamespace {
        /* Use instead of System.Web. */
        using Terrasoft.Web.Http.Abstractions;

        [ServiceContract]
        [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Required)]
        public class UsrCustomConfigurationService {
            /* The web service method. */
            [OperationContract]
            [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, BodyStyle = WebMessageBodyStyle.Wrapped,
                ResponseFormat = WebMessageFormat.Json)]
            public void SomeMethod() {
                ...
                var httpContext = HttpContext.Current;
                ...
            }
        }
    }
