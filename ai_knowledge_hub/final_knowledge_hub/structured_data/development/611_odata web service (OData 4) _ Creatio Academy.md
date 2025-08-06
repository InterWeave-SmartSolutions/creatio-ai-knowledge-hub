# odata web service (OData 4) | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 1413 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/data-services/odata/references/odata-odata-4

## Description

Depending on the request type, OData 4 protocol can return different data. Learn
more about the request and response structure below.

## Key Concepts

web service, odata, database, case

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

Depending on the request type, OData 4 protocol can return different data. Learn
more about the request and response structure below.

- Request structure
- Response structure

  // Request string.  
  method Creatio_application_address/0/odata/objects_collection(object_id)/object_field?$parameters

  // Request headers.  
  Accept: application/json  
  Content-Type: application/json; charset=utf-8; IEEE754Compatible=true  
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

  // Response body (available in GET and post requests).  
  {  
   "@odata.context":
  "https://Creatio_application_address/0/odata/$metadata#data_resource",  
   "value": [  {  "object1 field1": "object1 field_value1",  "object1 field2":
  "object1 field_value2",  ...  },  {  "object2 field1": "object2 field_value1",
   "object2 field2": "object2 field_value2",  ...  },  ...  ]  
  }

## Request string​

    method required

Creatio supports the following request methods:

- `GET` – retrieve data
- `POST` – add data
- `PATCH` – modify data
- `DELETE` – delete data

  Creatio_application_address required

Creatio application URL.

    odata required

OData 4 protocol's web service URL. Unmodifiable part of the request.

    objects_collection required

