# Batch request examples | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 2051 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/data-services/odata/examples/batch-request-examples

## Description

Batch requests combine multiple HTTP requests by specifying each request as a
separate object in the batch request's body. The Creatio database server returns
a single HTTP response that contains the responses to each request. Use batch
requests to improve Creatio performance.

## Key Concepts

odata, database

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

**Batch requests** combine multiple HTTP requests by specifying each request as
a separate object in the batch request's body. The Creatio database server
returns a single HTTP response that contains the responses to each request. Use
batch requests to improve Creatio performance.

The batch requests utilize:

- The `POST` HTTP method.
- The
  [$batch](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html#sec_AddressingtheBatchEndpointforaServic)
  parameter.
- The `Content-Type` header.

The **values** of the `Content-Type` header:

- `application/json` – restricts the content the server returns for each request
  within the batch request to a single type.
- `multipart/mixed` – allows you to set unique `Content-Type` headers for each
  request in the batch request body.

If one of the requests completes with a 4xx-5xx group response code, the
subsequent requests will not be executed. Add the
[Prefer:](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_Preferencecontinueonerrorodatacontin)
`continue-on-error` header to the main HTTP request to enable the execution of
the subsequent requests.

Important

A batch request can contain up to 100 requests.

## Batch request (Content-Type: application/json)​

- Batch request
- Response

  POST https://mycreatio.com/0/odata/$batch

  Content-Type: application/json; odata=verbose; IEEE754Compatible=true  
  Accept: application/json  
  BPMCSRF: OpK/NuJJ1w/SQxmPvwNvfO  
  ForceUseSession: true

  {  
   "requests": [  {  // Add an object instance to the City collection.
  "method": "POST",  "url": "City",  "id": "t3",  "body": {  // Add the Burbank
  value to the Name field.  "Name": "Burbank"  },  "headers": {  "Content-Type":
  "application/json;odata=verbose",  "Accept": "application/json;odata=verbose",
   "Prefer": "continue-on-error"  }  },  {  // Add an object instance to the
  City collection.  "method": "POST",  "atomicityGroup": "g1",  "url": "City",
  "id": "t3",  "body": {  // Add the 62f9bc01-57cf-4cc7-90bf-8672acc922e3 value
  to the Id field.  "Id": "62f9bc01-57cf-4cc7-90bf-8672acc922e3",  // Add the
  Spokane value to the Name field.  "Name": "Spokane"  },  "headers": {
  "Content-Type": "application/json;odata=verbose",  "Accept":
  "application/json;odata=verbose",  "Prefer": "continue-on-error"  }  },  {  //
  Update the 62f9bc01-57cf-4cc7-90bf-8672acc922e3 id object instance in the City
  collection.  "method": "PATCH",  "atomicityGroup": "g1",  "url":
  "City/62f9bc01-57cf-4cc7-90bf-8672acc922e3",  "id": "t2",  "body": {  //
  Change the value of the Name field to Texas.  "Name": "Texas"  },  "headers":
  {  "Content-Type": "application/json;odata=verbose",  "Accept":
  "application/json;odata=verbose",  "Prefer": "continue-on-error"  }  }  ]  
  }

  Status: 200 OK

  {  
   "responses": [  {  "id": "t3",  "status": 201,  "headers": {  "location":
  "https://mycreatio.com/0/odata/City(b6a05348-55b1-4314-a228-436ba305d2f3)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "b6a05348-55b1-4314-a228-436ba305d2f3",  "CreatedOn":
  "2020-05-18T17:50:39.2838673Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T17:50:39.2838673Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Burbank",  "Description":
  "",  "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  },  {
  "id": "t3",  "atomicityGroup": "c59e36b2-2aa9-44fa-86d3-e7d68eecbfa0",
  "status": 201,  "headers": {  "location":
  "https://mycreatio.com/0/odata/City(62f9bc01-57cf-4cc7-90bf-8672acc922e3)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "62f9bc01-57cf-4cc7-90bf-8672acc922e3",  "CreatedOn":
  "2020-05-18T17:50:39.361994Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T17:50:39.361994Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Spokane",  "Description":
  "",  "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  },  {
  "id": "t2",  "atomicityGroup": "c59e36b2-2aa9-44fa-86d3-e7d68eecbfa0",
  "status": 204,  "headers": {  "odata-version": "4.0"  }  }  ]  
  }

## Batch request (Content-Type: application/json and Prefer: continue-on-error)​

- Batch request
- Response

  POST https://mycreatio.com/0/odata/$batch

  Content-Type: application/json; odata=verbose; IEEE754Compatible=true  
  Accept: application/json  
  BPMCSRF: OpK/NuJJ1w/SQxmPvwNvfO  
  ForceUseSession: true  
  Prefer: continue-on-error

  {  
   "requests": [  {  // Add an object instance to the City collection.
  "method": "POST",  "url": "City",  "id": "t3",  "body": {  // Add the Burbank
  value to the Name field.  "Name": "Burbank"  },  "headers": {  "Content-Type":
  "application/json;odata=verbose",  "Accept": "application/json;odata=verbose",
   "Prefer": "continue-on-error"  }  },  {  // Update the
  62f9bc01-57cf-4cc7-90bf-8672acc922e3 id object instance in the City
  collection.  "method": "PATCH",  "atomicityGroup": "g1",  "url":
  "City/62f9bc01-57cf-4cc7-90bf-8672acc922e2",  "id": "t2",  "body": {  //
  Change the value of the Name field to Indiana.  "Name": "Indiana"  },
  "headers": {  "Content-Type": "application/json;odata=verbose",  "Accept":
  "application/json;odata=verbose",  "Prefer": "continue-on-error"  }  },  {  //
  Add an object instance to the City collection.  "method": "POST",
  "atomicityGroup": "g1",  "url": "City",  "id": "t3",  "body": {  // Write the
  62f9bc01-57cf-4cc7-90bf-8672acc922a1 value to the Id field.  "Id":
  "62f9bc01-57cf-4cc7-90bf-8672acc922a1",  // Write the Iowa value to the Name
  field.  "Name": "Iowa"  },  "headers": {  "Content-Type":
  "application/json;odata=verbose",  "Accept": "application/json;odata=verbose",
   "Prefer": "continue-on-error"  }  }  ]  
  }

  Status: 200 OK

  {  
   "responses": [  {  "id": "t3",  "status": 201,  "headers": {  "location":
  "https://mycreatio.com/0/odata/City(2f5e68f8-38bd-43c1-8e15-a2f13b0aa56a)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "2f5e68f8-38bd-43c1-8e15-a2f13b0aa56a",  "CreatedOn":
  "2020-05-18T18:06:50.7329808Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T18:06:50.7329808Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Burbank",  "Description":
  "",  "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  },  {
  "id": "t2",  "atomicityGroup": "0c1c4019-b9fb-4fb3-8642-2d0660c4551a",
  "status": 204,  "headers": {  "odata-version": "4.0"  }  },  {  "id": "t3",
  "atomicityGroup": "0c1c4019-b9fb-4fb3-8642-2d0660c4551a",  "status": 201,
  "headers": {  "location":
  "https://mycreatio.com/0/odata/City(62f9bc01-57cf-4cc7-90bf-8672acc922a1)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "62f9bc01-57cf-4cc7-90bf-8672acc922a1",  "CreatedOn":
  "2020-05-18T18:06:50.7954775Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T18:06:50.7954775Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Iowa",  "Description": "",
  "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  }  ]  
  }

## Batch request (Content-Type: multipart/mixed)​

- Batch request
- Response

  POST https://mycreatio.com/0/odata/$batch

  Content-Type: multipart/mixed;boundary=batch_a685-9724-d873;
  IEEE754Compatible=true  
  BPMCSRF: OpK/NuJJ1w/SQxmPvwNvfO  
  ForceUseSession: true

  --batch_a685-9724-d873  
  Content-Type: multipart/mixed; boundary=changeset_06da-d998-8e7e

  --changeset_06da-d998-8e7e  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary

  // Add an object instance to the City collection.  
  POST City HTTP/1.1  
  Content-ID: 1  
  Accept: application/atomsvc+xml;q=0.8, application/json;odata=verbose;q=0.5,
  _/_;q=0.1  
  Content-Type: application/json;odata=verbose

  // Write the Gilbert value to the Name field.  
  {"Name": "Gilbert"}

  --changeset_06da-d998-8e7e  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary

  // Update the 62f9bc01-57cf-4cc7-90bf-8672acc922e2 id object instance in the
  City collection.  
  PATCH City/62f9bc01-57cf-4cc7-90bf-8672acc922e2 HTTP/1.1  
  Content-ID: 2  
  Accept: application/atomsvc+xml;q=0.8, application/json;odata=verbose;q=0.5,
  _/_;q=0.1  
  Content-Type: application/json;odata=verbose

  // Change the value of the Name field to Lincoln.  
  {"Name": "Lincoln"}

  --changeset_06da-d998-8e7e  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary

  // Delete the 62f9bc01-57cf-4cc7-90bf-8672acc922e2 id object instance from the
  City collection.  
  DELETE City/62f9bc01-57cf-4cc7-90bf-8672acc922e2 HTTP/1.1  
  Content-ID: 3  
  Accept: application/atomsvc+xml;q=0.8, application/json;odata=verbose;q=0.5,
  _/_;q=0.1  
  Content-Type: application/json;odata=verbose

  Status: 200 OK

  --batchresponse_e17aace9-5cbb-49bd-b7ad-f1be8cc8c9d8  
  Content-Type: multipart/mixed;
  boundary=changesetresponse_a08c1df6-4b82-4a9b-be61-7ef4cc7b23ba

  --changesetresponse_a08c1df6-4b82-4a9b-be61-7ef4cc7b23ba  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary  
  Content-ID: 1

  HTTP/1.1 201 Created  
  Location: https://mycreatio.com/0/odata/City(fbd0565f-fa8a-4214-ae89-c976c5f3acb4)  
  Content-Type:
  application/json; odata.metadata=minimal  
  OData-Version: 4.0

  {  
   "@odata.context": "https://mycreatio.com/0/odata/$metadata#City/$entity",  
   "Id": "fbd0565f-fa8a-4214-ae89-c976c5f3acb4",  
   "CreatedOn": "2020-05-18T18:41:57.0917235Z",  
   "CreatedById": "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  
   "ModifiedOn": "2020-05-18T18:41:57.0917235Z",  
   "ModifiedById": "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  
   "Name": "Gilbert",  
   "Description": "",  
   "CountryId": "00000000-0000-0000-0000-000000000000",  
   "RegionId": "00000000-0000-0000-0000-000000000000",  
   "TimeZoneId": "00000000-0000-0000-0000-000000000000",  
   "ProcessListeners": 0  
  }  
  --changesetresponse_a08c1df6-4b82-4a9b-be61-7ef4cc7b23ba  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary  
  Content-ID: 2

  HTTP/1.1 204 No Content  
  OData-Version: 4.0

  --changesetresponse_a08c1df6-4b82-4a9b-be61-7ef4cc7b23ba  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary  
  Content-ID: 3

  HTTP/1.1 204 No Content

  --changesetresponse_a08c1df6-4b82-4a9b-be61-7ef4cc7b23ba--  
  --batchresponse_e17aace9-5cbb-49bd-b7ad-f1be8cc8c9d8--

## Batch request (Content-Type: multipart/mixed and different sets of requests)​

- Batch request
- Response

  POST https://mycreatio.com/0/odata/$batch

  Content-Type: multipart/mixed;boundary=batch_a685-9724-d873;
  IEEE754Compatible=true  
  Accept: application/json  
  BPMCSRF: OpK/NuJJ1w/SQxmPvwNvfO  
  ForceUseSession: true

  --batch_a685-9724-d873  
  Content-Type: multipart/mixed; boundary=changeset_06da-d998-8e7e

  --changeset_06da-d998-8e7e  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary

  // Add an object instance to the City collection.  
  POST City HTTP/1.1  
  Content-ID: 1  
  Accept: application/atomsvc+xml;q=0.8, application/json;odata=verbose;q=0.5,
  _/_;q=0.1  
  Content-Type: application/json;odata=verbose

  // Write the d6bc67b1-9943-4e47-9aaf-91bf83e9c285 value to the Id field.  
  // Write the Nebraska value to the Name field.  
  {"Id": "d6bc67b1-9943-4e47-9aaf-91bf83e9c285", "Name": "Nebraska"}

  --batch_a685-9724-d873  
  Content-Type: multipart/mixed; boundary=changeset_06da-d998-8e71

  --changeset_06da-d998-8e71  
  Content-Type: application/http  
  Content-Transfer-Encoding: binary

  // Add an object instance to the City collection.  
  POST City HTTP/1.1  
  Content-ID: 2  
  Accept: application/atomsvc+xml;q=0.8, application/json;odata=verbose;q=0.5,
  _/_;q=0.1  
  Content-Type: application/json;odata=verbose

  // Write the d6bc67b1-9943-4e47-9aaf-91bf83e9c286 value to the Id field.  
  // Add the Durham value to the Name field.  
  {"Id": "d6bc67b1-9943-4e47-9aaf-91bf83e9c286", "Name": "Durham"}

  Status: 200 OK

  {  
   "responses": [  {  "id": "1",  "atomicityGroup":
  "e9621f72-42bd-47c1-b271-1027e4b68e3b",  "status": 201,  "headers": {
  "location":
  "https://mycreatio.com/0/odata/City(d6bc67b1-9943-4e47-9aaf-91bf83e9c285)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "d6bc67b1-9943-4e47-9aaf-91bf83e9c285",  "CreatedOn":
  "2020-05-18T18:49:16.3766324Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T18:49:16.3766324Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Nebraska",  "Description":
  "",  "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  },  {
  "id": "2",  "atomicityGroup": "960e2272-d8cb-4b4d-827c-0181485dd71d",
  "status": 201,  "headers": {  "location":
  "https://mycreatio.com/0/odata/City(d6bc67b1-9943-4e47-9aaf-91bf83e9c286)",
  "content-type": "application/json; odata.metadata=minimal",  "odata-version":
  "4.0"  },  "body": {  "@odata.context":
  "https://mycreatio.com/0/odata/$metadata#City/$entity",  "Id":
  "d6bc67b1-9943-4e47-9aaf-91bf83e9c286",  "CreatedOn":
  "2020-05-18T18:49:16.4078852Z",  "CreatedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "ModifiedOn":
  "2020-05-18T18:49:16.4078852Z",  "ModifiedById":
  "dad159f3-6c2d-446a-98d2-0f4d26662bbe",  "Name": "Durham",  "Description": "",
   "CountryId": "00000000-0000-0000-0000-000000000000",  "RegionId":
  "00000000-0000-0000-0000-000000000000",  "TimeZoneId":
  "00000000-0000-0000-0000-000000000000",  "ProcessListeners": 0  }  }  ]  
  }

---

## Resources​

[Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest)

- Batch request (Content-Type: application/json)
- Batch request (Content-Type: application/json and Prefer: continue-on-error)
- Batch request (Content-Type: multipart/mixed)
- Batch request (Content-Type: multipart/mixed and different sets of requests)
- Resources
