# Integration options | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 765
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/overview

## Description

You can integrate Creatio with a wide range of external apps.

## Key Concepts

business process, configuration, integration, web service, odata, rest api,
database, operation, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

You can integrate Creatio with a wide range of external apps.

The choice of the integration option depends on the following **factors** :

- customer needs
- external app type and architecture
- developer expertise level

View the main integration options in the figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Integrations/8.0/scr_IntegrationWithCreatio_en.png)

View the comparison of the major features of Creatio integration options in the
table below.

| Feature | Integration option | DataService | OData | `ProcessEngineService.svc` | Custom web service | Authentication options | Forms | Forms | Forms | Anonymous, Forms | Problems solved | Execute CRUD operations with Creatio objects, filter data, and use built-in Creatio macros | Execute CRUD operations with Creatio objects, add and delete bindings, retrieve properties, collections, object fields, sort data, etc. | Run business processes, transfer and receive parameters of the launched process, run individual process elements | Solve arbitrary problems within the capabilities of Creatio's open API | Data exchange formats | XML, JSON, JSV, CSV | XML, JSON | XML, JSON | XML, JSON | Developer | Creatio | Microsoft | Creatio | Creatio | Client libraries | You can use Creatio \*.dll libraries only for .NET apps | Learn more about the libraries: [official vendor documentation](http://www.odata.org/libraries) (OData) | No need | No need | Complexity | High | Medium | Low | Medium |
| ------- | ------------------ | ----------- | ----- | -------------------------- | ------------------ | ---------------------- | ----- | ----- | ----- | ---------------- | --------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------- | ------------------- | --------- | --------- | --------- | --------- | ------- | --------- | ------- | ------- | ---------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---- | ------ | --- | ------ |

## Data services​

Creatio lets you use the following **data services** :

- OData protocol
- DataService service

### DataService service​

**DataService** (developed by Creatio) is a service that enables communication
between Creatio front-end and back-end. DataService lets you transfer user data
to Creatio back-end to be processed and saved to a database. Learn more:
[DataService](https://academy.creatio.com/documents?ver=8.3&id=15411).

Besides executing CRUD operations, DataService lets you use
[built-in macros](https://academy.creatio.com/documents?ver=8.3&id=15415) and
[filters](https://academy.creatio.com/documents?ver=8.3&id=15411). You can
execute complex
[batch requests](https://academy.creatio.com/documents?ver=8.3&id=15419).

### OData protocol​

**OData (Open Data Protocol)** is an ISO/IEC-approved OASIS standard. It defines
a set of best practices for building and using REST API. Any external app that
supports the HTTP protocol messaging and can handle data in the `XML` or `JSON`
format can access Creatio data and objects using the OData protocol. In this
case, data is available as resources identified using a URL. To interact with
data, use the standard `GET`, `PUT`/`PATCH`, `POST` and `DELETE` HTTP methods.
Learn more about the protocol:
[official vendor documentation](https://www.odata.org/getting-started/) (OData).

Besides executing CRUD operations, the OData protocol lets you use the string,
date, and time functions. Also, the protocol lets you extend its functionality
using a large number of client libraries developed for widespread apps.

Creatio supports OData 4 and OData 3 protocols. OData 4 has more features than
OData 3. The main **difference** between the protocols is the data format of the
server's response. Learn more about the differences between OData 3 and OData 4
protocols:
[official vendor documentation](http://docs.oasis-open.org/odata/new-in-odata/v4.01/new-in-odata-v4.01.html)
(OData). Use the protocol version 4 when you integrate an external app with
Creatio via the OData protocol.

## Service that runs business processes​

Use the `ProcessEngineService.svc` system web service to run business processes
from an external app. Besides running business processes from an external app,
the `ProcessEngineService.svc` service lets you exchange data between Creatio
and external apps. Learn more:
[Service that runs business processes](https://academy.creatio.com/documents?ver=8.3&id=15441).

## Custom web service​

You can create **custom web services** to solve certain integration problems.
The configuration web service is a RESTful service based on
[WCF](https://docs.microsoft.com/en-us/dotnet/framework/wcf/?redirectedfrom=MSDN)
technology. Learn more:
[Custom web services](https://academy.creatio.com/documents?ver=8.3&id=15262).

A custom web service lets you perform a data exchange implemented by the
developer. The web service also lets you implement any operations with Creatio
objects, including CRUD operations.

Users can access such services without authorization.

## Recommendations for integrating external apps with Creatio​

We recommend using multithreaded integration to maximize Creatio throughput. The
exact recommendations depend on the session mode that Creatio protocol or
service uses.

- If the Creatio protocol or API service uses **non-blocking session mode** ,
  set up integration in multiple threads that use the same credentials.
- If the Creatio protocol or API service uses **blocking session mode** , use
  specific credential collection for each thread to leverage available app
  resources.

When you create integrations in a third-party app, make sure the integration can
use simultaneous threads that an external app generates when it accesses
Creatio. This lets you allocate resources optimally and ensure all subsystems
work as expected. At the same time, you can control the load of the integrated
app on the Creatio API.

---

## See also​

[Custom web services](https://academy.creatio.com/documents?ver=8.3&id=15262)

[Authentication](https://academy.creatio.com/documents?ver=8.3&id=15402)

[OData](https://academy.creatio.com/documents?ver=8.3&id=15431)

[DataService](https://academy.creatio.com/documents?ver=8.3&id=15411)

[Service that runs business processes](https://academy.creatio.com/documents?ver=8.3&id=15441)

[Integrations](https://academy.creatio.com/documents?ver=8.3&id=15085)

---

## Resources​

[OData client libraries](http://www.odata.org/libraries)

[Description of the differences between OData 3 and OData 4 protocols](http://docs.oasis-open.org/odata/new-in-odata/v4.01/new-in-odata-v4.01.html)

[Official OData documentation](https://www.odata.org/getting-started/)

[Description of the WCF technology](https://docs.microsoft.com/en-us/dotnet/framework/wcf/?redirectedfrom=MSDN)

- Data services
  - DataService service
  - OData protocol
- Service that runs business processes
- Custom web service
- Recommendations for integrating external apps with Creatio
- See also
- Resources
