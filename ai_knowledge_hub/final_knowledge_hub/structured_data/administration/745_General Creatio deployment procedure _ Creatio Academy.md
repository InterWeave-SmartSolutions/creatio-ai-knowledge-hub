# General Creatio deployment procedure | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 428
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/on-site-deployment/general-creatio-deployment-procedure

## Description

This guide covers all steps needed to deploy and set up Creatio on-site on
Windows or Linux, as well as links to detailed descriptions of each step.

## Key Concepts

configuration, detail, integration, sql, database, operation, synchronization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/on-site-deployment/general-creatio-deployment-procedure)**
(8.3).

Version: 8.1All Creatio products

On this page

This guide covers all steps needed to deploy and set up Creatio on-site on
Windows or Linux, as well as links to detailed descriptions of each step.

## Deploy the Creatio application on Windows​

The general procedure to deploy Creatio on-site is as follows:

1. Deploy the Creatio caching server (Redis).
   [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/category/caching-server)
2. Deploy the database. Note that this step is DBMS-dependent.
   [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/category/database-server)
3. Enable and install the required Windows components.
   [Read more >>>](https://academy.creatio.com/documents?id=2081)
4. Install the latest Windows updates.
5. Create and set up the application website using IIS.
   [Read more >>>](https://academy.creatio.com/documents?id=2136)
6. Modify the ConnectionStrings.config file. Note that this step is
   DBMS-dependent.
   [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/category/application-server-on-windows)
7. Modify the Web.config file.
   [Read more >>>](https://academy.creatio.com/documents?id=2141)

After installing Creatio, perform **additional setup** to ensure correct
operation of all its components.

- Set up websockets.
  [Read more >>>](https://academy.creatio.com/documents?id=1631)
- Switch Creatio from HTTP to HTTPS.
  [Read more >>>](https://academy.creatio.com/documents?id=1632)
- Deploy and set up global search in Creatio.
  [Read more >>>](https://academy.creatio.com/documents?id=1712)
- Set up the machine learning service.
  [Read more >>>](https://academy.creatio.com/documents?id=1935)
- Set up integrations and Internet access for additional functions. For example,
  the data enrichment service, social media integration, or Google
  synchronization.
  [Read more >>>](https://academy.creatio.com/docs/8.x/setup-and-administration/category/additional-setup)
- Set up bulk emails (only for configurations with Marketing Creatio).
  [Read more >>>](https://academy.creatio.com/documents?id=1777)

## Deploy the Creatio .NET 6 application on Linux​

The general procedure to deploy Creatio on-site is as follows:

1. Prepare the Creatio setup files.
   [Read more >>>](https://academy.creatio.com/documents?id=2450)
2. Deploy the database server.
   [Read more >>>](https://academy.creatio.com/documents?id=2121)
3. Deploy the Creatio caching server (Redis).
   [Read more >>>](https://academy.creatio.com/documents?id=2108)
4. Modify the ConnectionStrings.config file.
   [Read more >>>](https://academy.creatio.com/documents?id=2450#title-263-2)
5. Deploy the Creatio application server.
   [Read more >>>](https://academy.creatio.com/documents?id=2451)

If you are going to run Creatio directly **on the local machine** :

1. Install .NET 6, a GDI+ compatible API for UNIX-like operating systems, and
   development libraries and header files for GNU C.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-2)
2. Run the Creatio application server.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-3)

If you are going to run Creatio **in a Docker container** :

1. Make Redis accessible from the Docker container.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-5)
2. Install Docker.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-6)
3. Create a Dockerfile.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-7)
4. Build and run the Docker image.
   [Read more >>>](https://academy.creatio.com/documents?id=2451#title-2649-8)

note

The procedure for running a PostgreSQL server in Docker is covered in the
[Docker documentation](https://hub.docker.com/_/postgres).

---

## See also​

[Database server](https://academy.creatio.com/docs/8.x/setup-and-administration/category/database-server)

[Caching server](https://academy.creatio.com/docs/8.x/setup-and-administration/category/caching-server)

[Application server on Windows](https://academy.creatio.com/docs/8.x/setup-and-administration/category/application-server-on-windows)

[Additional setup](https://academy.creatio.com/docs/8.x/setup-and-administration/category/additional-setup)

[Containerized components](https://academy.creatio.com/docs/8.x/setup-and-administration/category/%D1%81ontainerized-components)

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

---

## Resources​

[Tech Hour - Installing Local instance of Creatio](https://youtu.be/lf-yWsJ4p0Q)

- Deploy the Creatio application on Windows
- Deploy the Creatio .NET 6 application on Linux
- See also
- Resources
