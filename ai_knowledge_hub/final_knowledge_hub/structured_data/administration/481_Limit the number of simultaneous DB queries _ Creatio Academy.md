# Limit the number of simultaneous DB queries | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 486
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/creatio-maintenance/limit_DB_thread_count

## Description

This functionality is available in Creatio version 8.0.2 and higher for MSSQL
PostgreSQL DBMS.

## Key Concepts

business process, configuration, section, integration, sql, database, operation,
system setting

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/administration/user-and-access-management/user-access-overview)**
(8.3).

Version: 8.0All Creatio products

On this page

note

This functionality is available in Creatio version 8.0.2 and higher for MSSQL
PostgreSQL DBMS.

You can improve application performance by limiting the amount of processor
resources (threads) that a heavy database query can consume. This will reduce
the impact of resource-intensive procedures on the work of users. Such requests
are generated both in the background, for example, when executing business
processes or integrations, or by users, for example, sorting registries by an
aggregate column. This article describes how to configure restrictions for
on-site applications. For cloud applications, these restrictions are applied
automatically after upgrading to version 8.0.2.

The thread limiting mechanism works most effectively on servers with 4 or more
processor cores.

The general procedure for setting restrictions consists requires steps:

1. Enable resource limit in configuration files.
   [Read more >>>](https://academy.creatio.com#)
2. Set resource limit in Creatio settings.
   [Read more >>>](https://academy.creatio.com#)

## Enable resource limit for requests​

Limiting the number of threads is disabled in Creatio by default. You can enable
it in the ApplyMaxDopHintToUserQueries section of the configuration file:

- For **NET Framework** , these are web.config files located in the root folder
  of the application and in the TerrasoftWebApp folder.
- For **.NET Core and .NET** , this is the Terrasoft.WebHost.dll.config file
  located in the root folder of the application.

Configuration file line example

    <configuration>
        ...
        <appsettings>
            ...
            <add key="ApplyMaxDopHintToUserQueries" value="true">
            ...
        </appsettings>
        ...
    </configuration>

## Set resource limit for requests​

The system setting "Number of MaxDopQueryHint Threads" (code
"MaxDopHintThreadsCount") is intended to throttle the resources that can be used
for queries to the database. To set a resource limit:

1. Open the system designer by clicking the
   ![btn_system_designer00001.png](https://academy.creatio.com/docs/sites/default/files/documentation/user/ru/sys_settings_lookups/BPMonlineHelp/add_lookups/btn_system_designer00001.png)
   button in the upper right corner of the application.

2. In the **System settings** group, click **System settings**.

3. Open the "MaxDopQueryHint thread count" system setting (code
   "MaxDopHintThreadsCount").

4. In the **Default value** field, set the resource limit. We recommend using
   from a quarter to a half of the total number of available threads, assuming
   one thread corresponds to one processor core. In this way, you prevent all
   available threads from being occupied by resource-intensive operations.

note

The limit of half of the available number of threads allows you to perform all
the necessary processes and tasks, while not slowing down the work of users. For
the number of threads between 4 and 8 threads, we recommend setting the limit
between 2 and 4 (i.e. half the number of available threads).

As a result, the load on the resources of the database server processors is
significantly reduced, which allows you to perform resource-intensive operations
without affecting the work of Creatio users.

---

## See also​

[System requirements calculator](https://academy.creatio.com/docs/calculator)

- Enable resource limit for requests
- Set resource limit for requests
- See also
