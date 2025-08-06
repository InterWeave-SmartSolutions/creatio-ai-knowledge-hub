# Service that runs business processes | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 2173
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/integrations-and-api/business-process-service/overview

## Description

ProcessEngineService.svc is a web service implemented in the Creatio service
model to run business processes. Use the web service to integrate external apps
with Creatio.

## Key Concepts

business process, configuration, web service, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: advanced

`ProcessEngineService.svc` is a web service implemented in the Creatio service
model to run business processes. Use the web service to integrate external apps
with Creatio.

## Run a business process from an external app​

Use the `CreatioURL/0/ServiceModel/ProcessEngineService.svc` URL to access
Creatio objects. For example,
`https://mycreatio.com/0/ServiceModel/ProcessEngineService.svc`.

The `Terrasoft.Core.Service.Model.ProcessEngineService` class implements the
`ProcessEngineService.svc` functionality. View the primary methods of the
`ProcessEngineService.svc` service in the table below.

| Method | Description | Execute() | Runs a business process. Passes a key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. Returns the process execution result. | ExecProcElByUId() | Executes a specific business process element. Can only execute an element of a running process. |
| ------ | ----------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------- |

View the full list of the methods in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.ServiceModel.ProcessEngineService.html).

## Run a business process from the front-end​

Creatio lets you run a business process from the front-end using the following
ways:

- `executeProcess()` method of the `ProcessModuleUtilities` module in the
  `CrtNUI` package