Name of the database table (the name of the object collection). Run the
[authentication](https://academy.creatio.com/documents?ver=8.0&id=15402) and
execute one of the requests to retrieve the list of database tables.

- JSON
- XML
- [SysSchema] table data

  // The result will be received in JSON.  
  GET Creatio_application_address/0/odata/

  // Request headers.  
  ForceUseSession: true  
  BPMCSRF: authentication_cookie_value

  // The result will be received in XML.  
  GET Creatio_application_address/0/odata/$metadata

  // Request headers.  
  ForceUseSession: true  
  BPMCSRF: authentication_cookie_value

  // The result will be received from the [SysSchema] database table in JSON.  
  GET Creatio_application_address/0/odata/SysSchema?$filter=ManagerName eq
  'EntitySchemaManager'

  // Request headers.  
  ForceUseSession: true  
  BPMCSRF: authentication_cookie_value

To **retrieve only the total number of records** by excluding the records
themselves from the response body, use the `$count` parameter directly in the
request string, not as a parameter.

- Request for .NET Framework
- Request for .NET Core and .NET 6

  https://mycreatio.com/0/odata/objects_collection/$count

  https://mycreatio.com/odata/objects_collection/$count

  object_id optional

Identifier of the database table record string (the identifier of the collection
object instance).

    object_field optional

Database table record field (the field of the collection object instance).

    parameters optional

Optional OData 4 parameters you can use in the `GET` Creatio request string. Use
the `?` operator to specify the parameters. Add the parameter name after the `$`
operator. Use the `&` operator to use two or more parameters.

Available values

| $value |     | The field value. | [$count](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptioncount) | `$count=true` | Whether to extend the response body with information about the total number of records in the selection. | `$count=true&$top=0` | Only the total number of records excluding the records themselves from the response body. The response structure is the same when the `$count` parameter is used with and without the `$top` parameter. For example, retrieve the total number of records when their number exceeds the limit. | [$skip](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionstopandskip) | `$skip=n` | The first n elements that must be excluded from the selection. | [$top](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionstopandskip) | `$top=n` | The first n elements that must be included in the selection. | [$select](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionselect) | `$select=field1,field2,...` | A set of fields that must be included in the selection. | [$orderby](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionorderby) | `$orderby=field asc` or `$orderby=field desc` | How to sort the field values in the selection. | [$expand](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionexpand) | `$expand=field1,field2,...` | Extension of the connected fields. | [$filter](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_SystemQueryOptionfilter) | `$filter=field template 'field_value'` | How to filter the fields in the selection. |
| ------ | --- | ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------ |

## Request headers​

    Accept application/json required

Data type to expect in the server response. Optional for `GET` requests.

    Content-Type application/json; charset=utf-8; IEEE754Compatible=true required

Encoding and type of the resource passed in the request body. Optional for `GET`
requests.

    ForceUseSession true required

`ForceUseSession` header forces the use of an existing session.

    BPMCSRF authentication_cookie_value required

Authentication cookie.

## Request body​

    field1, field2, ... required

The field names passed in the request body.

    value1, value2, ... required

Values of the `field1, field2, …` fields passed in the request body.

## HTTP status code​

    code

Response status code.

Status codes

| 200 OK | A request that does not create a resource was completed successfully, and the resource's value does not equal 0. In this case, the response body should contain the value of the resource specified in the request URL. The information in the response depends on the request method:`GET` – the resource was found and passed in the response body.`POST` – the resource with the description of server actions caused by the request was passed in the response body. | 201 Created | A request that creates a resource successfully. The response body should contain the created resource. Used for `POST` requests that [create a collection](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_CreateanEntity), [create a multimedia object](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_CreateaMediaEntity) (e. g., a photo), or [call an action through import](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_InvokinganAction). | 202 Accepted | Data request processing has started but has not finished yet. There is no guarantee that the request will be completed successfully ([asynchronous request processing](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_AsynchronousRequests)). | 204 No content | The request was processed successfully, but there is no need to return any data. The value of the requested resource is 0. The response will pass only the headers, the response body should be empty. | 3xx Redirection | Redirection means the client must take further actions to execute the request. The response should contain the `Location` header with the URL that can be used to retrieve the result. The response can also contain the `Retry-After` header that displays time, in seconds. The time specifies how long the client can wait before executing another request to the resource in the `Location` header. Learn more: [Location header](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderLocation), [Retry-After header](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderRetryAfter). | 304 Not modified | The client executes a `GET` request with the `If-None-Match` header, and the content remains unchanged. The response should not contain any other headers. Learn more: [If-None-Match header](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderIfNoneMatch). | 403 Forbidden | The request is correct, but the server refused to authorize it. This means the client lacks permissions to work with the resource. This may be caused by an invalid `BPMCSRF` cookie. | 404 Not Found | The server cannot find the resource specified in the URL. The response body may contain additional information. | 405 Method Not Allowed | The resource specified in the request URL does not support the specified request method. The response should contain the `Allow` header with the list of request methods the resource supports. | 406 Not Acceptable | The resource specified in the request URL does not have any current view that is acceptable for the client as per `Accept`, `Accept-Charset`, and `Accept-Language` request headers. The service does not provide a default view. Learn more: [Accept](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderAccept), [Accept-Charset](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderAcceptCharset), [Accept-Language](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderAcceptLanguage) request headers. | 410 Gone | The requested resource is no longer available. The resource had used the specified URL but was deleted and is no longer available. | 412 Prediction Failed | The client specified a request header condition the resource cannot process. | 424 Failed Dependency | The current request cannot be processed because the requested action depends on another action that could not be executed. The request has not been executed due to dependency failure. | 501 Not Implemented | The client is using a request method that is not implemented in OData 4 protocol and cannot be processed. The response body should contain the description of the unimplemented functionality. |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## Response body​

    @odata.context

Information about the type of the returned data. Besides the data source path,
the `data_resource` element can contain the `$entity` parameter. This parameter
indicates that the response returned a single instance of the collection object.
Available only for `GET` and `POST` requests.

    value

Contains the object collection. Not available if the response contains a single
collection object instance. Available only for `GET` requests.

    []

Object collection. Available only for `GET` requests.

    {}

Collection object instances. Available only for `GET` and `POST` requests.

    object1 field1, object1 field2, ..., object2 field1, object2 field2, ...

The names of the `field1, field2, …` fields in the `object1, object2, …`
collection object instances. Available only for `GET` and `POST` requests.

    object1 field_value1, object1 field_value2, ..., object2 field_value1, object2 field_value2, ...

The values of the `field1, field2, …` fields in the `object1, object2, …`
collection object instances. Available only for `GET` and `POST` requests.

---

## Resources​

[Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest)

[OData 4 documentation (description of request headers)](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_HeaderFields)

[OData 4 documentation (description of request parameters)](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#_Toc31360954)

- Request string
- Request headers
- Request body
- HTTP status code
- Response body
- Resources
