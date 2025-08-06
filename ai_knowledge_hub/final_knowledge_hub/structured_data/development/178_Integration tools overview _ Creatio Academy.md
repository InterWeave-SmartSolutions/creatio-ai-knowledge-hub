# Integration tools overview | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 747 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/architecture/development-in-creatio/integrations

## Description

Integration is data exchange between systems with or without subsequent data
processing. The purpose of integration is to transfer custom data automatically
between apps.

## Key Concepts

business process, configuration, detail, integration, web service, odata, rest
api, database, operation, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/architecture/development-in-creatio/integrations)**
(8.3).

Version: 8.0

On this page

Level: beginner

**Integration** is data exchange between systems with or without subsequent data
processing. The **purpose** of integration is to transfer custom data
automatically between apps.

Creatio has a wide range of integrations with external apps. Creatio's open API
lets you implement integration solutions of any complexity.

Creatio has the following **ways to integrate** :

- Integration of external apps with Creatio.
- Creatio integration with external apps.

The choice of the integration method depends on the following **features** :

- client needs
- external app type and architecture
- developer expertise level

## Integration of external apps with Creatio​

The integration of external apps with Creatio solves the following **problems**
:

- execute CRUD operations with Creatio objects
- launch business processes
- implement custom tasks that you can solve using Creatio's open API

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Integrations/8.0/scr_IntegrationWithCreatio_en.png)

We recommend using multithreaded integration to maximize Creatio throughput.
Learn more in a separate article:
[Integration options](https://academy.creatio.com/documents?ver=8.0&id=15401&anchor=title-2296-1).

### Data services​

The **purpose** of data services is to execute CRUD operations with Creatio
objects. Learn more in separate articles:
[Access data directly](https://academy.creatio.com/documents?ver=8.0&id=15233),
[Data access through ORM](https://academy.creatio.com/documents?ver=8.0&id=15246).

Creatio lets you use the following **data services** :

- OData protocol
- DataService service

#### OData protocol​

**OData (Open Data Protocol)** is an ISO/IEC-approved OASIS standard. It defines
a set of best practices for building and using REST API. Use OData to create
REST-based services that let you publish and edit resources using simple HTTP
requests. Such resources should be identified with a URL and defined in the data
model. Learn more in a separate article:
[OData](https://academy.creatio.com/documents?ver=8.0&id=15431).

Creatio supports OData 4 and OData 3 protocols. OData 4 has more features than
OData 3. The main **difference** between the protocols is the data format of the
server's response. Learn more about the differences between OData 3 and OData 4
protocols in the official
[OData documentation](http://docs.oasis-open.org/odata/new-in-odata/v4.01/new-in-odata-v4.01.html).
Use the protocol version 4 when you integrate with Creatio via the OData
protocol.

Learn more about the detailed protocol description in the official
[OData documentation](https://www.odata.org/getting-started/).

#### DataService service​

**DataService** (developed by Creatio) is a service that implements
communication between front-end and back-end app parts. DataService lets you
transfer custom data to back-end app part to be processed and saved to a
database. Learn more in a separate article:
[DataService](https://academy.creatio.com/documents?ver=8.0&id=15411).

### Service that runs business processes​

Use the `ProcessEngineService.svc` system web service to run business processes
from an external app. Learn more in a separate article:
[Service that runs business processes](https://academy.creatio.com/documents?ver=8.0&id=15441).

### Custom web service​

Users can create **custom web services** to solve integration problems. The
configuration web service is RESTful service based on
[WCF](https://docs.microsoft.com/en-us/dotnet/framework/wcf/?redirectedfrom=MSDN)
technology. Learn more in a separate article:
[Custom web services](https://academy.creatio.com/documents?ver=8.0&id=15262).

## Creatio integration with external apps​

Use app tools to combine different enterprise apps into a single digital
ecosystem. When you integrate Creatio with external apps, you can develop a
custom solution or use an out-of-the-box integration solution.

### Develop custom integration solution​

Use app tools to
[set up integration](https://academy.creatio.com/documents?ver=8.0&id=1862) with
a custom RESTful API. You can call a web service from a business process after
you set up the integration. Use REST API tools to interact with external web
services with no developer involvement.

### Use out-of-the-box integration solution​

View the out-of-the-box integration solutions Creatio implements below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/Integrations/8.0/scr_IntegrationCreatio_en_8_0.png)

Creatio implements out-of-the-box integration solutions with the following
**apps** :

- [OneLogin portal](https://academy.creatio.com/documents?ver=8.0&id=1650), used
  as a single sign-on point for all company services.
- [Active Directory Federation Services (ADFS)](https://academy.creatio.com/documents?ver=8.0&id=1649)
  software component to manage single sign-on for all system users.
- [Just-In-Time User Provisioning (JIT UP)](https://academy.creatio.com/documents?ver=8.0&id=1759)
  function, which alleviates the need to create accounts for each separate
  service and keep the user database up-to-date manually.
- [Lightweight Directory Access Protocol (LDAP)](https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/category/synchronize-users-with-ldap)
  is an app layer protocol to access a specific database that usually stores
  accounts of users, computers, etc.
- Mail service via
  [IMAP/SMTP](https://academy.creatio.com/documents?ver=8.0&id=1415) protocol.
- [Google](https://academy.creatio.com/documents?ver=8.0&id=1773) mail,
  calendar, and contacts.
- [Webitel](https://academy.creatio.com/documents?ver=8.0&id=1366),
  [Asterisk](https://academy.creatio.com/documents?ver=8.0&id=1368),
  [Cisco Finesse](https://academy.creatio.com/documents?ver=8.0&id=1369),
  [TAPI](https://academy.creatio.com/documents?ver=8.0&id=1370),
  [CallWay](https://academy.creatio.com/documents?ver=8.0&id=1371),
  [Avaya](https://academy.creatio.com/documents?ver=8.0&id=1373) telephony
  services.
- [Microsoft Exchange and Microsoft 365](https://academy.creatio.com/documents?ver=8.0&id=1418)
  messaging and collaboration services.

---

## See also​

[Authentication](https://academy.creatio.com/documents?ver=8.0&id=15402)

[Service that runs business processes](https://academy.creatio.com/documents?ver=8.0&id=15441)

[DataService](https://academy.creatio.com/documents?ver=8.0&id=15411)

[OData](https://academy.creatio.com/documents?ver=8.0&id=15431)

---

## Resources​

[Tech Hour - Integrate like a boss](https://www.youtube.com/watch?v=mHaGY1DxETw&list=PLnolcTT5TeE3v8WGd3VqlZSd2D02GWSGa&index=2)

---

## E-learning courses​

[Integrations. Calling external web-services from the program code](https://academy.creatio.com/node/531113/takecourse)

[Data integration. Working with OData/DataService](https://academy.creatio.com/node/531101/takecourse)

- Integration of external apps with Creatio
  - Data services
  - Service that runs business processes
  - Custom web service
- Creatio integration with external apps
  - Develop custom integration solution
  - Use out-of-the-box integration solution
- See also
- Resources
- E-learning courses
