# Overview of Freedom UI Designer and its elements | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 4997 **URL:**
https://academy.creatio.com/docs/8.x/no-code-customization/8.0/nocode-platform/UI-designer

## Description

Freedom UI Designer is a visual drag-and-drop editor that lets you create and
set up a fully responsive app layout (including mobile). You can create UIs from
ready layout templates, such as pages with tabs and dashboards. You can also
create a custom UI of any structure from scratch. Set up the pages in the new
Freedom UI framework, which lets you modify the appearance of elements, manage
data sources, and place page components arbitrarily.

## Key Concepts

business process, workflow, configuration, freedom ui, classic ui, section,
lookup, dashboard, integration, database

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/no-code-customization/customization-tools/recommendations/recommendations-on-app-creation)**
(8.3).

Version: 8.0

On this page

Level: beginner

**Freedom UI Designer** is a visual drag-and-drop editor that lets you create
and set up a fully responsive app layout (including mobile). You can create UIs
from ready layout templates, such as pages with tabs and dashboards. You can
also create a custom UI of any structure from scratch. Set up the pages in the
new Freedom UI framework, which lets you modify the appearance of elements,
manage data sources, and place page components arbitrarily.

Work in the Freedom UI Designer using no-code tools. UI design involves
structuring the page with layout elements: tabs, areas, and columns. Depending
on the information you want to display on the page, you can also set up charts,
add fields, lists, buttons, and other components.

note

We recommend using Freedom UI Designer in Google Chrome instead of Safari to
take full advantage of Freedom UI Designer capabilities.

To begin with the setup of Freedom UI pages, click the
![](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/btn_edit_page.png)
button in the top right of the current app page → **Edit page**.

This opens the Freedom UI Designer (Fig. 1).

Fig. 1 Freedom UI Designer

![Fig. 1 Freedom UI Designer](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_freedom_ui_designer.png)

**Element library (1)**. The library contains the tools required to set up a
custom UI.

**Action panel (2)**. Use the action panel to save the page design, cancel the
changes, set up the business rules, open the source code and page property
settings.

**Canvas (3)**. The working area of the Freedom UI Designer. Drag elements from
the library to the canvas to set up the page structure.

**Setup area (4)**. Use the setup area to manage the properties of visual
components, the behavior of buttons, expansion panels, charts, etc. Learn more
about the settings in the description of each element. To open the setup area,
double-click the relevant element or select the element on the canvas and click
.

### UI Designer elements​

View the elements of the Designer in the table below:

| Element types | Description | Data | Element group that manages the page data source: the object of the section where the page is located. | Charts | Elements that visualize statistics. The following chart types are available: spline, line, bar, doughnut, area, column, scatter, pipeline, sales pipeline, full pipeline, metric, gauge. | Components | Elements that execute target page actions and solve a number of other problems: button, label, list, folders, action panel, etc. | Layout elements | Elements that structure the page: expansion panels, tabs, toggle panels, grid containers, flex containers. |
| ------------- | ----------- | ---- | ----------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------- |

## Data​

Apps can contain pages that have different data sources. For example, a data
source for a record page is a specific object. Creatio adds a data source
automatically when you create an app. You can add an existing source or create a
new source when you add an app page.

To add a new data source:

1. Click **Add data source**.
2. Select "New data source." This opens a window.
3. Fill out the **Name** and **Description** fields of the data source in the
   window.

As a result, Creatio will add an object and connect it to the page as a data
source. The Freedom UI Designer will display the data source in the **Data**
group. The **Code** field will be populated automatically (Fig. 2).

Fig. 2 Data in the Freedom UI Designer

![Fig. 2 Data in the Freedom UI Designer](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/designer_interfaces_new_source.png)

You can display data and enable users to enter data using fields and inputs.

### Fields​

Use fields to display data and enable users to enter data. When you set up
fields, Creatio adds and modifies the corresponding attributes of the data
model. After you set up a field and save the page, you can remove the field from
the canvas without removing the corresponding attributes of the data model. To
add existing fields to the page, drag them from the **Data** area to the
relevant part of the canvas.

Creatio specifies the data source automatically. You can change it in the
**Advanced** section of the field setup area if needed. If the new data source
is a different attribute of the page data model, the field on the canvas changes
to the field bound to the specified attribute. If the new data source is an
attribute of a related object, Freedom UI Designer converts the field to an
input.

