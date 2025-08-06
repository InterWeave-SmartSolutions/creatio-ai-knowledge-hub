# Schedule med rep visits | Creatio Academy

**Category:** administration **Difficulty:** beginner **Word Count:** 1970
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/pharma/schedule-med-rep-visits

## Description

Schedule visits of your pharmaceutical reps to physicians and pharmacies and
build routes on the map using the Visit scheduling view of the Activities
section.

## Key Concepts

section, detail, lookup, system setting, notification, contact, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Schedule visits of your pharmaceutical reps to physicians and pharmacies and
build routes on the map using the **Visit scheduling** view of the
**Activities** section.

The **Visit scheduling** view has the following functional areas:

1. **Contact list**. The area displays the list of doctors with scheduled
   visits. To display a list of contacts with a certain system user as owner,
   specify the owner’s full name in the schedule quick filter. The records in
   the list of contacts can be filtered via the **Apply filter** command of the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_roles_actions_menu_0.png)
   menu.

2. **Account list.** The list displays pharmacies and hospitals where you can
   schedule visits. To display a list of accounts with a certain system user as
   owner, specify the owner’s full name in the schedule quick filter. You can
   filter the records in the accounts list by selecting the **Apply filter**
   option from the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_roles_actions_menu_0.png)
   button menu.

3. **Med rep's calendar.** The calendar in the **Visit scheduling** view is
   similar to the standard user calendar. The titles of days in the calendar
   contain additional buttons that allow the user to build the pharmaceutical
   rep's daily route.

4. **Route map.** The map that displays the pharmaceutical rep's daily route.

## Schedule visits automatically​

Use the **Cyclic tasks** section in Pharma Creatio to automatically plan medical
rep visits to pharmacies and physicians. A cyclic task is an activity that
includes multiple visits planned for a certain period of time. You can create
cyclic tasks in the **Cyclic tasks** section. One cyclic task may schedule
multiple visits over a certain period.

note

After installing the "Pharma Creatio" app, make sure you add the **Cyclic
tasks** section to the needed workplaces.

### 1\. Add a cyclic task​

1. Go to the **Cyclic tasks** section.

2. Click the **New task** button.

3. On the displayed page, fill in the required fields. On the displayed page,
   populate the required fields: specify the name of the cyclic task, the start
   and the end dates, and the owner. The owner must be a contact for which the
   system user is created.

4. On the **General information** tab:
   1. Add the visit category. Specify the name of the category in the **Name**
      field.

   2. In the **Quantity** field, specify the total number of visits you want to
      schedule for the selected time frame. The **Days between visits** and the
      **Visits frequency per month** field values are populated automatically.

note

If you change the values in either one of the **Quantity** , **Days between
visits** and the **Visits frequency per month** fields, the values in the other
two fields will be automatically recalculated based on the total task execution
period.

        * Select the lookup value in the **Visit rule** field to specify the rule according to which the visit will be performed. The field is populated from the **Field sales rules** lookup.

        * Select the contacts and accounts in the **Doctors** and **Pharmacies** details.

5. In the **Products** tab, specify a list of products, which the medical rep
   will promote for physicians and pharmacies.

note

During automatic visit planning, the products specified on the **Promoted
products** detail will be promoted instead of those specified on the
**Products** tab of a contact (doctor), or an account (pharmacy) page.

6. Save the cyclic task (Fig. 1).

Fig. 1 Populated cyclic task page

![Fig. 1 Populated cyclic task page](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_cyclic_tasks_planning.png)

note

We recommend planning your visits quarterly to analyze product promotion results
correctly.

### 2\. Schedule med rep visits using cyclic tasks​

After adding a cyclic task. proceed to schedule visits. To do this:

1. Open the cyclic task created on the previous step. Use the **Calculate
   available visits** command of the **Actions** menu on the cyclic task page to
   calculate available visit slots. As a result, Creatio will populate the
   **Available quantity of visits** field of the cyclic task page (Fig. 2)

