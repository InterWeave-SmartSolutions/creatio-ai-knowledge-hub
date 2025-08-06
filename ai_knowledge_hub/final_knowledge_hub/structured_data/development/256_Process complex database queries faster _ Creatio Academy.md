# Process complex database queries faster | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 604 **URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.0/administration/creatio-maintenance/process_complex_database_queries_faster

## Description

Some Creatio database queries take a long time to process, which might affect
page loading or task completion time significantly. Such queries are usually
called "heavy." They include:

## Key Concepts

section, dashboard, sql, database, operation, package, case

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

Some Creatio database queries take a long time to process, which might affect
page loading or task completion time significantly. Such queries are usually
called "heavy." They include:

- complex filters in pages and dynamic folders
- complex analytical selections in section dashboards
- complex custom queries implemented using development tools

You can accelerate the processing of heavy queries by forwarding them to a
read-only database replica. This will reduce the load on the main database
significantly and free up resources for the activity of users and the operation
of other Creatio elements.

To set up the redirection of heavy queries, take the following steps:

1. Create a read-only database replica.
2. Configure access to the database replica in Creatio.

## Step 1. Create a database replica​

The procedure to create a database replica is DBMS-specific. Learn more about
the process in vendor documentation:

- [Create a database replica in PostgreSQL](https://www.postgresql.org/docs/current/warm-standby.html).
- [Create a database replica in Microsoft SQL](https://docs.microsoft.com/en-us/sql/relational-databases/replication/sql-server-replication?view=sql-server-ver15).
- [Create a database replica in Oracle](https://docs.oracle.com/cd/B19306_01/server.102/b14228/config_simple.htm#STREP056).

## Step 2. Set up redirection of heavy queries​

1. **Set up redirection** of heavy queries to the database replica. Perform the
   setup in the Terrasoft.WebHost.dll.config file for **Creatio .NET Core and
   .NET** and in the web.config file for Creatio **NET Framework**.
   1. Select the `UseQueryKinds` checkbox.

      <add key="UseQueryKinds" value="true" />  


   2. Add the `replicaConnectionStringName="db_Replica"` value to the
      `db general` parameter.
      - For Microsoft SQL
      - For PostgreSQL


    <general connectionStringName="db" replicaConnectionStringName="db_Replica" securityEngineType="Terrasoft.DB.MSSql.MSSqlSecurityEngine, Terrasoft.DB.MSSql" executorType="Terrasoft.DB.MSSql.MSSqlExecutor, Terrasoft.DB.MSSql" engineType="Terrasoft.DB.MSSql.MSSqlEngine, Terrasoft.DB.MSSql" metaEngineType="Terrasoft.DB.MSSql.MSSqlMetaEngine, Terrasoft.DB.MSSql" metaScriptType="Terrasoft.DB.MSSql.MSSqlMetaScript, Terrasoft.DB.MSSql" typeConverterType="Terrasoft.DB.MSSql.MSSqlTypeConverter, Terrasoft.DB.MSSql" enableRetryDBOperations="false" retryDBOperationFactoryType="Terrasoft.DB.MSSql.MSSqlRetryOperationFactory, Terrasoft.DB.MSSql" binaryPackageSize="1048576" currentSchemaName="dbo" enableSqlLog="false" sqlLogQueryTimeElapsedThreshold="5000" sqlLogRowsThreshold="100" useOrderNullsPosition="false" maxEntitySchemaNameLength="128" />


    <general connectionStringName="db" replicaConnectionStringName="db_Replica" maxEntitySchemaNameLength="128" useOrderNullsPosition="false" sqlLogRowsThreshold="100" sqlLogQueryTimeElapsedThreshold="5000" enableSqlLog="false" currentSchemaName="public" binaryPackageSize="1048576" typeConverterType="Terrasoft.DB.PostgreSql.PostgreSqlTypeConverter, Terrasoft.DB.PostgreSql" metaScriptType="Terrasoft.DB.PostgreSql.PostgreSqlMetaScript, Terrasoft.DB.PostgreSql" metaEngineType="Terrasoft.DB.PostgreSql.PostgreSqlMetaEngine, Terrasoft.DB.PostgreSql" engineType="Terrasoft.DB.PostgreSql.PostgreSqlEngine, Terrasoft.DB.PostgreSql" maxAnsiJoinCount="0" isCaseInsensitive="true" executorType="Terrasoft.DB.PostgreSql.PostgreSqlExecutor, Terrasoft.DB.PostgreSql" securityEngineType="Terrasoft.DB.PostgreSql.PostgreSqlSecurityEngine, Terrasoft.DB.PostgreSql"/>

2. **Configure access** to the database replica in Creatio. To do this, add the
   `db_Replica` parameter to the `ConnectionStrings.config` file:
   - For Microsoft SQL
   - For PostgreSQL
   - For Oracle


    <add name="db_Replica" connectionString="Data Source=[Database server name]; Initial Catalog=[Database name]; Persist Security Info=True; MultipleActiveResultSets=True; Integrated Security=SSPI; Pooling = true; Max Pool Size = 100; Async = true" />


    <add name="db_Replica" connectionString="Server=[Database server name];Port=[Database server port];Database=[Database name];User ID=[PostgreSQL user that connects to the database];password=[PostgreSQL user password];Timeout=500; CommandTimeout=400;MaxPoolSiz>


    <add name="db_Replica" connectionString="Data Source=(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST =[Database server name])(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME =[Oracle service name]) (SERVER = DEDICATED)));User Id=[Schema name];Password=[Schema password];Statement Cache Size = 300" />

---

## See also​

[Requirements calculator](https://academy.creatio.com/docs/requirements/calculator)

[General Creatio deployment procedure](https://academy.creatio.com/documents?id=1263)

[Set up a dedicated query pool (developer documentation)](https://academy.creatio.com/documents?id=15261)

- Step 1. Create a database replica
- Step 2. Set up redirection of heavy queries
- See also