You can add the following field types to the page in the UI Designer:

- **Text**. Enables users to enter letters, digits, and other characters.
- **Number**. Enables users to enter integers or fractions.
- **Checkbox**. Enables users to select either of the two values: "True" or
  "False." "True" value is a selected checkbox.
- **Date/Time**. Enables users to select date and/or time, depending on the
  selected format.
- **Rich text**. Enables users to enter rich text content, including clickable
  links, images, and tables. For example, this is useful for writing comments or
  knowledge base articles.
- **Phone**. Enables users to enter phone numbers. Functionally identical to the
  "Phone number" format type of the text field. Can apply the phone number
  pattern. If Creatio is integrated with a phone service, users can click the
  phone number to initiate a call from the communication panel. Otherwise,
  clicking the field runs the application that handles phone calls.
- **Email**. Enables users to enter email addresses as clickable "mailto:" links
  that are opened by the default email client. Can validate the email address
  format.
- **Web link**. Enables users to enter clickable URLs.
- **Dropdown**. Enables users to select values from a set list of options stored
  in a lookup or other data source. You can add a new lookup object when you add
  this field.
- **Color**. Enables users to specify a color value. For example, this is useful
  for product pages.
- **Autonumber**. Numbers new records automatically starting from 1, both when a
  user adds a record and a business process or integration add it. You can set
  the number prefix and change the quantity of digits in the number. Creatio
  reserves the number when you click a button that adds records. When you click
  a button that adds records again, Creatio reserves the subsequent number, even
  if the previous record was not saved.
- **Image**. Enables users to upload or view images. Can display images from
  different sources, for example, Creatio database or CDN.