Fig. 2 Available visit quantity

![Fig. 2 Available visit quantity](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_number_of_available_visits.png)

2. When the calculation is finished, the **Schedule visits** action will become
   available on the cyclic task page (Fig. 3).

Fig. 3 The Schedule visits action

![Fig. 3 The Schedule visits action](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_cyclic_tasks_plan_visits_action.png)

3. Run the **Schedule visits** action to start the process of automatic visits
   scheduling in accordance with the configured parameters and physician and
   medical rep calendars. You will receive a notification when the visits are
   scheduled. The **Quantity of scheduled visits** will display the number of
   scheduled visits. The visit activities will appear on the **Activity** detail
   of the corresponding contacts and accounts.

### Automatic scheduling of visits​

The algorithm for automatic visit planning is as follows:

1. Creatio determines the route starting point. The current location of a sales
   rep responsible for the visit can be a starting point. The location is
   determined based on the information from the **Addresses** detail of the
   corresponding contact page. If the contact’s address is not specified, the
   system will use the address from the connected account page.

2. Creatio determines the closest sales outlet to the starting point. The
   optimal car route is determined within the 200 km radius.

3. Creatio checks the working hours of both the physician (pharmacy) and the
   medical rep.

note

When checking the working hours of visit participants, the system analyzes the
calendars of the medical rep and the doctor.

4. The system will create the first visit if the schedules of the medical rep
   and the physician (pharmacy) coincide.

If the visit time is outside of the working hours of both parties, the system
will look for the next closest location. Further planning and creation of visits
is carried out in the same way.

## Schedule visits manually​

note

Before scheduling visits, make sure that the rule that applies to the visit
corresponds to the needed time period and visit category. Setting up visit rules
is performed in the **Field sales rules** lookup.

To schedule a visit:

1. In the **Activities** section, select the **Visit scheduling** view (Fig. 4).

Fig. 4 Selecting the Visit scheduling view

![Fig. 4 Selecting the Visit scheduling view](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_field_force_open_view.png)

2. On the opened page, in the calendar filter area select the time period and
   the employee to schedule visits for.

3. If you plan a physician visit, select that physician’s contact and drag it to
   the calendar area (Fig. 5).

Fig. 5 Adding a visit to the calendar

![Fig. 5 Adding a visit to the calendar](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_planning_visits_drag_contact.png)

If more than one rule is set up for the period, a rule selection window will
open (Fig. 6).

Fig. 6 Selecting a visit rule

![Fig. 6 Selecting a visit rule](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_planning_visits_type_of_vizit_choice.png)

note

Visit rules are set up in the **Field sales rules** lookup.

As a result, the calendar will contain a new activity with the "Visit" type. The
contact that you dragged on the schedule area will be specified in the
corresponding visit. The list of actions set up in the **Field sales rules**
lookup will be added to the visit. The duration of the visit will correspond to
the value from the corresponding visit rule. If necessary, you can change the
visit duration manually.

4. Pharmacy visits are scheduled in a similar way, by dragging an account to the
   schedule.

note

When the calendar of visits has been changed, use the map to view the changes in
the pharmaceutical rep's route. Canceled visits are not taken into account when
building a route.

To automatically connect a manually created visit to a cyclic task, the
following parameters must coincide:

- visit time frame

- promoted product

- physician and/or pharmacy

If the above parameters are the same in the **Cyclic task** field of the
**Connected to** detail of the **Basic Information** tab of the manually
scheduled visit, the name of the associated cyclic task is displayed.

## Configure a personal calendar​

When planning visits, weekends and business hours are taken into account.
Therefore, it is required to configure calendars prior to planning visit dates.
By default, a single basic calendar with the following characteristics is set up
in the system:

- Time zone GMT 0, without daylight saving time.

- 5-day workweek (from Monday till Friday).

- 8-hour workday (from 9:00 AM to 6:00 PM), without lunch break.

- Workdays with irregular business hours and holidays are not included.

