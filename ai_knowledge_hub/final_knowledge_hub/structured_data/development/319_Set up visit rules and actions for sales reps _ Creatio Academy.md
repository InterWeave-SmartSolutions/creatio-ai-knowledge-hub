# Set up visit rules and actions for sales reps | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 970 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/field-management/set-up-visit-rules-and-actions-for-sales-reps

## Description

One of the primary components of a visit rule is the sale rep "to-do" list – the
activities that sales reps are required to complete during a visit. This
functionality lets field staff perform the following basic actions on their
mobile devices:

## Key Concepts

section, detail, lookup, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

One of the primary components of a visit rule is the sale rep "to-do" list – the
activities that sales reps are required to complete during a visit. This
functionality lets field staff perform the following basic actions on their
mobile devices:

| Check-in | Creatio receives GPS coordinates of the sales rep's location and the visit status is changed to "In progress." | Presentation | Opens a PowerPoint or PDF presentation on the sales rep's mobile device (the presentation must be added to the **Attachments and notes** detail of the visit record in the **Activities** section). If several presentations have been added to the detail, the sales rep will have to select the needed one. | Check-out | Creatio receives the GPS coordinates of the sales rep's location and the visit status is changed to "Completed." |
| -------- | -------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------- |

You can supplement the list of sales rep visit actions by adding new records to
the **Visit actions type** lookup. Employees mark visit actions as "complete" by
toggling a switch in the mobile device. The connection between visit actions and
system sections (e.g., creating a new contract based on a visit action) is
carried out only through development.

## Set up a med rep visit rule​

1. Click
   ![btn_system_designer.png](https://academy.creatio.com/docs/sites/default/files/documentation/user/ru/field_sales/BPMonlineHelp/field_sales_set_rules_and_actions/btn_system_designer.png)
   to open the System Designer.

2. Go to the **System setup** block → click **Lookups**.

3. Click the **Field sales rules** lookup.

4. On the lookup content page, click the **New rule** button.

5. Populate the required fields:
   1. Populate the **Name** field, for example, "2nd quarter of 2020 (Downtown)"
      or "1st quarter (Uptown)."
   2. In the **Start** and **Due** fields, specify the time limit of rule
      validity.
   3. Specify visit duration (including travel time) in the corresponding field.
   4. In the **Number of visits** field, enter the approximate number of visits
      of this type that a field staff member can perform during one day.

6. Click **Save**.

7. Similarly, specify the other rules. For example, the rules may vary by the
   due date or depending on the location a sales rep is operating in.

As a result, these rules will be taken into account when building a schedule for
the sales reps.

In the **Visit scheduling** view of the **Activities** section, drag a sales
outlet from the list to the left and drop it into the calendar. The duration of
the visit will be set automatically, according to the **Visit duration** value
from the corresponding visit rule.

If several rules can be applied to a sales outlet, Creatio will let you choose
which rule to use.

## Manage med rep visit actions​

Use the **Field visit rules** lookup to set up the list of activities that must
be completed during a visit.

To add an action:

1. Click
   ![btn_system_designer00001.png](https://academy.creatio.com/docs/sites/default/files/documentation/user/ru/field_sales/BPMonlineHelp/field_sales_set_rules_and_actions/btn_system_designer00001.png)
   to open the System Designer.

2. Go to the **System setup** block → click **Lookups**.

3. Click the **Field sales rules** lookup.

4. Select a rule to form an action and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit.png)
   (Fig. 1).

Fig. 1 Open a rule for editing

![Fig. 1 Open a rule for editing](https://academy.creatio.com/docs/sites/en/files/documentation/user/en/field_module/BPMonlineHelp/chapter_field_force/scr_field_force_edit_rule.png)

5. On the rule page, expand the **Actions during visit** detail and click the
   **Add** button.

6. Populate the columns of the new record:
   1. Select the visit action type "Check-in," "Check-out," "Presentation," etc.

   2. Use the **Actions priority order** column, to set up sequence of sales rep
      activities. For example, if the action is the first in the "to-do" list,
      enter "1."

   3. Select the **Required** checkbox for the actions that should not be
      skipped during a visit.

The sales rep will not be able to complete the visit until all the required
actions are performed.

7. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_apply.png)
   to save the visit action.

8. Similarly, add the rest of the visit actions.

As a result, when you drag a sales outlet and drop it into the calendar in the
**Visit scheduling** view of the **Activities** section, the **Visit actions**
detail of the visit will be populated automatically. The list of actions on the
detail will correspond to the list of actions set up in the lookup.

## Add a presentation to a visit​

The "Presentation" visit action requires additional setup so that the field
staff members have full access to the presentation materials.

In the system, create a knowledge base article and add a PowerPoint presentation
(\*.pptx) or PDF file on its **Attachments** detail. Then, link the article to
the "Presentation" visit action. As a result, your sales reps will be able to
show the attached presentation from their mobile device during visits.

note

You can add not just PowerPoint presentations but also any other documents to
the knowledge base article. In this case, when performing the "Presentation"
action, this document will be opened using the default applications for that
file type on the mobile device.

To add a presentation:

1. Click
   ![btn_system_designer00002.png](https://academy.creatio.com/docs/sites/default/files/documentation/user/ru/field_sales/BPMonlineHelp/field_sales_set_rules_and_actions/btn_system_designer00002.png)
   to open the System Designer.

2. Go to the **System setup** block → click **Lookups**.

3. Click the **Field sales rules** lookup.

4. Open the needed rule and go to the **Actions during visit** detail.

5. Select the "Presentation" record and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit.png).

6. On the displayed page, expand the **Presentation** detail and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_chapter_mobile_wizard_new_role.png).

7. In the displayed string, click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_lookup.png)
   in the field.

8. In the displayed lookup, select a knowledge base article with an attached
   presentation.

9. If necessary, add other knowledge base articles with attachments.

As a result, when a field staff member performs the **Presentation** visit
action, the PowerPoint presentation (or any other document) attached to the
knowledge base article will open on their mobile device. All presentations and
materials will be available on the **Attachments and notes** detail of the
visit.

Also, all visits planned in the calendar (the **Visit scheduling** view of the
**Activities** section), will have links to the knowledge base articles
specified on the **Attachments and notes** detail.

---

## See also​

[Install Field Management for Creatio](https://academy.creatio.com/documents?id=1374)

[Schedule sales rep visits](https://academy.creatio.com/documents?id=2333)

[Set up visit actions for sales reps](https://academy.creatio.com/documents?id=2332)

[Check-in verification for sales reps](https://academy.creatio.com/documents?id=2335)

- Set up a med rep visit rule
- Manage med rep visit actions
- Add a presentation to a visit
- See also
