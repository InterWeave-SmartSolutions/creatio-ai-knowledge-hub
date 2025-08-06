# Creatio platform overview | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1736 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/architecture/creatio-platform

## Description

The classic 3-tier Creatio architecture is cross-platform, flexible, and
scalable.

## Key Concepts

business process, configuration, integration, sql, database, operation, package,
mobile app, case, no-code

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/architecture/creatio-platform)**
(8.3).

Version: 8.2

On this page

Level: beginner

The classic 3-tier Creatio architecture is cross-platform, flexible, and
scalable.

Creatio allows for the following **deployment options** :

- **Without fault-tolerance**. Basic infrastructure option without using load
  balancers.
- **With fault-tolerance**. Infrastructure option that has horizontal scaling.
  Fault tolerance is implemented using Creatio server, database, and caching
  load balancers.

## Creatio layers​

Creatio has a classic **3-tier architecture** that has the following layers:
data, application, presentation.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MainApplication/scr_CreatioLevels.png)

### Presentation layer​

The presentation layer enables users to access the Creatio UI via a web browser
or a mobile app for Android or iOS. The layer contains web pages, JavaScript
code, and styles that define the **UI logic and look**.

The **key technologies** used here are Angular, JavaScript, HTML5, CSS.

The **supported browsers** include Chrome, Firefox, Edge, and Safari.

Mobile Creatio is an alternative client to access the app that uses the UI
optimized for Android and iOS devices.

### Application layer​

The application layer is implemented on .Net Platform (C#). You can deploy the
layer on Windows and Linux web servers. The application layer defines the **core
business logic** , such as dynamic case management, business process engine,
phone integration, etc.

The layer handles user authentication/authorization, license checks, and
instantiation. It also runs custom business logic implemented via Creatio and
no-code tools.

This layer corresponds to the application server on the infrastructure level.

### Data layer​

The data layer stores and manages all customer **data** , app settings, app
properties, and user authentication data.

Creatio uses it for in-memory storage of the session data and frequently used
caches, as well as quick interactions between web farm nodes.

**Supported DBMS** :

- Microsoft SQL Server, Oracle and PostgreSQL for **on-site** deployment
- PostgreSQL for **cloud** deployment

**Caching server** : Redis database.

The layer corresponds to the caching server and database server on the
infrastructure level.

## Creatio infrastructure​

The Creatio infrastructure includes the following **components** :

- Application server.
- Database server.
- Caching server.
- Version control system server (optional). Needed for multi-user development.
- Mobile Creatio (optional). Opens Creatio on a mobile device.

View the general architectural diagram of Creatio without fault tolerance in the
figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MainApplication/7.18/scr_ArchitectureWithoutFaultTolerance.png)

note

The architecture of Creatio with fault tolerance requires load balancers, as
well as additional application, Redis, and database servers.

### Application server​

The application server corresponds to the application layer and performs the
main computations.

