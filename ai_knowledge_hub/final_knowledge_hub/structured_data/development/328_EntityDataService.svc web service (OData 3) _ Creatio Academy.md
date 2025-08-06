# EntityDataService.svc web service (OData 3) | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1160 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/data-services/odata/references/entitydataservice-svc-odata-3

## Description

The $count and $value OData 3 parameters will be retired in Creatio version
8.0.10.

## Key Concepts

web service, odata, sql, database, contact

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

Important

The `$count` and `$value` OData 3 parameters will be retired in Creatio version
8.0.10.

Depending on the request type, OData 3 protocol can return different data. Learn
more about the request and response structure below.

- Request structure
- Response structure

  // Request string.  
  method Creatio_application_address/0/ServiceModel/EntityDataService.svc/objects_collectionCollection(guid'object_id')/object_field?$parameters

  // Request headers.  
  Accept: application/atom+xml; type=entry  
  Content-Type: application/json; odata=verbose  
  ForceUseSession: true  
  BPMCSRF: authentication_cookie_value

  // Request body (for POST and PATCH requests).  
  {  
   "field1": "value1",  
   "field2": "value2",  
   ...  
  }

  // The status code.  
  Status: code

  // Response body (available in GET and POST requests).
  <?xml version="1.0" encoding="utf-8"?>
  <feed xml:base="https://mycreatio.com/0/ServiceModel/EntityDataService.svc/" xmlns="https://www.w3.org/2005/Atom" xmlns:d="https://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="https://schemas.microsoft.com/ado/2007/08/dataservices/metadata">  
      <id>https://mycreatio.com/0/ServiceModel/EntityDataService.svc/data_resource</id>  
      <title type="text">data_resource</title>  
      <updated>date and time of request</updated>  
      <link rel="self" title="data_resource" href="data_resource" />  
      <entry>  
          metadata_data  
          <content type="application/xml">  
              <m:properties>  
                  <d:object1 field1>object1 field_value1</d:object1 field1>  
                  <d:object1 field2>object1 field_value2</d:object1 field2>  
                  ...  
              </m:properties>  
          </content>  
      </entry>  
      <entry>  
          metadata_data  
          <content type="application/xml">  
              <m:properties>  
                  <d:object2 field1>object2 field_value1</d:object2 field1>  
                  <d:object2 field2>object2 field_value2</d:object2 field2>  
                  ...  
              </m:properties>  
          </content>  
      </entry>  
      ...  
  </feed>

## Request string​

    method required

Creatio supports the following request methods:

- `GET` – retrieve data
- `POST` – add data
- `PATCH` – modify data
- `DELETE` – delete data

  Creatio_application_address required

Creatio application URL.

    ServiceModel required

OData 3 protocol’s web service URL. Unmodifiable part of the request.

    EntityDataService.svc required

OData 3 protocol’s web service URL. Unmodifiable part of the request.

    objects_collectionCollection required

Name of the database table (name of the object collection). When using the OData
3 protocol, add `Collection` to the first name of the object collection in the
request string (e.g., `ContactCollection`). Run a query to receive the list of
database tables.

- MSSQL
- Oracle
- PostgreSQL

  SELECT \* FROM INFORMATION_SCHEMA.TABLES

  SELECT \* FROM ALL_TABLES

  SELECT table_name FROM information_schema.tables

  guid'object_id' optional

The identifier of the database table record string (identifier of the collection
object instance). For example, `guid'00000000-0000-0000-0000-000000000000'`).

    object_field optional

The database table record field (field of the collection object instance).

    parameters optional

Optional OData 3 parameters you can use in the `GET` Creatio request string. Use
the `?` operator to specify the parameters. Add the parameter name after the `$`
operator. Use the `&` operator to use two or more parameters.

Available values

| [$value](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#requestingapropertysrawvalueusingvalue) |     | The field value. | [$count](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#requestingthecountofanentitycollection) | `$count=true` | The number of elements in the selection. | [$skip](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#theskipsystemqueryoption) | `$skip=n` | The first n elements that must be excluded from the selection. | [$top](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#thetopsystemqueryoption) | `$top=n` | The first n elements that must be included in the selection. | [$select](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#theselectsystemqueryoption) | `$select=field1,field2,...` | The set of fields that must be included in the selection. | [$orderby](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#theorderbysystemqueryoption) | `$orderby=field asc` or `$orderby=field desc` | How to sort the field values in the selection. | [$expand](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#theexpandsystemqueryoption) | `$expand=field1,field2,...` | Extension of the connected fields. | [$filter](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#thefiltersystemqueryoption) | `$filter=field template 'field_value'` | How to filter the fields in the selection. |
| --------------------------------------------------------------------------------------------------------------------------------------- | --- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------ |

## Request headers​

    Accept application/atom+xml; type=entry required

Data type to expect in the server response. The server returns the response in
XML. Optional for `GET` requests.

    Content-Type application/json; odata=verbose required

Ecoding and type of the resource passed in the request body. Optional for `GET`
requests.

    ForceUseSession true required

The `ForceUseSession` header forces the use of an existing session. You do not
need to use `AuthService.svc` in your request to the authentication service.

    BPMCSRF authentication_cookie_value required

Authentication cookie.

## Request body​

    field1, field2, ... required

The names of the fields passed in the request body.

    value1, value2, ... required

The values of the `field1, field2, ...` fields passed in the request body.

## HTTP status code​

    code

Response status code.

Status codes

| 200 OK | `GET`, `PUT`, `MERGE`, or `PATCH` request was completed successfully. The response body should contain the value of the object or properly specified in the request URL. | 201 Created | `POST` request created an object or a link successfully. The response body should contain the updated object. | 202 Accepted | Processing of the data update request has started but has not finished yet. The response body should contain the [`Location` header](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#thelocationheader) and the [`Retry-After` header](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#theretry-afterheader). The response body should be empty. The server should return the 303 response code with the [`Location` header](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#thelocationheader) that contains the final URL that can be used to retrieve the result. The body and the header of the final URL should be formatted similar to the initial data update request. | 204 No content | Data update request. The value of the requested resource is 0. The response body should be empty. | 3xx Redirection | Data update request. The redirection means the client must take further actions to execute the request. The response should contain the [`Location` header](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#thelocationheader) with the URL that can be used to retrieve the result. | 4xx Client Error | Incorrect requests. The server returns this code in response to client errors and requests to non-existent resources, such as entities, entity collections, or properties. If the response body is defined for the error code, the error body will be as defined for the corresponding [format](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#formats). | 404 Not Found | The object or collection specified in the URL does not exist. The response body should be empty. |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------------------------------------------------------------------------------------ |

## Response body​

    entry

The instance of the collection object.

    metadata_data

The properties of the collection object instance.

    object1 field1, object1 field2, ..., object2 field1, object2 field2, ...

The names of the `field1, field2, ...` fields in the `object1, object2, ...`
collection object instances.

    object1 field_value1, object1 field_value2, ..., object2 field_value1, object2 field_value2, ...

The values of the `field1, field2, ...` fields in the `object1, object2, ...`
collection object instances.

---

## Resources​

[Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest)

[OData 3 documentation (description of request headers)](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#headerfields)

[OData 3 documentation (description of request parameters)](https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/#requestingdata)

- Request string
- Request headers
- Request body
- HTTP status code
- Response body
- Resources
