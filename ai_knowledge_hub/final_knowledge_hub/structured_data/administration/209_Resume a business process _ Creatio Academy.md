# Resume a business process | Creatio Academy

**Category:** administration **Difficulty:** advanced **Word Count:** 647
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.1/creatio-basics/running-business-processes/resume-business-process

## Description

If a process step was postponed or a step was activated without opening any
pages, you can resume the process in the following ways:

## Key Concepts

business process, section, notification, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/creatio-basics/running-business-processes/resume-business-process)**
(8.3).

Version: 8.1All Creatio products

On this page

If a process step was postponed or a step was activated without opening any
pages, you can resume the process in the following ways:

- In the **Activities** section. Read more >>>
- From a record connected to the postponed process step. Read more >>>

Learn more about resuming business processes by a system administrator in the
[Run a process or a process step](https://academy.creatio.com/documents?id=7098)
article.

## Resume a process in the Activities section​

Processes often create activities for users to complete. A list of activities is
displayed in the **Activities** section and on the **History** tab in other
sections.

To resume a process, open a connected activity in the list of the **Activities**
section.

When the [**User dialog**](https://academy.creatio.com/documents?id=7010) and
[**Open edit page**](https://academy.creatio.com/documents?id=7012) elements are
activated, a process creates activities of the "Task" type in the **Activities**
section. If you open such an activity, the dialog page opens instead of the
default activity page.

note

Custom pages open only for incomplete activities. After the process element is
completed, the default task page will open for this activity.

## Resume a process from a connected record​

A process can perform steps that do not include any activities, for example,
when a page must be activated during a process, or the action is connected with
a specific record in the system.

If such a step is postponed, you can return to it by using the **Process**
button on the page of the record that is connected to the step
([Fig. 1](https://academy.creatio.com#XREF_28109_110)). If the record is
connected to multiple tasks, you can select the required task from the list.

Fig. 1 Resuming a process from a connected record page

![Fig. 1 Resuming a process from a connected record page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_processes_execution_continue_page.png)

If this record is selected from a list, system also displays **Move down the
process** button ([Fig. 2](https://academy.creatio.com#XREF_37808_111)).

Fig. 2 Resuming a process from a list

![Fig. 2 Resuming a process from a list](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_processes_execution_continue_list.png)

If you click the **Move down the process** button and the record is connected to
one incomplete process step, the corresponding page will be opened. If there are
several steps for the record, an additional window will open where you will have
the possibility to select the required step.

## Resume a process from the communication panel​

The notifications display case and process steps (also known as "user actions")
that require some form of activity from you. These process-related actions may
include completing Creatio activities, sending emails, editing records, filling
out pre-configured pages, etc. The tab displays process tasks where:

- You are specified as the owner.

- The process task status is "Running".

All notifications on the
![btn_com_process_tasks00013.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/base/BPMonlineHelp/chapter_notifications/btn_com_process_tasks00013.png)
tab in the notification center are active until they are processed. Click the
process task title to open the page where you can complete this process task
([Fig. 3](https://academy.creatio.com#XREF_95995_30)).

Fig. 3 Executing a business process task

![Fig. 3 Executing a business process task](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/base/BPMonlineHelp/chapter_notifications/scr_notifications_reminder_case.png)

Perform the process task on the opened page: complete the opened activity, send
the email, save the record, etc. If the process task is canceled or postponed to
a later time, the corresponding notification will be updated automatically.

After completing the process task, the notification will no longer display on
the communication panel. Once all process steps have been completed, the counter
on the
![btn_com_process_tasks00014.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/base/BPMonlineHelp/chapter_notifications/btn_com_process_tasks00014.png)
button disappears.

## Complete a process​

A process ends automatically when the end event is activated or when all active
process steps are completed. When a process instance is completed, the system
calculates the duration.

note

Only completed processes are taken into account when calculating statistics.

If you need to terminate a business process, you can
[cancel the process instance](https://academy.creatio.com/documents?id=7106) or
[disable the process](https://academy.creatio.com/documents?id=7106) itself.

---

## See also​

[Run a business process](https://academy.creatio.com/documents?id=7097)

[Execute process steps](https://academy.creatio.com/documents?id=7099)

- Resume a process in the Activities section
- Resume a process from a connected record
- Resume a process from the communication panel
- Complete a process
- See also