- `execute()` method of the `Terrasoft.process.RunProcessRequest` class
- `ProcessEngineService` service of the `@creatio-devkit/common` library. Learn
  more:
  [Interact with business processes using a request handler](https://academy.creatio.com/documents?ver=8.3&id=15186).

### Run a business process using the executeProcess() method​

1. **Create the Client module schema type** if needed. Instructions:
   [Configuration elements of the Client module type](https://academy.creatio.com/documents?ver=8.3&id=15106).

2. **Add the** `ProcessModuleUtilities` **module as a dependency** to the module
   of the page that calls the service.

3. **Implement the** `executeProcess()` **method**. Set the `args` object as a
   parameter.

4. **Pass the method parameters** listed in the table below.

| Parameter | Parameter type | sysProcessName | Name (the `Code` property value) of the business process to run. Optional if the `sysProcessId` parameter is used. | sysProcessId | The ID of the business process to run. Optional if the `sysProcessName` parameter is used. | parameters | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. |
| --------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |

5. **Call the** `executeProcess()` **method**.

### Run a business process using the execute() method​

1. **Create the Client module schema type** if needed. Instructions:
   [Configuration elements of the Client module type](https://academy.creatio.com/documents?ver=8.3&id=15106).

2. **Create the** `RunProcessRequest` **class**.

3. **Pass the method parameters and list of output parameters** listed in the
   table below.

| Parameter | Parameter type | schemaName | Name (the `Code` property value) of the business process to run. | schemaUId | The ID of the business process to run. | parameters | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. | resultParameterNames | Collection of output business process parameters whose values must be received when executing the process. Pass as an array. |
| --------- | -------------- | ---------- | ---------------------------------------------------------------- | --------- | -------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |

4. **Call the** `execute()` **method**.

## Run a business process from the back-end​

To run a business process from the back-end, call the `Execute()` method of the
`Terrasoft.Core.Process.IProcessExecutor` interface. The `IProcessExecutor`
interface provides a set of the `Execute()` method overloads for solving custom
tasks. View the description of the `IProcessExecutor` interface in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Process.IProcessExecutor.html).

note

Creatio forbids running the business process that has output parameters in the
background.

### Run a business process that passes or receives parameters​

View a list of ways to run a business process that passes or receives parameters
from the back-end in the table below.

| Method | Description | Execute(string processSchemaName)Parameters | processSchemaName | Name (the `Code` property value) of the business process to run. |
| ------ | ----------- | ------------------------------------------- | ----------------- | ---------------------------------------------------------------- |

| Runs a business process using the process name (the `Code` property value). | Execute(Guid processSchemaUId)Parameters | processSchemaUId | The ID of the business process to run. |
| --------------------------------------------------------------------------- | ---------------------------------------- | ---------------- | -------------------------------------- |

Runs a business process using the process ID.

View the example that runs a business process using the process name below.

Example that runs a business process using the process name

    UserConnection userConnection = Get<UserConnection>("UserConnection");
    IProcessEngine processEngine = userConnection.ProcessEngine;
    IProcessExecutor processExecutor = processEngine.ProcessExecutor;
    processExecutor.Execute("UsrProcess2Custom1");
    return true;

### Run a business process that passes input parameters​

View a list of ways to run a business process that passes input parameters from
the back-end in the table below.

| Method | Description | Execute(string processSchemaName, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaName | Name (the `Code` property value) of the business process to run. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. |
| ------ | ----------- | ------------------------------------------------------------------------------------------------ | ----------------- | ---------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |

| Runs a business process using the process name (the `Code` property value). | Execute(Guid processSchemaUId, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaUId | The ID of the business process to run. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |

Runs a business process using the process ID.

View the examples that run a business process below.

- Transfer an integer parameter value
- Transfer a parameter value of the value collection type
- Transfer a parameter value of the object collection type with attributes

  UserConnection userConnection = Get<UserConnection>("UserConnection");  
  IProcessEngine processEngine = userConnection.ProcessEngine;  
  IProcessExecutor processExecutor = processEngine.ProcessExecutor;  
  var nameValues = new Dictionary<string, string>();  
  int parameter1Value = 100;  
  nameValues["parameter1"] = parameter1Value.ToString();  
  processExecutor.Execute("UsrProcess3Custom1", nameValues);  
  return true;

  UserConnection userConnection = Get<UserConnection>("UserConnection");  
  IProcessEngine processEngine = userConnection.ProcessEngine;  
  IProcessExecutor processExecutor = processEngine.ProcessExecutor;  
  ObjectList<int> values = ObjectList.Create(1, 2, 3, 4);  
  string serializedValue =
  BaseSerializableObjectUtilities.SerializeToJson(values);  
  var parameterNameValues = new Dictionary<string, string>();  
  parameterNameValues["InputValueList"] = serializedValue;  
  processExecutor.Execute("ProcessRunsFromScriptTask", parameterNameValues);  
  return true;

  UserConnection userConnection = Get<UserConnection>("UserConnection");  
  IProcessEngine processEngine = userConnection.ProcessEngine;  
  IProcessExecutor processExecutor = processEngine.ProcessExecutor;

  /_ Create an object collection. _/  
  var list = new CompositeObjectList<CompositeObject>();  
  var item1 = new CompositeObject();

  /_ The process parameter object includes "Id" and "Name" columns. _/  
  item1["Id"] = new Guid("94cc536a-71a7-4bfb-87ca-13f53b23c28e");  
  item1["Name"] = "Name1"; list.Add(item1);  
  var item2 = new CompositeObject(); item2["Id"] = new
  Guid("e694d36e-1727-4276-9fbf-b9aa193e4f44");  
  item2["Name"] = "Name2";  
  list.Add(item2);  
  string serializedValue =
  BaseSerializableObjectUtilities.SerializeToJson(list);  
  var parameterNameValues = new Dictionary<string, string>();  
  parameterNameValues["InputObjectList"] = serializedValue;  
  processExecutor.Execute("ProcessRunsFromScriptTask", parameterNameValues);  
  return true;

### Run a business process that receives a single output parameter​

View a list of ways to run a business process that receives a single output
parameter from the back-end in the table below.

| Method | Description | Execute<TResult>(string processSchemaName, string resultParameterName, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaName | Name (the `Code` property value) of the business process to run. | resultParameterName | Name of the output business process parameter. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. Optional. |
| ------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------- | ------------------- | ---------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| Runs a business process using the process name (the `Code` property value). | Execute<TResult>(Guid processSchemaUId, string resultParameterName, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaUId | The ID of the business process to run. | resultParameterName | Name of the output business process parameter. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. Optional. |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------- | -------------------------------------- | ------------------- | ---------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Runs a business process using the process ID.

View the examples that run a business process using different ways below.

Run a business process that receives a single output parameter

    UserConnection userConnection = GetUserConnection();
    IProcessExecutor processExecutor = userConnection.ProcessEngine.ProcessExecutor;

    /* Key-value collection of input business process parameters where key is the parameter code (the "Code" property value) and the value is the parameter value. */
    var inputParameters = new Dictionary<string, string> {
        ["SomeInputParameter1"] = "SomeInputParameter1Value",
        ["SomeInputParameter2"] = "SomeInputParameter2Value"
    };
    string processSchemaName = "SomeBusinessProcessCode";
    Guid processSchemaUId = Guid.Parse("00000000-0000-0000-0000-000000000000");

    /* Run a business process using the process name. Returns the text value of the "SomeOutputParameter3" parameter. */
    string resultValue = processExecutor.Execute<string>(processSchemaName, "SomeOutputParameter3");

    /* Run a business process using the process ID. Returns the text value of the "SomeOutputParameter3" parameter. */
    string resultValue = processExecutor.Execute<string>(processSchemaName, "SomeOutputParameter3");

    /* Run a business process using the process name and collection of input process parameters. Returns the text value of the "SomeOutputParameter3" parameter. */
    string resultValue = processExecutor.Execute<string>(processSchemaName, "SomeOutputParameter3", inputParameters);

    /* Run a business process using the process ID and collection of input process parameters. Returns the text value of the "SomeOutputParameter3" parameter. */
    string resultValue = processExecutor.Execute<string>(processSchemaUId, "SomeOutputParameter3", inputParameters);

### Run a business process that receives a collection of output parameters​

View a list of ways to run a business process receives a collection of output
parameters from the back-end in the table below.

| Method | Description | Execute<TResult>(string processSchemaName, IEnumerable<string> resultParameterNames, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaName | Name (the `Code` property value) of the business process to run. | resultParameterNames | Collection of output business process parameters. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. Optional. |
| ------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------- | -------------------- | ------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| Runs a business process using the process name (the `Code` property value). | Execute<TResult>(Guid processSchemaUId, IEnumerable<string> resultParameterNames, IReadOnlyDictionary<string, string> parameterValues)Parameters | processSchemaUId | The ID of the business process to run. | resultParameterNames | Collection of output business process parameters. | parameterValues | Key-value collection of input business process parameters where key is the parameter code (the `Code` property value) and the value is the parameter value. Optional. |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- | -------------------------------------- | -------------------- | ------------------------------------------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

Runs a business process using the process ID.

View the examples that run a business process using different ways below.

Example that runs a business process that receives a collection of output
parameters

    UserConnection userConnection = GetUserConnection();
    IProcessExecutor processExecutor = userConnection.ProcessEngine.ProcessExecutor;

    /* Key-value collection of input business process parameters where key is the parameter code (the "Code" property value) and the value is the parameter value.*/
    var inputParameters = new Dictionary<string, string> {
        ["SomeInputParameter1"] = "SomeInputParameter1Value",
        ["SomeInputParameter2"] = "SomeInputParameter2Value"
    };

    /* Collection of output business process parameters.*/
    var resultParameterNames = new string[] {
        "SomeOutputParameter1",
        "SomeOutputParameter2"
    };
    string processSchemaName = "SomeBusinessProcessCode";
    Guid processSchemaUId = Guid.Parse("00000000-0000-0000-0000-000000000000");

    /* Run a business process using the process name and collection of output process parameters. */
    ProcessDescriptor processDescriptor = processExecutor.Execute(processSchemaName, resultParameterNames);

    /* Run a business process using the process ID and collection of output process parameters. */
    ProcessDescriptor processDescriptor = processExecutor.Execute(processSchemaName, resultParameterNames);

    /* Run a business process using the process name and collections of input and output process parameters. */
    ProcessDescriptor processDescriptor = processExecutor.Execute(processSchemaName, inputParameters, resultParameterNames);

    /* Run a business process using the process ID and collections of input and output process parameters. */
    ProcessDescriptor processDescriptor = processExecutor.Execute(processSchemaUId, inputParameters, resultParameterNames);

Running a business process that receives a collection of output parameters
returns an object of the `ProcessDescriptor` type. View the description of the
`ProcessDescriptor` class in the
[.NET classes reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Process.ProcessDescriptor.html).

To **receive the values of output parameters** , use the `ResultParameterValues`
property of the `IReadOnlyDictionary<string, object>` type in the
`Terrasoft.Core.Process.ProcessDescriptor` class.

View the example that receives the output parameter values below.

Example that receives the output parameter values

    ProcessDescriptor processDescriptor = processExecutor.Execute("processSchemaName", inputParameters, resultParameterNames);
    object parameter3Value = processDescriptor.ResultParameterValues["SomeOutputParameter3"];
    if (processDescriptor.ResultParameterValues.TryGetValue("SomeOutputParameter4", out object parameter4value)) {
        Console.Log(parameter4value);
    }

---

## See also​

[Interact with business processes using a request handler](https://academy.creatio.com/documents?ver=8.3&id=15186)

---

## Resources​

[Terrasoft.Core.Service.Model.ProcessEngineService class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.ServiceModel.ProcessEngineService.html)
(.NET classes reference)

[Terrasoft.Core.Process.IProcessExecutor interface](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Process.IProcessExecutor.html)
(.NET classes reference)

[Terrasoft.Core.Process.ProcessDescriptor class](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Core.Process.ProcessDescriptor.html)
(.NET classes reference)

- Run a business process from an external app
- Run a business process from the front-end
  - Run a business process using the executeProcess() method
  - Run a business process using the execute() method
- Run a business process from the back-end
  - Run a business process that passes or receives parameters
  - Run a business process that passes input parameters
  - Run a business process that receives a single output parameter
  - Run a business process that receives a collection of output parameters
- See also
- Resources