This calendar is specified as default in the **Base calendar** system setting
("BaseCalendar" code). You can modify the standard calendar according to the
working schedule of your company, or create a new one and add it to the system
setting as the default one. Additionally, you can create personal calendars for
pharmacies and doctors who your medical representatives are going to visit. The
**Base calendar** system setting ("BaseCalendar" code) must be filled in for
correct work of calendars. The system will refer to the **Base calendar** system
setting if a contact’s calendar is not configured.

Example

A process of setting up a contact’s personal calendar with a six-day workweek
and a shorter day on Saturday is described below. The lunch break is fixed, its
duration is 1 hour.

To create a new calendar:

1. Select "Calendar" in the **Actions** menu on the contact page.

2. Confirm adding a new personal calendar by clicking **Yes**.  
   The page for setting up the personal calendar of the contact will open. The
   **Name** and **Time zone** fields are populated automatically he **Name**
   field is read-only, but you can change the time zone if necessary.

3. In the **User** field, specify the company rep who will perform visits to the
   contact. Their working hours will be taken into consideration when planning
   visits.

4. Edit the workweek settings. The default week parameters match the parameters
   of the base calendar. Set the day type as "Work" for all days from Monday to
   Friday, "Reduced" for Saturday and "Day off" for Sunday.

5. Set up work time. Set the technical break by separating the work time into
   two intervals, before and after the break: 9:00 AM – 1:00 PM and 2:00 PM –
   6:00 PM.

6. Specify all holidays on the **Days off** tab.

note

The **Calendars** lookup may also be used to configure personal calendars of
contacts. The setup sequence is the same. Open the system designer by clicking
the
![system_designer00008.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/pharma/BPMonlineHelp/chapter_pharma/system_designer00008.png)
button at the top right corner of the application window.

## Build a route for a med rep​

Using the map allows you to save your pharmaceutical reps' time when moving
around the city.

Med outlet is displayed on the map in accordance with the GPS coordinates
specified on the account page. By default, when building routes, Creatio used
the last added address of the pharmacy account.

In case of a physician visit, last added address of the corresponding hospital
account is used. The address is displayed on the **Addresses** detail of the
**Contact info** tab of the contact page.

note

You can view the address of the sales outlet on the map and the title of the
selected visit by clicking the marker of the visit.

When all the visits are added to the map, build a route.

To **view routes for one day** , tap the
![btn_com_map_marker.png](https://academy.creatio.com/guides/sites/default/files/documentation/user/ru/pharma/BPMonlineHelp/chapter_pharma/btn_com_map_marker.png)
button located in the day title of the calendar (Fig. 8).

Fig. 8 Building a route for a med rep

![Fig. 8 Building a route for a med rep](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_field_force_plan_route.png)

As a result, the map will display all visits for the selected day. The order of
visits on the map will correspond to their order in the schedule. The
![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_map_marker_2.png)
button in the day title will change its color. The button color will correspond
to the color of the route on the map. The route color is different for each day.

You can **view routes for several days** by clicking
![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_map_marker_2.png)
for multiple dates.

note

On the map, the point that the route starts from is your current location (your
browser will need permission to share your current location). If your browser
privacy settings do not permit sharing location, the first point of the route is
the value specified in the "Default city for employees" system setting
("EmployeeCityDef" code).

---

## See also​

[Install Pharma Creatio](https://academy.creatio.com/documents?id=1715)

[Set up rules and actions of a med rep visit](https://academy.creatio.com/documents?id=2478)

[Conduct visits](https://academy.creatio.com/documents?id=2480)

[Monitor check-in performance](https://academy.creatio.com/documents?id=2481)

[Categorization of physicians](https://academy.creatio.com/documents?id=2482)

- Schedule visits automatically
  - 1\. Add a cyclic task
  - 2\. Schedule med rep visits using cyclic tasks
  - Automatic scheduling of visits
- Schedule visits manually
- Configure a personal calendar
- Build a route for a med rep
- See also
