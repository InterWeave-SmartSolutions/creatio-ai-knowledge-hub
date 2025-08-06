# Register a background operation | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 773 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/data-operations-back-end/execute-operations-in-the-background/examples/register-a-background-operation

## Description

Create a business process that registers a background operation. The background
operation takes approximately 30 seconds. After this time passes, the process
must add an Activity created by background task record to the list view of the
Activities section list.

## Key Concepts

business process, configuration, section, operation, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: intermediate

Example

Create a business process that registers a background operation. The background
operation takes approximately 30 seconds. After this time passes, the process
must add an **Activity created by background task** record to the list view of
the **Activities** section list.

## 1\. Create a class for the activity object​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.3&id=15121) to add the
   schema.

2. Click **Add** → **Source code** on the section list toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateSourceCodeSchema(7.17)/scr_add_schema.png>)

3. Go to the Schema Designer and fill out the schema properties:
   - Set **Code** to "UsrActivityData."
   - Set **Title** to "ActivityData."

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_ActivityData_Settings.png)

Click **Apply** to apply the properties.

4. Add the source code in the Schema Designer.

UsrActivityData

         namespace Terrasoft.Configuration {
             using System;
             using Terrasoft.Common;
             using Terrasoft.Core;
             using Terrasoft.Core.DB;
             public class UsrActivityData {
                 public string Title {
                     get;
                     set;
                 }
                 public Guid TypeId {
                     get;
                     set;
                 }
             }
         }


5. **Publish the schema**.

## 2\. Create a class that adds an activity​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.3&id=15121) to add the
   schema.

2. Click **Add** → **Source code** on the section list toolbar.

![](<https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateSourceCodeSchema(7.17)/scr_add_schema.png>)

3. Go to the Schema Designer and fill out the schema properties:
   - Set **Code** to "UsrBackgroundActivityCreator."
   - Set **Title** to "BackgroundActivityCreator."

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_BackgroundActivityCreator_Settings.png)

Click **Apply** to apply the properties.

4. Add the source code in the Schema Designer.

UsrBackgroundActivityCreator

         namespace Terrasoft.Configuration {
             using System;
             using Terrasoft.Common;
             using Terrasoft.Core;
             using Terrasoft.Core.DB;
             using Terrasoft.Core.Tasks;
             using System.Threading.Tasks;

             public class UsrBackgroundActivityCreator: IBackgroundTask <UsrActivityData> , IUserConnectionRequired {
                 private UserConnection _userConnection;

                 /* Implement the Run method of the IBackgroundTask interface. */
                 public void Run(UsrActivityData data) {
                     /* Forced 30 second delay. */
                     System.Threading.Tasks.Task.Delay(TimeSpan.FromSeconds(30));
                     /* Create an activity. */
                     var activity = new Activity(_userConnection) {
                         UseAdminRights = false,
                             Id = Guid.NewGuid(),
                             TypeId = data.TypeId,
                             Title = data.Title,

                             /* Set the activity category to "To do." */
                             ActivityCategoryId = new Guid("F51C4643-58E6-DF11-971B-001D60E938C6")
                     };
                     activity.SetDefColumnValues();
                     activity.Save(false);
                 }

                 /* Implement the SetUserConnection method of the IUserConnectionRequired interface. */
                 public void SetUserConnection(UserConnection userConnection) {
                     _userConnection = userConnection;
                 }
             }
         }


The `UsrBackgroundActivityCreator` class implements the
`IBackgroundTask<UsrActivityData>` and `IUserConnectionRequired` interfaces.
After a forced 30 seconds delay, the `Run()` method creates an instance of the
**Activities** section object based on the given `UsrActivityData` instance.

5. **Publish the schema**.

## 3\. Create a business process that starts the background operation​

1. [Go to the **Configuration** section](https://academy.creatio.com/documents?ver=8.3&id=15101&anchor=title-2093-2)
   and select a user-made
   [package](https://academy.creatio.com/documents?ver=8.3&id=15121) to add the
   schema.

2. Click **Add** → **Business process** on the section list toolbar.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateBusinessProcessSchema/scr_add_schema.png)

3. Go to the Process Designer and fill out the process properties:
   - Set the **Title** property in the element setup area to "Background Task
     Example Process."
   - Set the **Code** property on the **Settings** tab of the element setup area
     to "UsrBackgroundTaskExampleProcess."

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_BackgroundTaskExampleProcess_Settings.png)

4. Implement the business process.
   1. Click **System actions** in the Designer’s element area and place a
      **Script task** element between the **Simple** start event and
      **Terminate** end event on the Process Designer’s working area.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_add_ScriptTask.png)

     2. Set the name of the **Script task** element to "Create background task."

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_add_BusinessProcess.png)

     3. Add the code of the **Script task** element.

Сode of the Script task element

            var data = new UsrActivityData {
                Title = "Activity created by background task",
                    TypeId = ActivityConsts.TaskTypeUId
            };
            Terrasoft.Core.Tasks.Task.StartNewWithUserConnection <UsrBackgroundActivityCreator, UsrActivityData> (data);

            return true;


     4. Click the ![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/CreateClientSchema\(7.17\)/scr_add_button.png) button in the **Usings** block on the **Methods** tab of the Process Designer and add the `Terrasoft.Configuration` namespace. This is required for the business process to support the implementations of the class for the activity object and class that adds an activity.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_add_Usings.png)

5. **Publish the changes**.

## Outcome of the example​

To **run** the `Background Task Example Process` business process, click **Run**
on the Process Designer’s toolbar.

As a result, the `Background Task Example Process` business process will add the
**Activity created by background task** record to the list view of the
**Activities** section list.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/BackgroundTask/7.18/scr_result.png)

---

## Resources​

[Package with example implementation](https://academy.creatio.com/sites/default/files/documents/downloads/SDK/Packages/sdkBackgroundTaskPackage_2021-09-08_09.11.49.zip)

- 1\. Create a class for the activity object
- 2\. Create a class that adds an activity
- 3\. Create a business process that starts the background operation
- Outcome of the example
- Resources
