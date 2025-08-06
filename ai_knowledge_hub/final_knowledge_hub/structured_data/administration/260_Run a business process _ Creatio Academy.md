# Run a business process | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 691
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/creatio-basics/running-business-processes/run-business-process

## Description

Use the following tools to run a Creatio process manually:

## Key Concepts

business process, section, contact, case

## Use Cases

## Content

Version: 8.3All Creatio products

On this page

Use the following tools to run a Creatio process manually:

- Command line. Read more >>>
- Side panel. Read more >>>
- Any section that has processes associated with it. Read more >>>
- Section record page. Read more >>>

Learn more about how system administrators can run business processes in a
separate article:
[Run a process or a process step](https://academy.creatio.com/documents?id=7098).

note

Regardless of the tool, you can only run business processes that can be launched
manually, provided you have the corresponding permissions. Learn more in a
separate article:
[Set up the permissions to run a process](https://academy.creatio.com/documents?id=2348).

Once a business process is run, Creatio adds a new **process instance** that
starts executing process steps. These steps can include include opening record
pages, creating activities, etc.

Creatio terminates the business process instance when the end event is triggered
on the process diagram. You can start and stop business processes manually or
have them start automatically.

Important

You can run only active published processes with the "Business Process" tag
manually. Processes of other types cannot be run manually. If you try to run an
unpublished or inactive process, Creatio displays an error message.

## Run a process from the command line​

1. Enter **Run process** followed by the process name in the command line (Fig.
   1).

Fig. 1 Run a process from the command line

![Fig. 1 Run a process from the command line](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_processes_execution_start_command_line.png)

2. Click the
   ![btn_param_window_change.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/btn_param_window_change.png)
   button.

note

Learn more about the command line functionality in a separate article:
[Search records and run commands](https://academy.creatio.com/documents?id=1228).

## Run a process from the side panel​

1. Click the
   ![btn_com_sidebar_start_process.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/btn_com_sidebar_start_process.png)
   button on the side panel.

2. Select a process to run (Fig. 2).

Fig. 2 Run a process from the side panel using the run process button

![Fig. 2 Run a process from the side panel using the run process button](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_process_execution_start_process_sidebar.png)

note

Specify whether you can run the process using the
![btn_com_sidebar_start_process00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/btn_com_sidebar_start_process00001.png)
button on the
[process properties page](https://academy.creatio.com/documents?id=7111) of the
**Process library** section.

To run a process that is unavailable in the
![btn_com_sidebar_start_process00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/btn_com_sidebar_start_process00002.png)
button index:

1. Select **Another process** (Fig. 3). This opens a box.

Fig. 3 Select the command that runs a process

![Fig. 3 Select the command that runs a process](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_process_execution_start_other_process.png)

2. Select a process in the box that opens and click **Run**.

note

The same box opens when you click the
![btn_com_main_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/btn_com_main_menu.png)
button in the side panel and select **Run process**.

## Run a process from a section or record page​

If a section has an index of processes you can run from the section set up,
Creatio displays the **Run process** button in the section toolbar.

To run a process from a section:

1. Click **New process**.

2. Select a process to run (Fig. 4).

Fig. 4 Run a process from a section

![Fig. 4 Run a process from a section](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_processes_execution_start_section.png)

Creatio displays the same process index on the record page when you click
**Process** on the toolbar (Fig. 5).

Fig. 5 Run a process from a record page

![Fig. 5 Run a process from a record page](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/bpms/BPMonlineHelp/chapter_process_execution/scr_chapter_processes_execution_start_page.png)

### Run a process for multiple records in a section​

You can run a
[section business process](https://academy.creatio.com/documents?id=7152) for
multiple records at once. To do this:

1. Open the section where you want to run a process for multiple records, e. g.,
   **Contacts**.

2. Click **Actions** → **Select multiple records**.

3. Select the needed records.

4. Click **Run process** on the section toolbar and select the needed process.

note

The **Run process** button menu displays all processes you can run from the
section. The processes in the menu are grouped by start type: from the section
and from a record.

Fig. 6 Run a process for multiple section records

![Fig. 6 Run a process for multiple section records](https://academy.creatio.com/docs/sites/en/files/images/Platform_basics/run_business_process/run_process_multiple_records_0.gif)

As a result, Creatio will run a separate process instance for every selected
record. If one of the instances fails, other instances will continue running.

## Run a process automatically​

Processes can be run automatically when certain events occur. These events
include adding, modifying and deleting records. In this case, you do not need to
run the process manually.

Set up the automatic process start after an event in the
[Process Designer](https://academy.creatio.com/documents?id=7172).

---

## See also​

[Execute process steps](https://academy.creatio.com/documents?id=7099)

[Resume a business process](https://academy.creatio.com/documents?id=7105)

[Run a process or a process step](https://academy.creatio.com/documents?id=7098)

- Run a process from the command line
- Run a process from the side panel
- Run a process from a section or record page
  - Run a process for multiple records in a section
- Run a process automatically
- See also
