# Implement a custom web service | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1925
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/back-end-development/web-services/web-service-implementation/custom-web-service

## Description

A web service is software reachable via a unique URL, which enables interaction
between applications. The purpose of a web service is to integrate Creatio with
external applications and systems.

## Key Concepts

business process, configuration, section, integration, web service, odata,
database, operation, no-code, automation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/back-end-development/web-services/web-service-implementation/custom-web-service)**
(8.3).

Version: 8.2

On this page

Level: intermediate

A **web service** is software reachable via a unique URL, which enables
interaction between applications. The **purpose** of a web service is to
integrate Creatio with external applications and systems.

Based on the custom business logic, Creatio generates and sends a request to the
web service, receives the response, and extracts the needed data. Use this data
to create or update records in the Creatio database as well as for custom
business logic or automation.

Creatio supports the following web service types:

- **External REST and SOAP services** that you can integrate with no-code tools.
  Learn more in the user documentation guide:
  [Web services](https://academy.creatio.com/docs/8.x/no-code-customization/category/web-services).

- **System web services**.
  - System web services that use cookie-based authentication.
  - System web services that use anonymous authentication.

- **Custom web services**.
  - Custom web services that use cookie-based authentication.
  - Custom web services that use anonymous authentication.

.NET Framework system web services use the
[WCF](https://docs.microsoft.com/en-us/dotnet/framework/wcf/) technology and are
managed at the IIS level. .NET system web services use the
[ASP.NET Core Web API](https://docs.microsoft.com/en-us/aspnet/core/web-api/?view=aspnetcore-5.0)
technology.

Learn more about the authentication types Creatio provides for web services:
[Authentication](https://academy.creatio.com/documents?ver=8.2&id=15402). We
recommend using authentication based on the OAuth 2.0 open authorization
protocol. Learn more about OAuth-based authentication:
[Set up OAuth 2.0 authorization for integrated applications](https://academy.creatio.com/documents?ver=8.2&id=2396)
(user documentation).

Creatio **system web services that use cookie-based authentication** include:

- `odata` that executes OData 4 external application requests to the Creatio
  database server. Learn more about using the OData 4 protocol in Creatio:
  [OData](https://academy.creatio.com/documents?ver=8.2&id=15431&anchor=title-1398-1).
- `EntityDataService.svc` that executes OData 3 external application requests to
  the Creatio database server. Learn more about using the OData 3 protocol in
  Creatio:
  [OData](https://academy.creatio.com/documents?ver=8.2&id=15431&anchor=title-1398-2).
- `ProcessEngineService.svc` that enables external applications to run Creatio
  business processes. Learn more about the web service:
  [Service that runs business processes](https://academy.creatio.com/documents?ver=8.2&id=15441).

Creatio **services that use anonymous authentication** include `AuthService.svc`
that executes Creatio authentication requests. Learn more about the web service:
[Authentication](https://academy.creatio.com/documents?ver=8.2&id=15402).

This article covers custom web services. Learn more about system web services:
[Integrations tools](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/integrations-tools).

## Develop a custom web service​

A **custom web service** is a RESTful service that uses the WCF (for .NET
Framework) or ASP .NET Core (for .NET) technology. Unlike system web services,
custom web services let you solve unique integration problems.

The web service development procedure differs for each Creatio deployment
framework. View the unique features of the custom web service development for
the .NET Framework and .NET below.

You can use Postman to test querying a custom web service. Learn more about
Postman: [official vendor documentation](https://www.postman.com/) (Postman).
Learn more about querying Creatio using Postman:
[Working with requests in Postman](https://academy.creatio.com/documents?ver=8.2&id=15452).
Learn more about calling a web service via Postman:
[Call a custom web service from Postman](https://academy.creatio.com/documents?ver=8.2&id=15266).

### Develop a custom web service that uses cookie-based authentication​

1. Create a **Source code** schema. Learn more about creating a schema:
   [Source code (C#)](https://academy.creatio.com/documents?ver=8.2&id=15108&anchor=title-2123-8).

2. Create a **service class**.
   1. Add the `Terrasoft.Configuration` namespace or any of its nested
      namespaces in the Schema Designer. Name the namespace arbitrarily.
   2. Add the namespaces the data types of which to utilize in the class using
      the `using` directive.
   3. Use the `Terrasoft.Web.Http.Abstractions` namespace if you want the custom
      web service to support both .NET Framework and .NET. If you develop the
      web service using the `System.Web` namespace and have to run it on .NET,
      [adapt the web service](https://academy.creatio.com/documents?ver=8.2&id=15262&anchor=title-1243-7).
   4. Add the class name that matches the schema name (the **Code** property).
   5. Specify the `Terrasoft.Nui.ServiceModel.WebService.BaseService` class as a
      parent class.
   6. Add the `[ServiceContract]` and `[AspNetCompatibilityRequirement]` class
      attributes that contain the needed parameters. Learn more about the
      `[ServiceContract]` attribute:
      [official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.servicecontractattribute?view=dotnet-plat-ext-5.0)
      (Microsoft). Learn more about the `[AspNetCompatibilityRequirements]`
      attribute:
      [official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.activation.aspnetcompatibilityrequirementsattribute?view=netframework-4.8)
      (Microsoft).

3. Implement the **class methods** that correspond to the web service endpoints.

Add the `[OperationContract]` and `[WebInvoke]` method attributes that contain
the needed parameters. Learn more about the `[OperationContract]` attribute:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.operationcontractattribute?view=dotnet-plat-ext-5.0)
(Microsoft). Learn more about the `[WebInvoke]` attribute:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.web.webinvokeattribute?view=netframework-4.8)
(Microsoft).

4. Implement **additional classes** whose instances receive or return the web
   service methods (optional). Required to pass data of complex types. For
   example, object instances, collections, arrays, etc.

Add the `[DataContract]` attribute to the class and the `[DataMember]` attribute
to the class fields. Learn more about the `[DataContract]` attribute:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.serialization.datacontractattribute?view=net-5.0)
(Microsoft). Learn more about the `[DataMember]` attribute:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.serialization.datamemberattribute?view=net-5.0)
(Microsoft).

5. **Publish the schema**.

As a result, you will be able to call the custom web service that uses
cookie-based authentication from the source code of configuration schemas as
well as from external applications.

### Develop a custom web service that uses anonymous authentication​

A **custom web service that uses anonymous authentication** does not require the
user to pre-authenticate, i. e., you can use the service anonymously.

Important

We do not recommend using anonymous authentication in custom web services. It is
insecure and can hurt performance.

#### Develop a custom web service that uses anonymous authentication for .NET Framework​

1. Take steps 1-5 in the
   [Develop a custom web service that uses cookie-based authentication](https://academy.creatio.com/documents?ver=8.2&id=15262&anchor=title-2148-2)
   instruction.

2. Add the `SystemUserConnection` system connection when creating a service
   class.

3. Specify the user on whose behalf to process the HTTP request when creating a
   class method. To do this, call the
   `SessionHelper.SpecifyWebOperationIdentity` method of the
   `Terrasoft.Web.Common` namespace after retrieving `SystemUserConnection`.
   This method enables business processes to manage the database entity
   (`Entity`) from the custom web service that uses anonymous authentication.

   Terrasoft.Web.Common.SessionHelper.SpecifyWebOperationIdentity(  
    HttpContextAccessor.GetInstance(),  
    SystemUserConnection.CurrentUser  
    );

4. Register the **custom web service that uses anonymous authentication**.
   1. Create an \*.svc file in the `..\Terrasoft.WebApp\ServiceModel` directory.
      The file name must match the web service name.

   2. Add the following record to the file.
      - Template that registers the custom web service that uses anonymous
        authentication
      - Example that registers the custom web service that uses anonymous
        authentication


    <% @ServiceHost
        Service = "Service, ServiceNamespace"
        Factory = "Factory, FactoryNamespace"
        Debug = "Debug"
        Language = "Language"
        CodeBehind = "CodeBehind"
    %>


    <% @ServiceHost
        Service = "Terrasoft.Configuration.UsrAnonymousConfigurationServiceNamespace.UsrAnonymousConfigurationService"
        Debug = "true"
        Language = "C#"
    %>

The `Service` attribute contains the full name of the web service class and
specifies the namespace.

Learn more about the `@ServiceHost` WCF directive:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/wcf-directive/servicehost)
(Microsoft).

     3. Save the file.

5. Register a **non-standard text encoding** (optional).

Creatio lets you use arbitrary character encodings in .NET Framework web
services that use anonymous authentication. For example, you can use such
encodings as ISO-8859, ISO-2022, etc. Learn more about encodings:
[Character encoding](https://en.wikipedia.org/wiki/Character_encoding)
(Wikipedia).

To **register an arbitrary character encoding** :

     1. Add a `<customBinding>` section to the `..\Terrasoft.WebApp\ServiceModel\http\bindings.config` file.

     2. Add the following **attributes** to the `<customBinding>` file section:

        * `name` attribute of the `<binding>` element. Fill it with a custom name of the encoding.
        * `encoding` attribute of the `<customTextMessageEncoding>` element. Fill it with the code of the encoding, for example, ISO-8859-1.
        * `manualAddressing` attribute of the `<httpTransport>` element. Set it to `true`.

Example of changes to the ..\Terrasoft.WebApp\ServiceModel\http\bindings.config
file

    <bindings>
        ...
        <customBinding>
            <binding name="CustomEncodingName">
                <customTextMessageEncoding encoding="ISO-8859-1" />
                <httpTransport manualAddressing="true"/>
            </binding>
            ...
        </customBinding>
    </bindings>


Register each encoding (i. e., add `<binding>` file section for each)
individually.

     3. Save the file.

     4. Add an identical record to the `..\Terrasoft.WebApp\ServiceModel\https\bindings.config` file.

6. Enable both **HTTP and HTTPS support** for the custom web service that uses
   anonymous authentication.
   1. Add the following record to the
      `..\Terrasoft.WebApp\ServiceModel\http\services.config` file.

Example of changes to the ..\Terrasoft.WebApp\ServiceModel\http\services.config
file

            <services>
                ...
                <service name="Terrasoft.Configuration.SomeCustomNamespace.SomeServiceName">
                    <endpoint name="SomeServiceNameEndPoint"
                    address=""
                    binding="SomeBinding"
                    bindingConfiguration="SomeCustomEncoding"
                    behaviorConfiguration="RestServiceBehavior"
                    bindingNamespace="http://Terrasoft.WebApp.ServiceModel"
                    contract="Terrasoft.Configuration.SomeCustomNamespace.SomeServiceName" />
                </service>
            </services>



The `<services>` element contains the list of Creatio web service configurations
(the `<service>` nested elements).

The `name` attribute contains the name of the type (class or interface) that
implements the web service contract.

The `<endpoint>` nested element contains the address, binding, and interface
that defines the contract of the web service specified in the `name` attribute
of the `<service>` element.

The `binding` attribute contains the value of the character encoding. Must match
the name of the file section where the encoding that the web service uses is
registered. Set to "webHttpBinding" to use the UTF-8 encoding. Set to
"customBinding" to use a custom encoding.

The `bindingConfiguration` attribute. Must be present if the `binding` attribute
is set to "customBinding." The value of the current attribute must match the
value of the `<binding>` element’s `name` attribute specified on the previous
step.

Learn more about the web service configuration elements:
[official vendor documentation](https://docs.microsoft.com/en-us/dotnet/framework/wcf/configuring-services-using-configuration-files)
(Microsoft).

     2. Save the file.

     3. Add an identical record to the `..\Terrasoft.WebApp\ServiceModel\https\services.config` file.

7. Enable all users to **access the custom web service** that uses anonymous
   authentication.
   1. Add the `<location>` element that defines the relative path and access
      permissions to the web service to the `..\Terrasoft.WebApp\Web.config`
      file.

Example of changes to the ..\Terrasoft.WebApp\Web.config file

            <configuration>
                ...
                <location path="ServiceModel/SomeServiceName.svc">
                    <system.web>
                        <authorization>
                            <allow users="*" />
                        </authorization>
                    </system.web>
                </location>
                ...
            </configuration>



     2. Add the relative web service path to the `value` attribute of the `<appSettings>` element's `AllowedLocations` key in the `..\Terrasoft.WebApp\Web.config` file.

Example of changes to the ..\Terrasoft.WebApp\Web.config file

            <configuration>
                ...
                <appSettings>
                    ...
                    <add key="AllowedLocations" value="SomePreviousValues;ServiceModel/SomeServiceName.svc" />
                    ...
                </appSettings>
                ...
            </configuration>



     3. Save the file.

8. Restart Creatio in IIS.

As a result, you will be able to call the custom web service that uses anonymous
authentication from the source code of configuration schemas as well as from
external applications. You can access the web service both with and without
pre-authentication.

#### Develop a custom web service that uses anonymous authentication for .NET​

1. Take steps 1-5 in the
   [Develop a custom web service that uses cookie-based authentication](https://academy.creatio.com/documents?ver=8.2&id=15262&anchor=title-2148-5)
   instruction.

2. Enable all users to **access the custom web service** that uses anonymous
   authentication.

To do this, add the web service data to the `AnonymousRoutes` block of the
`..\Terrasoft.WebHost\appsettings.json` configuration file.

Example of changes to the ..\Terrasoft.WebHost\appsettings.json file

         "Terrasoft.Configuration.SomeServiceName": [
             "/ServiceModel/SomeServiceName.svc"
         ]


3. Restart Creatio.

As a result, you will be able to call the custom web service that uses anonymous
authentication from the source code of configuration schemas as well as from
external applications. You can access the web service both with and without
pre-authentication.

Important

Reconfigure the web service after updating Creatio. The existing configuration
files are overwritten as part of the update.

---

## See also​

[Authentication](https://academy.creatio.com/documents?ver=8.2&id=15402)

[OData](https://academy.creatio.com/documents?ver=8.2&id=15431)

[Service that runs business processes](https://academy.creatio.com/documents?ver=8.2&id=15441)

[Source code (C#)](https://academy.creatio.com/documents?ver=8.2&id=15108)

---

## Resources​

[Web services](https://academy.creatio.com/docs/8.x/no-code-customization/category/web-services)

[Integrations tools](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/integrations-tools)

[Official Microsoft documentation (description of the WCF technology) ](https://docs.microsoft.com/en-us/dotnet/framework/wcf/)

[Official Microsoft documentation (description of the ASP.NET Core Web API technology) ](https://docs.microsoft.com/en-us/aspnet/core/web-api/?view=aspnetcore-5.0)

[Official Microsoft documentation (description of the [ServiceContract] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.servicecontractattribute?view=dotnet-plat-ext-5.0)

[Official Microsoft documentation (description of the [AspNetCompatibilityRequirements] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.activation.aspnetcompatibilityrequirementsattribute?view=netframework-4.8)

[Official Microsoft documentation (description of the [OperationContract] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.operationcontractattribute?view=dotnet-plat-ext-5.0)

[Official Microsoft documentation (description of the [WebInvoke] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.servicemodel.web.webinvokeattribute?view=netframework-4.8)

[Official Microsoft documentation (description of the [DataContract] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.serialization.datacontractattribute?view=net-5.0)

[Official Microsoft documentation (description of the [DataMember] attribute) ](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.serialization.datamemberattribute?view=net-5.0)

[Official Microsoft documentation (description of the @ServiceHost WCF directive) ](https://docs.microsoft.com/en-us/dotnet/framework/configure-apps/file-schema/wcf-directive/servicehost)

[Official Microsoft documentation (description of the service configuration elements)](https://docs.microsoft.com/en-us/dotnet/framework/wcf/configuring-services-using-configuration-files)

[Concept of encoding](https://en.wikipedia.org/w/index.php?title=Character_encoding&oldid=1089398335)

[Official Postman documentation](https://www.postman.com/)

- Develop a custom web service
  - Develop a custom web service that uses cookie-based authentication
  - Develop a custom web service that uses anonymous authentication
- See also
- Resources