The Freedom UI Designer supports various properties that provide flexible field
setup options. Learn more about setting up fields in a separate guide:
[Fields and inputs](https://academy.creatio.com/docs/user/nocode_platform/element_setup_examples/fields_and_inputs).

Fig. 3 Dropdown field

![Fig. 3 Dropdown field](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_dropdown_field.png)

### Inputs​

Use **Input** layout elements to display data and enable users to enter data.
When you set up inputs, Creatio does not modify the attributes of the data
model.

Specify the data source manually in the **Advanced** section of the input setup
area. Inputs accept data from attributes of related objects. If you specify an
attribute of the page data model, Freedom UI Designer converts the input on the
canvas to a field.

Input setup is mostly similar to the field setup. However, input setup does not
modify the structure of the data model.

The input types you can add correspond to field types except for the unique
**Slider** input. It displays an integer within a range and enables users to
slide the value up and down with a preset step value. Learn more about setting
up the **Slider** in a separate article:
[Set up a Slider input](https://academy.creatio.com/documents?id=2442).

Fig. 4 Slider input

![Fig. 4 Slider input](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_slider.png)

## Charts​

Chart functionality in Freedom UI is mostly similar to
[analytics](https://academy.creatio.com/documents?id=2144) in the **Dashboard**
section of the main Creatio application. However, Freedom UI charts have some
unique features:

- You can connect all charts except "Sales pipeline" and "Full pipeline" to
  lists, approval lists, or attachment lists. This filters chart data by records
  displayed in the connected component or the record selected in the list. For
  example, this lets you display data in case charts only for open cases.

Fig. 5 Charts connected to a list

![Fig. 5 Charts connected to a list](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_charts_connected_to_list.gif)

- You can filter all charts except "Sales pipeline" and "Full pipeline" using
  the **Quick filter** component. For example, this lets you display data in
  case charts only for a particular agent.

Fig. 6 Filtering charts using the quick lookup filter

![Fig. 6 Filtering charts using the quick lookup filter](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_chart_lookup_filter.gif)

- When you drill down chart data, you can customize the data list similarly to a
  Freedom UI section list as well as search for specific records (Fig. 7). Learn
  more about customizing Freedom UI lists in a separate article:
  [Manage a list](https://academy.creatio.com/documents?id=2402).

Fig. 7 Drilling down chart data

![Fig. 7 Drilling down chart data](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_drill_down.gif)

- You can export chart and pivot table data to Excel to process data easier. To
  do this, expand the dashboard and select **Export to Excel** in the context
  menu. The browser will download the data file to your computer (Fig. 8).

Fig. 8 Exporting chart data to Excel

![Fig. 8 Exporting chart data to Excel](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_export_to_excel.gif)

- For charts that have multiple series, you can customize the header color and
  series color individually. Use the **Chart color** and **Style** fields to do
  this, respectively (optional) (Fig. 9).

Fig. 9 Setting up a chart that has several series

![Fig. 9 Setting up a chart that has several series](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/set_home_page/page_wizard_set_dashboard.gif)

- You can select from several fill options in the **Chart style** field for
  "Metric" and "Chart" dashboard headings (Fig. 10).

Fig. 10 Setting up the chart heading style

![Fig. 10 Setting up the chart heading style](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/set_home_page/set_up_dashboard_style.gif)

- The "Pie chart" type is replaced with the "Doughnut chart" type. Set up this
  chart similar to the pie chart (Fig. 11).

Fig. 11 Doughnut chart

![Fig. 11 Doughnut chart](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/set_home_page/dashboard_donut.png)

- You can filter chart and metric data by the parameters of their location page.
  Configure the filter in the **How to associate with page data** field group.
  The setup process is similar to the **How to associate with section data**
  field group. For example, you can set up a budget composition chart on a
  request page and limit the chart data to the request whose page the user
  opens.

- You can specify whether to display values of individual bars and columns on
  "Bar" and "Column" chart types, respectively.

## Components​

### Button​

Use the **Button** component to execute a page action. The following actions are
available:

- **Open new record**. Opens the form page of a new record that belongs to any
  Creatio object. You can create and edit the form page for any Creatio object
  as part of the button setup. It is possible to set different form pages for
  new records and existing records, for example, a mini page and full page,
  respectively. If different record types use different pages, for example,
  **Activities** section, you can specify the page to open.

The action can also populate the form page fields with specific values if
needed.

- **Delete data**. Deletes selected records from the **List** component that has
  multiselect turned on.

- **Open existing record**. Opens the form page of a specific record that
  belongs to any Creatio object. You can create and edit the form page for any
  Creatio object as part of the button setup. It is possible to set different
  form pages for new records and existing records, for example, a mini page and
  full page, respectively. If different record types use different pages, for
  example, the **Activities** section, you can specify the page to open.

- **Open specific page**. Opens any Freedom UI page, including list pages, mini
  pages, and homepages. You can create and edit the page to open as part of the
  button setup.

- **Open duplicates page**. Searches for duplicate records and displays the
  found duplicates on a separate page. You can connect the button to any section
  that supports the duplicate search functionality.

- **Save data**. Saves changes without closing the page. Applies to all page
  data sources, for example, fields and editable lists.

- **Cancel changes**. Cancels changes without closing the page. Applies to all
  page data sources, for example, fields and editable lists.

- **Refresh data**. Refreshes data of a list object, attachment list, approval
  list, or gallery without refreshing the entire page.

- **Close page**. Returns to the previous page the browser tab had open. If the
  current page is the first page the browser tab has open, no action is
  executed.

- **Run process**. Runs the latest version of a business process. You can create
  and edit the process to run as part of the button setup.

- **Upload file**. Uploads a file to an attachment list. You can select from
  attachment lists that are present on the page. The upload mechanism is
  pre-configured and non-editable.

- **Add communication option**. Adds a communication option to the
  **Communication options** component. The action is available only if you have
  **Customer 360** app installed.

- **Data import**. Imports data to any Creatio object. The import mechanism is
  pre-configured and non-editable.

- **Export to Excel**. Downloads list data as an \*.xlsx file. You can select
  from lists that are present on the page except for attachment lists. The
  export mechanism is pre-configured and non-editable.

- **Set up access rights**. Configures access permissions to the form page where
  the button is placed. Works only on form pages. The permission setup mechanism
  is pre-configured and non-editable.

- **Show record's relationship**. Opens the relationship chart of an account or
  contact record.

- **Continue in other page**. Opens the default form page for the data source
  without saving the record yet. This is particularly useful for mini pages.

You can customize button caption, visual style, and size as well as add an icon
to a button. You can also set up multi-level button menus. A menu item title can
contain text, an icon, or both. You can copy existing menu items to accelerate
the setup process. You can also copy existing buttons together with their
settings.

Learn more about setting up buttons in a separate article:
[Set up Button components](https://academy.creatio.com/documents?id=2401).

Fig. 12 Button component

![Fig. 12 Button component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_button.png)

### List​

Use the **List** component to add a list of the selected object’s data based on
pre-configured filters.

You can connect lists to other page components that work with data. This
includes approval lists, attachment lists, other lists, or charts except "Sales
pipeline" and "Full pipeline." The connected components filter their data by
records displayed in the list. For example, this lets you filter the list of
cases by the list of displayed agents. Components can be linked via direct
connection, for example, the city of a contact. If you connect a list to another
list, you can also filter data by the record selected in the list.

Users can add, hide, freeze, and resize list columns while working in an app.
Creatio saves the list settings in the user profile, therefore the settings are
applied every time an app is opened. It is also possible to apply list settings
to every app user. Restore the default settings in a single click via the
**Reset to default settings** button. Learn more about managing lists in a
separate article:
[Manage a list](https://academy.creatio.com/documents?id=2402).

Learn more about setting up lists in a separate article:
[Set up List components](https://academy.creatio.com/documents?id=2457).

Fig. 13 List component

![Fig. 13 List component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_freedom_ui_list.png)

### Expanded list​

**Expanded list** is an **Expansion panel** layout element that has **List** ,
**Search** , and multiple **Button** components that control the list attached.
Once you select a list object, Freedom UI Designer automatically links the
**Search** component and buttons to the object. The title of the expansion panel
is updated automatically as well provided that you have not changed the title
manually. Otherwise, setup process of the expansion panel and components
attached to it is identical to standalone elements.

Fig. 14 Expanded list component

![Fig. 14 Expanded list component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_expanded_list.png)

### Label​

Use the **Label** component to add arbitrary text to the page, create individual
headings for element groups, or display data of the current user contact. Learn
more about setting up labels in a separate article:
[Set up a Label component](https://academy.creatio.com/documents?id=2433).

Fig. 15 Label component

![Fig. 15 Label component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_label.png)

### Folders​

Use the **Folders** component to configure the folder structure that segments
records by the specified filters. If you create a Freedom UI app for an object
that has a Classic UI section, you can reuse folders of the Classic UI section
in the Freedom UI **Folders** component. This streamlines the migration of
Classic UI sections to Freedom UI.

Manage Freedom UI folders similarly to folders in the classic Creatio UI. Learn
more in a separate article:
[Folders](https://academy.creatio.com/documents?id=1018).

Fig. 16 Folders component

![Fig. 16 Folders component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_folders.png)

### Folder management menu​

Use the **Folder management menu** component to enable users to open the page
folder tree as well as reach favorite folders quickly. If the page contains the
**Folders** component without the management menu, users will be unable to
reopen the folder tree after closing it.

Fig. 17 Folder management menu component

![Fig. 17 Folder management menu component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_folder_management_menu.gif)

### Communication options​

The component is available if you have **Customer 360** app installed.

Use the **Communication options** component to enable users to manage record
communication options, for example, email, phone, and web link.

The component comprises **Expansion panel** , **Button** , **Flex container** ,
**Grid container** , and **Communication options** componets. Setup procedure
for all components except for **Communication options** is identical to
standalone elements.

Fig. 18 Communication options component

![Fig. 18 Communication options component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_communication_options.png)

### Feed​

Use the **Feed** component to enable internal and external users to post and
read comments that support rich text and user mention via "@." Authors can edit
or delete their posts or attachments. You can select between the following feed
types:

- "Record." Display posts and comments connected to a specific record. For
  example, a lead.
- "User." Display the index of posts and comments that mention the current user
  or those to which the user is subscribed.

Fig. 19 Feed component

![Fig. 19 Feed component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_feed.png)

### Action dashboard​

note

The component is available in Creatio version 8.0.8 and earlier. Action
dashboards are still available on existing pages in Creatio version 8.0.9 and
later, but you cannot add them to new pages. Instead, use **Progress bar** and
**Next steps** components that let you set up user workflow much more flexibly.
Learn more about the components in different sections: Progress bar, Next steps.

Use the **Action dashboard** component to edit the dynamic case that organizes
the workflow in the app. You can define the list of actions users can execute
directly from the page using a mini page, for example, schedule a task, write an
email, summarize the call results, post a message in the record feed.

If the data source is specified in the element setup area (for example, when you
add an action dashboard to the canvas, Freedom UI Designer sets the element data
source to the page data source automatically), click the **Set up cases** button
to open the Case Designer. Specify the case stages, as well as steps and tasks
required to complete the case in the Designer. Learn more in a separate guide:
[Case Designer workflows](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/category/case-designer-workflows).

Fig. 20 Action dashboard component

![Fig. 20 Action dashboard component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_action_dashboard.png)

### Attachments​

Use the **Attachments** component to enable users to upload and download files.
You can bind the files to the current record or related objects. You can also
tag specific attachments to filter them or display multiple attachment lists on
a single page, for example, required request files and additional request files.

The component comprises **Expansion panel** , **Button** , **Flex container** ,
and **Attachment list** components. Setup procedure for all components except
for the **Attachment list** is identical to standalone components. Learn more
about setting up attachments in a separate article:
[Set up an Attachments component](https://academy.creatio.com/documents?id=2434).

Fig. 21 Attachments component

![Fig. 21 Attachments component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_attachments.png)

### Gallery​

note

The component is available for beta testing in Creatio version 8.0.2 Atlas and
later. To evaluate new Creatio capabilities, enable the "ShowDesignerDemoItems"
feature in a test environment yourself using
[Feature Toggle mechanism](https://academy.creatio.com/documents?id=15631) or
request Creatio support to enable the feature. Contact us if you have feedback,
we appreciate it:
[beta@creatio.com](https://academy.creatio.commailto:%20beta@creatio.com)

Use the **Gallery** component to display visual data of any Creatio object on a
page. For example, you can display the index of meeting participants or order
products as a gallery. Besides images, you can display record caption and brief
description text in the gallery (Fig. 22).

Fig. 22 Gallery component

![Fig. 22 Gallery component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_gallery.png)

### Approvals​

Use the **Approvals** component to enable users to approve or deny records. You
can hide the component from the page if the current user has no approvals
assigned to them.

The component behavior is pre-configured and non-editable. After you add the
component to the page, set up the approval mechanism in a business process or
case. Learn more in separate articles:
[Configure a document approval process](https://academy.creatio.com/documents?id=2363),
[Set up an approval case](https://academy.creatio.com/documents?id=2328).

Fig. 23 Approvals component

![Fig. 23 Approvals component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_approvals.png)

### Approvals list​

Use the **Approvals list** component to enable users to view the entire approval
process of a specific record as a list to ensure transparency. The component is
an **Expansion panel** element that has **Approvals list** , **Search** , and
multiple **Button** components attached. The setup process of the expansion
panel and most components attached to it is identical to standalone components.
The behavior of the **Approvals list** component is pre-configured and
non-editable.

Fig. 24 Approvals list component

![Fig. 24 Approvals list component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_approvals_list.png)

### Progress bar​

Use the **Progress bar** component to enable users to track and change case
stages. The element is connected to the page data source automatically. Click
the **Set up cases** button to open the Case Designer. Specify the case stages
as well as steps and tasks required to complete the case in the Designer. Learn
more in a separate guide:
[Case Designer workflows](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/category/case-designer-workflows).

Fig. 25 Progress bar component

![Fig. 25 Progress bar component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_progress_bar.png)

### Next steps​

Use the **Next steps** component to view and manage activities and tasks for the
current record as tiles. The activities and tasks can be generated by cases or
added manually. The component completes activities and displays new activities
based on the stage in the **Progress bar** component. The component also lets
you do the following:

- add a task or email
- complete an activity manually
- approve a record
- view the task owner and open their contact page

The component comprises **Expansion panel** , **Button** , **Flex container** ,
**Grid container** , and **Next steps** components. Setup procedure for all
components except for **Next steps** is identical to standalone elements. The
behavior of the **Next steps** component is pre-configured and non-editable.

Fig. 26 Next steps component

![Fig. 26 Next steps component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_next_steps.png)

### Search​

Use the **Search** component to enable users to search for records by all
visible columns or specific visible columns in any Freedom UI list, attachment
list, or approval list. The **Expanded list** and **Approvals list** components
include the component by default.

Fig. 27 Search component

![Fig. 27 Search component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_search.gif)

### Quick filter​

Use the **Quick filter** component to enable users to filter the values of any
list or chart except for "Sales pipeline" and "Full pipeline" by a manually
defined condition, date/time range, or the value of any lookup. Learn more about
setting up quick filters in a separate article:
[Set up Quick filter components](https://academy.creatio.com/documents?id=2458).

Fig. 28 Quick filter component

![Fig. 28 Quick filter component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_quick_lookup_filter.gif)

### Message composer​

Use the **Message composer** component to send emails and post feed messages.
Both communication channels support rich text, including images. The email
channel includes the following features as well:

- Attachments. The upload of attachments is restricted based on the values of
  "Attachment max size" ("MaxFileSize" code), "File Security Mode"
  ("FileSecurityMode" code), and "MaxAttachmentSize" system settings.
- Templates. Learn more:
  [Work with message templates](https://academy.creatio.com/documents?id=2357).
- Drafts. The component also saves drafts automatically when you close the tab
  or open a different page.
- Email forwarding.
- Email thread expansion.

The **Timeline** component also includes the message composer functionality.

Fig. 29 Message composer component

![Fig. 29 Message composer component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_message_composer.png)

### Timeline​

Use the **Timeline** component to enable users to view the history of
communication regarding the record as well as records linked to it in
chronological order. You can specify the sorting column for most objects in the
timeline except for "Feed" and "File" that are always sorted by creation date.
Users can like and comment feed records in the timeline. The component also
includes the message composer functionality.

The component displays the linked records of the following objects:

- Attachments
- Activities
- Emails
- Calls
- Feed messages

note

To display additional objects, select the "Show in Timeline component by
default" checkbox for the relevant object in the Object Designer. Learn more
about the Object Designer in the developer documentation:
[Object](https://academy.creatio.com/documents?id=15107).

The timeline displays the primary display value and creation date of linked
records. You can customize the columns to display in the timeline addon of the
relevant object using low-code tools. Learn more in the developer documentation:
[Customize an object column to display in the **Timeline** component](https://academy.creatio.com/documents?id=15046).

Fig. 30 Timeline component

![Fig. 30 Timeline component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_timeline.png)

### Timer​

Use the **Timer** component to count down to or up from specific date and time
in the time zone of the user. For example, this is useful if you want to display
the case response deadline. Learn more about setting up timers in a separate
article: [Set up timers](https://academy.creatio.com/documents?id=2435).

Fig. 31 Timer component

![Fig. 31 Timer component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_timer.png)

### Local time​

Use the **Local time** component to display the current time within a time zone.
You can use any time zone field as a data source. Learn more about setting up
local time in a separate article:
[Set up a Local time component](https://academy.creatio.com/documents?id=2436).

Fig. 32 Local time component

![Fig. 32 Local time component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_local_time.png)

### Account compact profile​

The component is available if you have the **Customer 360** app installed.

Use the **Account compact profile** component to display main data of an
account:

- logo
- name
- also known as
- local time
- country

The component behavior is pre-configured and non-editable.

Fig. 33 Account compact profile component

![Fig. 33 Account compact profile component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_account_compact_profile.png)

### Contact compact profile​

The component is available if you have the **Customer 360** app installed.

Use the **Contact compact profile** component to display main data of a contact:

- photo
- full name
- birth date
- age
- local time
- country

The component behavior is pre-configured and non-editable.

Fig. 34 Contact compact profile component

![Fig. 34 Contact compact profile component](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_contact_compact_profile.png)

## Layout elements​

### Expansion panel​

Use the **Expansion panel** layout element to add page elements grouped by a
single criterion. You can attach any elements available in the Freedom UI
Designer to the expansion panel title or the area within the expansion panel.
Learn more about setting up expansion panels in a separate article:
[Set up an Expansion panel layout element](https://academy.creatio.com/documents?id=2437).

You can customize the internal layout of the expansion panel: column number,
background color, spacing, etc. To do this, select the area within the expansion
panel and click the
![](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/btn_properties.png)
button. The customization is similar to the **Grid container** layout element.
Learn more about setting up grid containers in a separate article:
[Set up a Grid container layout element](https://academy.creatio.com/documents?id=2439).

Fig. 35 Expansion panel layout element

![Fig. 35 Expansion panel layout element](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_expansion_panel.gif)

### Tabs​

Use the **Tabs** layout element to add a tab area to the page. The area lets you
display content grouped by multiple criteria. That way, you can publish more
required information without overcrowding the page. You can reorder tabs and
attach any elements available in the Freedom UI Designer to tabs, including
other tabs. To do this, drag the tab to the needed position. Learn more about
setting up tabs in a separate article:
[Set up a Tabs layout element](https://academy.creatio.com/documents?id=2438).

You can customize the internal layout of each tab: column number, background
color, spacing, etc. To do this, select the area within a tab and click the
![](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/btn_properties.png)
button. The customization is similar to the **Grid container** layout element.
Learn more about setting up grid containers in a separate article:
[Set up a Grid container layout element](https://academy.creatio.com/documents?id=2439).

Fig. 36 Tabs layout element

![Fig. 36 Tabs layout element](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_tabs.gif)

### Toggle panel​

Use the **Toggle panel** layout element to add a tab area to the page. Compared
to the similar **Tabs** element, toggle panel has the following unique features
that let you create more advanced page functionality:

- Toggle panel is controlled by buttons you can place anywhere on the page.
- You can click the active tab button to hide the panel. Click any tab button to
  display the panel again. The panel is hidden by default.

This lets you save more workspace by placing elements that are usually only
needed on demand, such as a feed or attachment list.

The element setup process is similar to the **Tabs** layout element. Learn more
about setting up tabs in a separate article:
[Set up a Tabs layout element](https://academy.creatio.com/documents?id=2438).

Fig. 37 Toggle panel layout element

![Fig. 37 Toggle panel layout element](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/gif_toggle_panel.gif)

### Area and columns​

**Area** and **Columns** layout elements are different configuration options of
the **Grid container** element. Grid containers have a fixed layout that can
contain up to 12 columns. You can attach any Freedom UI element to a grid
container, including other grid containers.

Areas let you divide the page visually into multiple sections. Use areas to add
page blocks that group any combination of other elements. For example, fields,
charts, buttons, and other areas. Use columns to change layout parameters for
areas, expansion panels, or tabs flexibly as well as arrange page content
vertically.

Learn more about setting up grid containers in a separate article:
[Set up a Grid container layout element](https://academy.creatio.com/documents?id=2439).

Fig. 38 Fields in the 3 columns layout element

![Fig. 38 Fields in the 3 columns layout element](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_columns.png)

### Flex container​

Use flex containers to group elements in a certain direction without binding the
elements to a fixed layout. For example, flex containers are a convenient option
for button placement.

The Freedom UI Designer includes the following flex container types:

- **Flex row**. Lets you place elements horizontally. For example, buttons.
- **Flex column**. Lets you place as many elements as needed vertically.

To transform a flex row into a flex column and vice versa, click the
corresponding buttons in the **Direction** block of the setup area. Learn more
about setting up flex containers in a separate article:
[Set up a Flex container layout element](https://academy.creatio.com/documents?id=2440).

Fig. 39 Buttons in the Flex row layout element

![Fig. 39 Buttons in the Flex row layout element](https://academy.creatio.com/docs/sites/en/files/images/NoCode_Customization/designer_interfaces/updates/scr_flex_container.png)

---

## See also​

[Create a custom app](https://academy.creatio.com/documents?id=2377)

[Install applications from the Marketplace](https://academy.creatio.com/documents?id=1836)

[Element setup examples](https://academy.creatio.com/docs/8.x/no-code-customization/8.0/category/element-setup-examples)

[Set up the app UI](https://academy.creatio.com/documents?id=2409)

[Set up business rules](https://academy.creatio.com/documents?id=2409)

[Localize a Freedom UI element](https://academy.creatio.com/documents?id=2441)

- UI Designer elements
- Data
  - Fields
  - Inputs
- Charts
- Components
  - Button
  - List
  - Expanded list
  - Label
  - Folders
  - Folder management menu
  - Communication options
  - Feed
  - Action dashboard
  - Attachments
  - Gallery
  - Approvals
  - Approvals list
  - Progress bar
  - Next steps
  - Search
  - Quick filter
  - Message composer
  - Timeline
  - Timer
  - Local time
  - Account compact profile
  - Contact compact profile
- Layout elements
  - Expansion panel
  - Tabs
  - Toggle panel
  - Area and columns
  - Flex container
- See also