Creatio supports the .Net Platform (C#). View the setup options for Creatio
products in the table below.

| Creatio products | .NET Framework | .NET | Marketing | +   | +   | Sales Enterprise | +   | +   | Sales Commerce | +   |     | Sales Team | +   |     | Service Enterprise | +   | +   | Customer Center | +   |     | Studio | +   | +   | Lending | +   |     | Bank Customer Journey | +   |     | Bank Sales | +   |     | Sales Enterprise & Marketing & Service Enterprise | +   | +   | Sales Enterprise & Marketing & Customer Center | +   |     | Sales Commerce & Marketing & Customer Center | +   |     | Sales Team & Marketing | +   |     | Sales Team & Marketing & Customer Center | +   | +   | Bank Sales & Bank Customer Journey & Lending & Marketing | +   | +   |
| ---------------- | -------------- | ---- | --------- | --- | --- | ---------------- | --- | --- | -------------- | --- | --- | ---------- | --- | --- | ------------------ | --- | --- | --------------- | --- | --- | ------ | --- | --- | ------- | --- | --- | --------------------- | --- | --- | ---------- | --- | --- | ------------------------------------------------- | --- | --- | ---------------------------------------------- | --- | --- | -------------------------------------------- | --- | --- | ---------------------- | --- | --- | ---------------------------------------- | --- | --- | -------------------------------------------------------- | --- | --- |

#### .NET Framework application server​

Creatio on **.NET Framework** runs under Microsoft Internet Information Services
(**IIS**) in **Windows**.

Learn more about the system requirements for .NET Framework Creatio product
servers:
[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator).

The .NET Framework Creatio application server consists of the following
components:

1. The **loader** (`WebAppLoader`), an application that performs Creatio service
   functions and redirects users to the configuration component of the main
   Creatio application.

The loader handles the following:

     * user authorization
     * license verification and user authentication
     * running the background task scheduler

The loader is located in the Creatio root folder on the file system level.

After the application loader authenticates a request, the users can work with
the configuration component.

2. The **configuration component** (`WebApp`), an application that implements
   specific configuration in Creatio and handles the business logic.

The configuration component is located in the `Terrasoft.WebApp` folder on the
file system level.

#### .NET application server​

Creatio on **.NET** runs under **Kestrel** on **Linux** and Microsoft Internet
Information Services (**IIS**) in **Windows**.

Learn more about the system requirements for .NET Creatio product servers:
[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator).

Creatio on .NET is monolithic and serves as both the application **loader** and
the **configuration component**. Learn more:
[Creatio .NET products](https://academy.creatio.com/documents?ver=8.2&id=2453).

### Database server​

The database server is a part of the Creatio data layer.

The database stores the following data:

- user data
- data required for Creatio operation
- configuration settings that determine the product functionality

You can use the following DBMS:

- Microsoft SQL Server (for on-site deployment)
- Oracle (for on-site deployment)
- PostgreSQL (for cloud deployment)

Find the up-to-date versions of supported DBMS in the
[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)
after performing the calculations.

View the setup options for Creatio products in the table below.

| Creatio products | Microsoft SQL | Oracle | PostgreSQL | .NET Framework | .NET | Marketing | +   |     | +   | +   | Sales Enterprise | +   |     | +   | +   | Sales Commerce | +   |     | +   |     | Sales Team | +   |     | +   |     | Service Enterprise | +   |     | +   | +   | Customer Center | +   |     | +   |     | Studio | +   |     | +   | +   | Lending | +   |     | +   |     | Bank Customer Journey | +   |     | +   |     | Bank Sales | +   |     | +   |     | Sales Enterprise & Marketing & Service Enterprise | +   | +   | +   | +   | Sales Enterprise & Marketing & Customer Center | +   |     | +   |     | Sales Commerce & Marketing & Customer Center | +   |     | +   |     | Sales Team & Marketing | +   |     | +   |     | Sales Team & Marketing & Customer Center | +   |     | +   | +   | Bank Sales & Bank Customer Journey & Lending & Marketing | +   | +   | +   | +   |
| ---------------- | ------------- | ------ | ---------- | -------------- | ---- | --------- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | -------------------------------------------------------- | --- | --- | --- | --- |

### Redis caching server​

Redis is a part of the Creatio data layer. It handles the following tasks:

- user and application data storage (user profile, session data, etc.)
- cached data storage
- data exchange between web farm nodes

Creatio uses **data warehousing** to achieve these goals. This technology is
based on an object class model, a unified API that manages the application's
access to data in an external repository. Creatio uses Redis caching server as
the external repository.

Redis supports the following data storage strategies:

- **Data storage in memory only**. Redis converts a persistent database to a
  caching server.
- **Periodical saves to drive** (default). Redis creates a data snapshot every
  1-15 minutes depending on when the previous snapshot was created and the
  number of modified keys.
- **Transaction log**. Redis synchronously records each change to a special
  append-only log-file.
- **Replication**. You can assign a master server to each Redis server. Redis
  will replicate all changes to master servers on slave servers.

Define the data storage strategy in Redis server configuration.

### Version control system server (optional)​

The version control system server is an optional Creatio component. Use this
component when developing custom configurations in parallel with the normal
operation of Creatio. Version control system is required for **multi-user
development**. Learn more about setting up a version control system server:
[Version control system for development environments](https://academy.creatio.com/documents?ver=8.2&id=2321)
(user documentation).

The version control server handles the following functions:

- **Migrating changes between Creatio applications during the development**. The
  version control system transfers changes via packages stored as sets of files
  and directories on the file system level.
- **Storing the configuration status as packages of a specific version**. The
  version control system stores all configuration elements that you develop in
  the packages.

The Creatio IDE is designed to work with Subversion, but you can use other
version control systems when developing in third-party IDEs.

## Horizontal scaling​

You can enhance the performance of large-scale Creatio projects through
horizontal scaling. Use horizontal scaling for a Creatio instance that has
fault-tolerance.

The Creatio instance that has fault tolerance includes the following
**components** :

- Load balancer. The load balancer can be either hardware or software. To work
  in fault-tolerant mode, use an HTTP/HTTPS traffic balancer that supports
  WebSocket protocol. Learn more about installing and setting up the balancer:
  [Application server web farm](https://academy.creatio.com/documents?ver=8.2&id=2110)
  (user documentation).
- Web farm (multiple application servers).
- Caching server that uses the
  [Redis Cluster](https://academy.creatio.com/documents?ver=8.2&id=2349)
  mechanism (multiple Redis caching servers).
- Database server or database cluster (multiple database servers).
- Version control system server (optional).

View the general architectural diagram of Creatio with horizontal scaling in the
figure below.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/MainApplication/7.18/scr_WebFarmArchitecture.png)

## Deployment options​

Creatio supports the following deployment options:

- on-site (deploy the Creatio instance on the customer's local servers)
- cloud (deploy the Creatio instance in the cloud)

### On-site deployment​

When deploying Creatio on-site, the customer is responsible for all server
infrastructure expenses, including the installation, configuration, maintenance,
and administration.

On-site deployment **advantages** :

- Fast and convenient development.
- Independent development environments. Since development is performed in a
  separate Creatio instance, it cannot affect other users.
- Version control system lets you save and migrate changes.
- IDE and continuous integration pipeline setup are supported.

On-site deployment **constraints** :

- Dedicated servers are required to deploy Creatio components.
- Continuous updates, debugging, infrastructure administration are required.

When deploying Creatio on-site, make sure that both Creatio servers and client
computers meet the system requirements. To calculate server parameters required
to deploy Creatio and containerized components, use the
[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator).

Learn more about Creatio on-site deployment and setup stages on Windows or
Linux:
[On-site deployment](https://academy.creatio.com/docs/8.x/setup-and-administration/category/on-site-deployment)
(user documentation).

### Cloud deployment​

In the cloud mode, Creatio is deployed on cloud data center servers (Amazon,
Azure) managed by Creatio. Both servers and data are physically located in the
data centers. Creatio handles all issues related to administration, speed, or
scalability. The customers only use the client part of Creatio.

Cloud deployment **advantages** :

- Timely updates.
- Maximum performance.
- Compliance with industry standards on data availability and security.

Cloud deployment **constraints** :

- Creatio in the cloud must comply with the set of requirements. Learn more:
  [Development environment](https://academy.creatio.com/documents?ver=8.2&id=15201&anchor=title-2124-1).
- Creatio in the cloud supports PostgreSQL only.

You can deploy Creatio cloud from a
[trial version](https://www.creatio.com/trial/creatio) available on our website.
During the 14-days trial period, you can get familiar with the main features of
the application. After the trial period ends, the demo version can be migrated
to the main Creatio platform.

---

## See also​

[Environment overview](https://academy.creatio.com/documents?ver=8.2&id=15201)

[System requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

[Version control system for development environments](https://academy.creatio.com/documents?ver=8.2&id=2321)
(user documentation)

[Packages overview](https://academy.creatio.com/documents?ver=8.2&id=15121)

[Application server web farm](https://academy.creatio.com/documents?ver=8.2&id=2110)
(user documentation)

[Creatio .NET Core products](https://academy.creatio.com/documents?ver=8.0&id=2341)
(user documentation)

---

## Resources​

[PostgreSQL downloads](https://www.postgresql.org/download/)

[Redis caching server documentation](https://redis.io/documentation)

[On-site deployment](https://academy.creatio.com/docs/8.x/setup-and-administration/category/on-site-deployment)
(user documentation)

[Version control tools](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/version-control-tools)

---

## E-learning courses​

[Creatio architecture](https://academy.creatio.com/group/91/module/160/answer/569)

- Creatio layers
  - Presentation layer
  - Application layer
  - Data layer
- Creatio infrastructure
  - Application server
  - Database server
  - Redis caching server
  - Version control system server (optional)
- Horizontal scaling
- Deployment options
  - On-site deployment
  - Cloud deployment
- See also
- Resources
- E-learning courses
