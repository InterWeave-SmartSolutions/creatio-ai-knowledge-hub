# Plan visits | Creatio Academy

**Category:** applications **Difficulty:** beginner **Word Count:** 1544
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.2/products/more-apps/field-sales/plan-field-meetings

## Description

Create sales rep visits  in the Visit scheduling view of the Activities section.

## Key Concepts

section, detail, lookup, system setting, notification, contact, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.2**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/products/more-apps/field-sales/plan-field-meetings)**
(8.3).

Version: 8.2Sales Enterprise

On this page

Create **sales rep visits** in the **Visit scheduling** view of the
**Activities** section.

The **Visit scheduling** view has the following functional areas:

1. **List of accounts.** The area displays the list of locations (e.g., sales
   outlets) with scheduled visits. The list includes only the accounts that have
   the same owner specified as the one that is selected in the calendar. You can
   filter the records in the accounts list by selecting the **Apply filter**
   option from the
   ![btn_com_roles_actions_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/btn_com_roles_actions_menu.png)
   button menu.

2. **Sales rep's calendar.** The calendar in the **Visit scheduling** view is
   similar to the standard user calendar. The titles of days in the calendar
   contain additional buttons that allow the user to build the sales rep's daily
   route.

3. **Route map.** The map that displays the sales reps’ daily route.

## Plan visits automatically​

The Field Sales for Creatio app utilizes cyclic task features to implement
automatic visit scheduling. A cyclic task is an activity that includes several
visits to sales outlets during a specified time frame. Use the **Cyclic tasks**
section to create such activities. One cyclic task may schedule multiple visits
over a certain period.

note

The **Cyclic tasks** section becomes available after installing the "Field Sales
for Creatio".

### 1\. Create a cyclic task:​

1.  Go to the **Cyclic tasks** section.

2.  Click the **New task** button.

3.  On the displayed page, populate the required fields: specify the name of the
    cyclic task, the start and the end dates, and the owner. The owner must be a
    contact for which the system user is created.

4.  On the **General information** tab:

         1. Click ![btn_add_ke.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/btn_add_ke.png) in the **Visit categories** detail to add a new visit category record.

         2. Specify the name of the category in the **Name** field.

         3. In the **Quantity** field, specify the total number of visits you want to schedule for the selected time frame. The **Days between visits** and the **Visits frequency per month** field values are populated automatically.

    If you change the values in either one of the **Quantity** , **Days between
    visits** and the **Visits frequency per month** fields, the values in the
    other two fields will be automatically recalculated based on the total task
    execution period.

         4. Select the lookup value in the **Visit rule** field to specify the rule according to which the visit will be performed. Visit rules determine the actions that the sales rep is expected to perform during the visit. Use the **Field visit rules** lookup to set up custom visit rules, if needed.

         5. Add the accounts of the "Sales outlet" and "Retail chain" types to the **Accounts** detail. Creatio will be scheduling visits to these accounts.

5.  Save the cyclic task.

note

We recommend planning your visits quarterly to analyze product promotion results
correctly.

### 2\. Create visits from a cyclic task​

After adding a cyclic task, proceed to schedule visits. To do this:

1. Open the cyclic task created on the previous step and use the **Calculate
   available visits** command of the **Actions** menu on the cyclic task page to
   calculate available visit slots. As a result, Creatio will populate the
   **Available quantity of visits** field of the cyclic task page
   ([Fig. 1](https://academy.creatio.com#XREF_84239_298)).

Fig. 1 Available visit quantity

![Fig. 1 Available visit quantity](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/chapter_field_force_number_of_available_visits.png)

2. When the calculation is finished, the **Schedule visits** action will become
   available on the cyclic task page
   ([Fig. 2](https://academy.creatio.com#XREF_44860_299)).

Fig. 2 The Schedule visits action

![Fig. 2 The Schedule visits action](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/chapter_field_force_cyclic_tasks_plan_visits_action.png)

3. Run the **Schedule visits** action to start the process of automatic visit
   scheduling in accordance with the configured parameters and the sales rep’s
   calendar.

You will receive a notification when the visits have been scheduled. The
**Quantity of scheduled visits** field will display the number of scheduled
visits. The visit activities will appear on the **Activity** detail of the
corresponding accounts.

### How the automatic visit scheduling works​

When scheduling visits, Creatio performs the following actions:

1. Determines the route starting point. The current location of a sales rep
   responsible for the visit can be a starting point. The location is determined
   based on the information from the **Addresses** detail of the corresponding
   contact page. If the contact’s address is not specified, the system will use
   the address from the connected account page.

2. Determines the sales outlet closest to the starting point. The optimal car
   route is determined within the 200 km radius.

3. Checks the working hours of the sales rep and sales outlet.

note

When checking the working hours, Creatio analyzes the calendar of the sales rep
employee. More information about setting up a contact’s calendar is available in
the "Configure a personal calendar for a contact" article. The calendar
specified in the "Base calendar" system setting determines the business hours of
the outlets.

4. Creatio creates the first visit.  
   If the visit time is outside of the working hours, Creatio will look for the
   next closest location. The procedure repeats until all visits have been
   scheduled.

## Plan visits manually​

Before scheduling visits, make sure that the rule that applies to the visit
corresponds to the needed period. If several field rules apply to one visit,
Creatio will let you choose which rule to apply to that visit. Learn more in the
"[Set up rules and actions of a field meeting](https://academy.creatio.com/documents?id=1375)"
article.

To schedule a visit:

1. In the **Activities** section, select the **Visit scheduling** view
   ([Fig. 1](https://academy.creatio.com#XREF_68117_88)).

Fig. 1 Selecting the Visit scheduling view

![Fig. 1 Selecting the Visit scheduling view](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/scr_field_force_open_view.png)

2. Use the filters in the calendar area to select the period and a sales rep
   employee.

3. Select an outlet to schedule a visit to in the list of accounts to the left,
   then drag it and drop into the needed time in the calendar
   ([Fig. 2](https://academy.creatio.com#XREF_98990_89)).

Fig. 2Adding a visit to the calendar

![Fig. 2Adding a visit to the calendar](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/scr_field_drag_account.png)

You can also schedule a visit of **sales rep** in the **Calendar** view of the
**Activities** section. Click **Add action** → "Visit" on the toolbar to
schedule a visit ([Fig. 3](https://academy.creatio.com#XREF_51199_4)). This
method of scheduling a visit requires populating the **Contact** or **Account**
field on the visit page. If both fields are blank, you will not be able to save
the record.

Fig. 3 Adding a visit in the Activities section list

![Fig. 3 Adding a visit in the Activities section list](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/scr_field_force_plan_visit_from_the_list.png)

As a result, Creatio will add a new "Visit" activity. The primary contact of the
account will be specified as the contact of the visit. The list of actions will
be added to the visit according to the corresponding visit rule. Creatio sets
the duration of the visit will according to the corresponding visit rule. If
necessary, you can change the visit duration manually.

note

After adding all visit activities of a sales rep on the calendar, use the map to
view the changes in the sales rep's route for each day. Canceled visits are not
taken into account when building a route.

A manually created visit will be automatically mapped to a cyclic task if the
following parameters match:

- visit time frame

- promoted product

- outlet

If the above parameters of a visit correspond to those of a cyclic task, the
**Cyclic task** field on the **General Information** tab of the visit page will
be populated with that cyclic task, and the cyclic task will treat the manually
scheduled visit as if it was scheduled automatically (will not schedule
duplicate visits, etc.).

## Build a route for a sales rep​

Build sales rep routes on the map for more efficient visit scheduling. Creatio
uses the timing of visits and the locations of the sales outlets to
automatically chart routes that the sales reps should take.

The sales outlet is displayed on the map based on the GPS coordinates specified
on the account page. If an account has several addresses, Creatio will use the
address marked as "primary", regardless of the address type. You can view the
address of an outlet on the map and the title of the corresponding visit by
clicking the marker of the visit.

When all the visits are added to the map, build a route. To do this:

- Click the corresponding
  ![btn_com_map_marker.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/btn_com_map_marker.png)
  button that is located next to the date in the calendar
  ([Fig. 1](https://academy.creatio.com#XREF_62721_90)).

Fig. 1 Building a route for a sales rep

![Fig. 1 Building a route for a sales rep](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/scr_field_force_plan_route.png)

As a result, the map will display the route between the visit locations for the
selected day. The order of visits on the map will correspond to their order in
the schedule.

The
![btn_com_map_marker00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/btn_com_map_marker00001.png)
button in the day title will change its color. The button color will correspond
to the color of the route on the map. The route color is different for each day.

You can view routes for several days by clicking
![btn_com_map_marker00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/field_sales/BPMonlineHelp/field_sales_plan_visits/btn_com_map_marker00002.png)
for multiple dates.

note

On the map, the point that the route starts from is your current location (your
browser will need permission to share your current location). If your browser
privacy settings do not permit sharing location, the first point of the route is
the value specified in the "Default city for employees" system setting.

---

## See also​

[Install the field sales app](https://academy.creatio.com/documents?id=1374)

[Set up rules and actions of a visit](https://academy.creatio.com/documents?id=1375)

[Sales rep's actions during a visit](https://academy.creatio.com/documents?id=1382)

[Check-in verification](https://academy.creatio.com/documents?id=1799)

- Plan visits automatically
  - 1\. Create a cyclic task:
  - 2\. Create visits from a cyclic task
  - How the automatic visit scheduling works
- Plan visits manually
- Build a route for a sales rep
- See also
