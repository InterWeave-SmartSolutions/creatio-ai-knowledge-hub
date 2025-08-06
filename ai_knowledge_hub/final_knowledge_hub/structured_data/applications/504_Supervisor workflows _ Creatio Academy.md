# Supervisor workflows | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 1349
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/service-tools/contact-center-tools/agent-desktop-workflows/supervisor-workflows

## Description

The contact center or support team supervisor can use the Queues section to
control the queue elements handling.

## Key Concepts

workflow, section, lookup, operation, contact, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Service Creatio

On this page

The contact center or support team supervisor can use the **Queues** section to
control the queue elements handling.

Here you can view all cases and other queue elements:

- You can monitor the work of the contact center on-line.
  [When monitoring the content of all queues](https://academy.creatio.com#HT_section_supervisor_view_queue_items)
  in one list, a contact center supervisor can view the number of cases or
  outgoing calls or elements that are already in progress.

- [Track the performance of specific queues](https://academy.creatio.com#HT_section_supervisor_filter_by_queue)
  and
  [control the workload of particular agents](https://academy.creatio.com#HT_section_supervisor_filter_by_agent)
  using the quick filters.

- Due to the similar
  [queue element sorting](https://academy.creatio.com#HT_section_supervisor_sorting),
  as well as on the agent desktop agent page, the supervisor can identify which
  queue elements are going to be processed.

- Distribute the current workload between the agents
  [by assigning the agents to specific queue elements](https://academy.creatio.com#HT_section_supervisor_act_assign_agent).
  Involve additional agents to work with the queues. Delegate cases from one
  agent to the other or cancel handling the case by a particular agent.

- Join the contact center team: take cases and other queue elements, return the
  elements that were closed incorrectly back to the corresponding queues,
  manually close the queue elements that do not require processing.

note

Any user who has access to the **Queues** section can perform all operations as
the contact center manager.

## Monitor contact center performance​

The key element of agent workflow management is the ability to monitor the total
workload of the contact center. When monitoring all outgoing calls and incoming
cases in a single list, the supervisor can quickly identify the cases that
require attention.

Use the **Queues** section to view all incoming cases, contacts, and accounts in
a single list if they were added to the
[static queues](https://academy.creatio.com/documents?product=studio&ver=7&id=802)
or are within the
[dynamic queues](https://academy.creatio.com/documents?product=administration&ver=7&id=801)
according to the filter settings.

The list displays key information about the queue content. You can manage the
information displayed using the standard **View** menu → **Select fields to
display** menu.

Queue| The queue to which the element belongs. Click the queue name to open the
setup page of the current queue.| Agent| The agent who processed the queue
element or was assigned by the contact center manager to handle the queue
element.| Status| Current status of the element in a queue:

- "Not processed" – the agent has not started working with the element.
  Assigning the agent does not change the status of the element in the queue.
- "In progress" – the agent has started working on the element by clicking the
  **Take it** button.
- "Processed" – the agent has finished working with this element. The elements
  in this status are not displayed unless the **Show processed** checkbox is
  checked.

| Date of next handling | The field displays the date when this element is scheduled for processing if the agent postponed the processing of this element. | Number of postponements | The number of times the element was returned to the queue by clicking the **Back to queue** button. | Case, Account, Contact, etc. | The main fields of the queue object. The "primary display columns" of the queue object. The primary display column contains the case number for the "Cases" queue object or the contact full name for the "Contact" queue object. If you add other objects to the **Queue objects** lookup, their primary display columns will be displayed in this field too. Click the queue element name to open the corresponding record page. |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

note

[Customize columns](https://academy.creatio.com/documents?product=base&ver=7&id=1231)
to display fields of queue objects in the list. For example, you can add the
**Case subject** field to the list of the **Queues** section.

The **Queues** section displays information about queue elements that are being
processed, elements that were taken by an agent and postponed, and those that
were not taken. When sorting elements by the **Agent** or **Status** column, the
contact center manager can view the current status of the operations.

## Manage progress on specific queues​

To monitor the progress of particular queues, the contact center manager can
quickly display data for particular queues. For example, the queues filter can
be used to analyze calls to customers for one or several product promotions.

To view particular queue items, filter the records using the **Queue** filter:

1. Go to the **Queues** section.

2. In the **Queues** view, click **Queue** and select the **Add queue** option.

3. Select the required queue in the opened lookup.

The selected queue will be added to the filter conditions. The content of this
queue will be displayed in the list. If you add multiple queues to the filter,
all elements from the selected queues will be displayed.

You can view the progress for specific queues by displaying the total number of
their elements. To view the queue elements:

1. In the **View** menu, select the **Set up summaries** command.

2. Select the **Display number of records** checkbox.

To display processed elements, select the **Show processed** checkbox. Only
processed elements from the selected queues will be displayed in the list, for
example, closed cases or completed calls.

To view which queue elements are in the process, sort the elements by **Agent**
or **Status** column.

## Manage current workload of an agent​

To view the current workload of an agent, filter the elements by the agent in
the **Queues** section. The filter enables you to view the current workload for
one or several agents regardless of which queues they work with.

To filter the case by an agent:

1. Go to the **Queues** section.

2. Select the **Add agent** option from the **Agent** filter.

3. Select the required agent in the opened lookup.

The list will display queue elements that are being processed by the selected
agent and those elements assigned to that particular agent. If you add several
agents to the filter, the list will display queue elements processed by all of
the selected agents.

4. To view processed cases, check the **Show processed** checkbox.

As a result, processed queue elements, such as closed cases, will be displayed
in the list. for example, the cases with the "Closed" status.

The contact center manager can then monitor which cases the agent is currently
processing and which the agent has already processed.

## Plan agent workload​

To plan which queue elements will be processed next by the agents, display the
items from the selected queues in the same order as they are shown on the agent
desktop To do this:

1. Go to the **Queues** section.

2. Use the queue filter to display the required elements in the list.

3. Select the **Agent view** checkbox.

The queue elements will be displayed in the same order as they are shown on the
agent desktop As a result, the contact center manager can view the order in
which the elements will be processed.

If the **Agent view** checkbox is selected, the list in the **Queues** section
will display all elements from the blind queues and in the order in which they
will be processed.

## Assign agents​

The contact center manager can assign and reassign agents manually or cancel low
priority elements.

To assign agents:

1. Go to the **Queues** section.

2. Select the queue element that must be assigned to a particular agent in the
   list.

3. Select the **Assign agent** option from the **Actions** menu.

4. Select an agent from the list.

The selected agent will be assigned to the queue element. The elements assigned
to the agent will be displayed on the agent desktop for this particular agent
even if the agent is not included in the team of the corresponding queue. After
assigning the agent, the item will not be displayed on the agent desktop for
other agents.

To cancel the assignment:

1. Go to the **Queues** section.

2. Select the element that has been assigned to an agent.

3. Select the **Clear agent** option from the **Actions** menu.

The selected element will be returned to the queue and becomes available for an
agent who is included in the corresponding queue team.

---

## See also​

[General Agent Desktop settings](https://academy.creatio.com/documents?id=1072)

[Regular queue workflow](https://academy.creatio.com/documents?id=810)

[Blind queue workflow](https://academy.creatio.com/documents?id=811)

[Incoming call workflow](https://academy.creatio.com/documents?id=812)

[Sort queue elements](https://academy.creatio.com/documents?id=813)

[Set up regular and blind queues](https://academy.creatio.com/documents?id=803)

- Monitor contact center performance
- Manage progress on specific queues
- Manage current workload of an agent
- Plan agent workload
- Assign agents
- See also
