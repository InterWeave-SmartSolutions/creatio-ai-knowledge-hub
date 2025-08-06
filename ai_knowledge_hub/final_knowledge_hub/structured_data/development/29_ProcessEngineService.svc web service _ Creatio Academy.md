# ProcessEngineService.svc web service | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 559
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.2/integrations-and-api/business-process-service/references/processengineservice-svc

## Description

Request string

## Key Concepts

business process, configuration, section, web service

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/business-process-service/references/processengineservice-svc)**
(8.3).

Version: 8.2

On this page

Level: advanced

- Request structure
- Response structure for the Execute() method

  /_ Request string. _/  
  GET Creatio_application_address/0/ServiceModel/ProcessEngineService.svc/[processSchemaName/]methodName[?ResultParameterName=resultParameterName&inputParameter=inputParameterValue][/processElementUID]

  /_ Request headers. _/  
  ForceUseSession: true  
  BPMCSRF: authentication_cookie_value

  /_ Status code. _/  
  Status: code

  /_ Response body. _/  
  <string xmlns="https://schemas.microsoft.com/2003/10/Serialization/">  
   "[  {\"Id\":\"object1_id\",\"object1 field1\":\"object1
  field_value1\",\"object1 field2\":\"object1 field_value2\"},
  {\"Id\":\"object2_id\",\"object2 field1\":\"object2 field_value1\",\"object2
  field2\":\"object2 field_value2\"},  ... {},  ]"  
  </string>

## Request string​

    GET

Method of the request to run business processes. Required.

    Creatio_application_address

Creatio instance URL. Required.

    ServiceModel

The path to the service that runs business processes. Unmodifiable part of the
request. Required.

    ProcessEngineService.svc

The address of the web service that runs business processes. Unmodifiable part
of the request. Required.

    methodName

The method of the web service that runs business processes. Required.

Primary **methods** :

- `Execute()`. Runs a business process. Lets you pass a set of incoming
  parameters and return the outcome of the web service execution.
- `ExecProcElByUId()`. Executes a specific business process element. You can
  only execute an element of the running process. If Creatio has already
  executed the process element by the time the method is called, the element is
  not executed again.

  ProcessSchemaName optional

Applicable for the `Execute()` method.

The name of the business process schema. You can find the name of the business
process schema in the **Configuration** section.

    ResultParameterName optional

Applicable for the `Execute()` method.

The variable of the process parameter code. Unmodifiable part of the request.

    resultParameterName optional

Applicable for the `Execute()` method.

The code of the process parameter that stores the outcome of the process
execution. If you omit this parameter, the web service runs the business process
without waiting for the outcome of the process execution. If the process lacks
the parameter code, the web service returns `null`.

    inputParameter optional

Applicable for the `Execute()` method.

The variable of the incoming process parameter code. If you pass multiple
incoming parameters, combine them using the `&` character.

    inputParameterValue optional

Applicable for the `Execute()` method.

The values of the incoming process parameters.

    ProcessElementUID optional

Applicable for the `ExecProcElByUId()` method.

The ID of the process element to run.

## Request headers​

    ForceUseSession true

Forced use of an existing session. Required.

    BPMCSRF authentication_cookie_value

The authentication cookie. Required.

## Response body​

    []

The object collection.

    {}

The collection object instances.

    Id

The name of the **Id** field.

    object1_id, object2_id, ...

The IDs of the collection object instances.

    object1 field1, object1 field2, ..., object2 field1, object2 field2, ...

The names of the `field1, field2, ...` fields in the `object1, object2, ...`
collection object instances.

    object1 field_value1, object1 field_value2, ..., object2 field_value1, object2 field_value2, ...

The values of the `field1, field2, ...` fields in the `object1, object2, ...`
collection object instances. Available only for `GET` and `POST` requests.

- Request string
- Request headers
- Response body
