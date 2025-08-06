# Bulk duplicate search service | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 637 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/architecture/microservices/bulk-duplicate-search

## Description

Bulk duplicate search is a third-party service for bulk deduplication of Creatio
section records.

## Key Concepts

section, web service, sql, database, operation, system setting, lead, contact,
account, customization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

Bulk duplicate search is a third-party service for bulk deduplication of Creatio
section records.

Duplicate records may appear in Creatio whenever users add new records to system
sections. Finding and merging duplicates helps maintain the quality of your data
in any Creatio section.

## Bulk duplicate search basics​

You need the
[global search service](https://academy.creatio.com/documents?ver=8.3&id=15063)
set up and configured using
[ElasticSearch](https://en.wikipedia.org/w/index.php?title=Elasticsearch&oldid=993216412)
to ensure the operation of the bulk duplicate search service.

Creatio implements the following duplicate search modes:

- **Bulk duplicate search** – check for duplicates is run for the entire
  database. Launched manually or automatically.
- **Duplicates search when saving a record** – checks for duplicates for a
  particular record. It is run automatically when a new record is added and
  saved in a section.

Additionally, you can manually merge any records in a section, even if they were
not flagged as duplicates. This option is available for all system sections. By
default, duplicate search is available in the **Accounts** , **Contacts** and
**Leads** sections. In Creatio, the duplicate search is executed with the help
of pre-configured rules. Creatio also provides customization of out-of-the-box
duplicate search rules for contacts, accounts, and leads. Create custom rules
for any Creatio section, including custom sections.

The bulk duplicate search function is pre-enabled in Creatio applications
deployed in the cloud. Creatio applications deployed on-site require the
[global search service](https://academy.creatio.com/documents?ver=8.3&id=15063)
set up and configured before the bulk duplicate search service can be enabled.

[To connect bulk duplicate search to Creatio](https://academy.creatio.com/documents?ver=8.3&id=1959),
take the following steps:

1. Set up the **Deduplication service api address**
   [system setting](https://academy.creatio.com/documents?ver=8.3&id=269) value.
2. Set up the **Duplicates search**
   [operation permissions](https://academy.creatio.com/documents?ver=8.3&id=2000).
3. Run the SQL script to
   [enable the bulk duplicate search functionality in Creatio](https://academy.creatio.com/documents?ver=8.3&id=1959)
   (`BulkESDeduplication`, `ESDeduplication`, `Deduplication`).
4. Restart the Creatio application.

## Bulk duplicate search service operation schema​

Bulk duplicate search service consists of the following components:

- **RabbitMQ** – message broker. Bulk duplicate search service component.
- **ElasticSearch** – a search engine. Bulk duplicate search service component.
- **Redis** – repository used for caching and speed.
- **MongoDB** – document-oriented DBMS.
- **WebAPI** – web service for communicating in the main Creatio application.
- **Data Service** – internal service for communication with a MongoDB
  component.
- **Duplicates Search Worker** – duplicate search component.
- **Duplicates Deletion Worker** – targeted duplicate deletion component.
- **Duplicates Confirmation Worker** – component for grouping and filtering the
  detected duplicates based on their uniqueness.
- **Duplicates Cleaner** – component for clearing the duplicates.
- **Deduplication Task Worker** – component for setting the deduplication task.
- **Deduplication Preparation Worker** – component for preparing the
  deduplication process. This component generates queries for duplicate search
  according to the rules.

Operation scheme of the bulk duplicate search service

![Operation scheme of the bulk duplicate search service](https://academy.creatio.com/sites/default/files/pictures/SchemyBezOU_EN/7.18/BezOU+GP+D.png)

## Bulk duplicate search service scalability​

Database clustering enables scaling of the bulk duplicate search service in
large projects. Learn more about ElasticSearch clustering:
[official vendor documentation](https://www.elastic.co/guide/en/cloud-on-k8s/master/k8s-deploy-elasticsearch.html)
(Elastic).

## Bulk duplicate search service compatibility with Creatio products​

The bulk duplicate search service features several versions: 1.0-1.5, 2.0. Each
version is compatible with all Creatio products of version 7.14 and up.

## Bulk duplicate search service deployment options​

You can deploy the bulk duplicate search service on-site and in the cloud.

On-site applications require a
[preliminary setup of the global search service](https://academy.creatio.com/documents?ver=8.3&id=1712).
To set up the bulk duplicate search service, you need a server (a physical or
virtual machine) that meets specific
[system requirements](https://academy.creatio.com/docs/8.x/setup-and-administration/category/system-requirements).
Both servers must run under Linux with
[Docker](<https://en.wikipedia.org/w/index.php?title=Docker_(software)&oldid=992064330>)
installed. You can find the list of supported Linux distributions in the
[Docker documentation](https://docs.docker.com/get-docker/).

We recommend that you install the most up-to-date version of the bulk duplicate
search service.

---

## E-learning courses​

[Tech Hour - Docker for Creatio](https://www.youtube.com/watch?v=cwTI8pIa_5g)

- Bulk duplicate search basics
- Bulk duplicate search service operation schema
- Bulk duplicate search service scalability
- Bulk duplicate search service compatibility with Creatio products
- Bulk duplicate search service deployment options
- E-learning courses
