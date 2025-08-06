# Global search | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 723 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/architecture/microservices/global-search

## Description

The global search integrates ElasticSearch with Creatio. Learn more: Wikipedia.

## Key Concepts

business process, configuration, section, detail, lookup, web service, database,
operation, system setting, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/architecture/microservices/global-search)**
(8.3).

Version: 8.1

On this page

Level: beginner

The **global search** integrates ElasticSearch with Creatio. Learn more:
[Wikipedia](https://en.wikipedia.org/w/index.php?title=Elasticsearch&oldid=993216412).

Use the global search to quickly search data in the Creatio by entering a search
request in the search string. Creatio always searches in all sections (including
custom sections).

## Global search basics​

The global search implements recording and transport functions by doing the
following:

- Subscribes clients by creating an index in ElasticSearch and saves the
  connection between the index and the app.
- Disconnects clients by removing their index in ElasticSearch.
- Participates in the indexing process by retrieving data from the database.

Creatio executes the following actions using the global search:

- Search records by their text and lookup fields as well as the **Addresses** ,
  **Communication options** , and **Banking details** expanded lists.
- Search files and links on the **Attachments and notes** tab of the record page
  by their name or description.
- Take into account common typos and morphology of different word forms in
  English when handling search requests. The search request is case-insensitive.
- Rank the search results by relevance both in the actual results list and with
  any configured filters. For example, if the search is performed from a
  section, the records of this section are displayed at the beginning of the
  results list.
- If a user does not have permissions for a specific object column, such a
  column is not displayed on the page of global search results.

View the system settings to set up global search parameters in the table below.

| System setting | System setting code | Description | Global search default entity weight | GlobalSearchDefaultEntityWeight | Set up the rules for displaying search results. | Global search default primary column weight | Global search default primary column weight | Display search results with partial match | UseInexactGlobalSearch | Display search results taking morphology, typos, and fuzzy matches into account. | Match threshold for displaying in search results (percent) | GlobalSearchShouldMatchPercent | Manage the number of displayed search results with partial match and increase the chances of finding data for inaccurate search requests. |
| -------------- | ------------------- | ----------- | ----------------------------------- | ------------------------------- | ----------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ----------------------------------------- | ---------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |

## Global search operation schema​

View the components of global search in the table below.

| Component | Description | RabbitMQ | Message broker. | ElasticSearch | A search engine. | GS Database Server | Database for configuring the global search component. | GS Caching Server Redis | Database used for caching and speed. | WebAPI | Web service for global search component configuration. | Indexing Service | Web service for processing the requests for the targeted indexing of Creatio data. | GS Scheduler | Scheduler for indexing data from Creatio to ElasticSearch. | GS Worker | Index data from Creatio to ElasticSearch as per the **GS Scheduler** tasks. | GS Replay Worker | Handle indexing results (**GS Worker** operation results). | GS Single Worker | Index of business process data in ElasticSearch upon a request from the business process. | GS Single Replay Worker | Handle exceptions when processing targeted indexing results (**GS Single Worker** operation results). | GS Single Task Worker | Schedule tasks for **GS Single Worker**. | GS Queried Single Task Worker | Generate tasks for **GS Single Worker**. |
| --------- | ----------- | -------- | --------------- | ------------- | ---------------- | ------------------ | ----------------------------------------------------- | ----------------------- | ------------------------------------ | ------ | ------------------------------------------------------ | ---------------- | ---------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------------- | --------- | --------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------- | ----------------------------- | ---------------------------------------- |

View the operation schema of the global search below.

![](https://academy.creatio.com/sites/default/files/pictures/SchemyBezOU_EN/8.0/BezOU+GP.png)

## Global search requests handling​

View the schema of handling global search requests below.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/GlobalSearch/8.2/scr_handling_global_search_requests.png)

## Global search scalability​

Database clustering enables scaling of the global search in large projects.
Learn more about ElasticSearch clustering:
[official vendor documentation](https://www.elastic.co/guide/en/cloud-on-k8s/master/k8s-deploy-elasticsearch.html)
(Elastic).

## Global search compatibility with Creatio products​

The global search is compatible with all Creatio products of version 7.10 and
up. Learn more:
[Global search](https://academy.creatio.com/documents?ver=8.1&id=1712),
[Global search and deduplication FAQ](https://academy.creatio.com/documents?ver=8.1&id=2342)
(user documentation).

## Global search deployment options​

You can deploy the global search on-site and in the cloud.

Creatio **on-site** requires a preliminary setup of the global search. To set up
the service, you need two servers (physical or virtual machines) that meet
[Server-side system requirements](https://academy.creatio.com/documents?ver=8.1&id=1456)
(user documentation). Both servers must run under Linux with Docker installed.
Learn more about the list of supported Linux distributions:
[official vendor documentation](https://docs.docker.com/get-docker/) (Docker).

---

## See also​

[Global search](https://academy.creatio.com/documents?ver=8.1&id=1712) (user
documentation)

[Global search and deduplication FAQ](https://academy.creatio.com/documents?ver=8.1&id=2342)
(user documentation)

[Server-side system requirements](https://academy.creatio.com/documents?ver=8.1&id=1456)
(user documentation)

---

## Resources​

[Elasticsearch](https://en.wikipedia.org/w/index.php?title=Elasticsearch&oldid=993216412)
(Wikipedia)

[Official Elastic documentation](https://www.elastic.co/guide/en/cloud-on-k8s/master/k8s-deploy-elasticsearch.html)

[Official Docker documentation](https://docs.docker.com/get-docker/)

---

## E-learning courses​

[Tech Hour - Docker for Creatio](https://www.youtube.com/watch?v=cwTI8pIa_5g)

- Global search basics
- Global search operation schema
- Global search requests handling
- Global search scalability
- Global search compatibility with Creatio products
- Global search deployment options
- See also
- Resources
- E-learning courses
