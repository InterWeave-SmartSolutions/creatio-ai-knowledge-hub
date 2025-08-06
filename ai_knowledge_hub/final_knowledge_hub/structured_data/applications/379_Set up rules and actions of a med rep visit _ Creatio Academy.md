# Set up rules and actions of a med rep visit | Creatio Academy

**Category:** applications **Difficulty:** beginner **Word Count:** 1550
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/pharma/set-up-rules-of-a-med-rep-visit

## Description

Visit rules determine the different types of visits and med rep’s "to-do" list
for each visit type. This enables you to plan med rep visits with a few clicks,
as Creatio will populate the properties of each visit automatically, according
to applicable visit rule.

## Key Concepts

section, detail, lookup, contact, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Visit rules determine the different types of visits and med rep’s "to-do" list
for each visit type. This enables you to plan med rep visits with a few clicks,
as Creatio will populate the properties of each visit automatically, according
to applicable visit rule.

You can set up rules for physician and pharmacy visits, as well as the list of
activities that your employees must follow during visits. For example, the first
step of any visit is the "Check-in" action, which confirms that the med rep has
actually arrived at the visit site. Completing this action will automatically
save the information about the employee's location. Other visit activities may
include presentation of new products, order placement and "Check-out".

1. Open the system designer by clicking
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_0.png)
   in the top right corner of the application window.

2. Click the **Lookups** link in the **System setup** block.

3. Click the **Field sales rules** lookup.

4. On the lookup content page, click the **New rule** button.

5. Populate the required fields:
   1. Populate the rule name, for example, "Visit to a doctor rule — I quarter".

   2. In the **Start** and **Due** fields, specify the time limit of rule
      validity.

   3. Specify visit duration (including travel time) in the corresponding field.
      The specified duration will be used by the system when creating visit
      activities.

   4. In the **Number of visits** field, enter the approximate number of visits
      of this type that a med rep can perform during one day.

   5. In the **Visit category** field, select the "Visit to the doctor" or
      "Visit to the pharmacy" value.

6. Save the changes.

7. Similarly, specify the other rules. Normally, different visit rules apply to
   different periods and locations.  
   As a result, these rules will be taken into account when building a schedule
   for the med reps. If several rules can be applied to a sales outlet, Creatio
   will let you choose which rule to use.

## Manage med rep visit actions​

A list med rep’s actions during a visit is set up on the **Actions during
visit** detail of the **Field sales rules** lookup.

To add an action:

1. Open the **Field sales rules** lookup.

2. Select a rule to form an action and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_0.png)
   (Fig. 1).

Fig. 1 Open a rule for editing

![Fig. 1 Open a rule for editing](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_edit_rule.png)

3. On the rule page, expand the **Actions during visit** detail and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_add_tab.png).

4. Populate the columns of the new record:
   1. Select the visit action type "Check-in", "Check-out" "Presentation" or
      "Number of patients."

   2. To set up sequence of med rep activities, use the **Actions priority
      order** field.

   3. Select the **Required** checkbox for the actions that the med rep should
      not be able to skip. The med rep will not be able to complete the visit
      until all the required actions are performed.

5. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_apply_0.png)
   to save the visit action.

6. Similarly, add the rest of the visit actions.

As a result, when planning visits in the **Activities** section, the **Visit
actions** will be populated automatically. The list of actions on the detail
will correspond to the list of actions set up in the lookup for the
corresponding visit rule.

The **Action types** lookup contains a pre-configured list of actions performed
during a visit to a doctor or pharmacy These actions are available by default
when setting up actions for physician or pharmacy visits on the **Actions during
visit** detail of the **Field sales rules** rules. You can supplement the list
of available action types by adding the needed types to the **Action types**
lookup. Med rep can complete an action by toggling a switch in the mobile
device. The connection between visit actions and system sections (e.g., creating
a new contract based on a visit action) is carried out only through development.

### Pre-configured rules for "Visit to the doctor"​

| Check-in | When the action is performed, the system receives the GPS coordinates of the med rep's location and the visit is assigned the "In progress" status. | Presentation | When the action is performed, a PowerPoint or PDF presentation will open on the mobile device if it has been added to the **Attachments and notes** detail of the visit. | Number of patients | A pharmaceutical rep, based on the information from a physician specifies the number of patients that the physician treats regularly and whose diagnoses requires treatment by the promoted product. Based on this value, the doctor is categorized. | Promoted products | When performing this action during visits, a pharmaceutical rep, based on the information from a physician specifies how many units of promoted products has the physician prescribed since the last visit.. Based on this value, the doctor is categorized. | Check-out | When the action is performed, the system receives the GPS coordinates of the med rep's location and the visit is assigned the "Completed" status. |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |

### Pre-configured rules for "Visit to the pharmacy"​

| Check-in | When the action is performed, the system receives the GPS coordinates of the med rep's location and the visit is assigned the "In progress" status. | Presentation | When the action is performed, a PowerPoint or PDF presentation will open on the med rep's mobile device if it has been added to the **Attachments and notes** detail of the visit. | SKU Monitoring | Opens the SKU monitoring window for the med rep to enter changes in SKUs and specify whether the products are on display in a pharmacy. | Check-out | When the action is performed, the system receives the GPS coordinates of the med rep's location and the visit is assigned the "Completed" status. |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |

## Add a presentation to a visit​

Set up the **Presentation** action to enable the pharmaceutical reps show
presentation from a mobile device during visits.

Create a knowledge base article and add a PowerPoint presentation (\*.pptx) or
PDF file on its **Attachments** detail. Then, connect the article to the action.
As a result, during a visit the presentation will open automatically on the
mobile device.

note

You can add not only PowerPoint presentations or PDF files but also any other
document to the knowledge base article. When performing the "Presentation"
action, this document will be opened using the standard applications of the
mobile device.

To add a presentation to a med rep visit action:

1. Open the system designer by clicking
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_0.png)
   in the top right corner of the application window.

2. Click the **Lookups** link in the **System setup** block.

3. Click the **Field sales rules** lookup.

4. Select the required rule, for example, "Visit to the doctor" and expand by
   clicking the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_1.png)
   button.

5. Open the **Actions during visit** detail.

6. Select the "Presentation" record and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_1.png).

7. On the displayed page, expand the **Presentation** detail and click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_chapter_mobile_wizard_new_role_0.png).

8. In the displayed string, click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_lookup_0.png)
   in the field.

9. In the displayed lookup, select a knowledge base article with an attached
   presentation.

10. If necessary, add other knowledge base articles with attachments.

As a result, the med rep’s mobile device will display the presentation and the
med rep will have access to other added knowledge base articles on the
**Attachments** detail.

## Set up a list of promoted products​

When monitoring SKU, a med rep must only see a list of products promoted via a
doctor or pharmacy. This is done by setting up individual lists of promoted
products for each customer contact or account. There are two ways to do this.

To set up the list of products promoted via **accounts** :

- Go to the **Accounts** detail of the product page and add the list of all
  accounts that promote the product. The information about the product will be
  automatically added to the **Products** detail of an account page.

- Add the promoted products to the **Products** detail of the account page of
  the account where the products must be promoted. The information about
  accounts will be added to the **Accounts** detail of the product page.

To set up the list of products promoted via **contacts** :

- Go to the **Contacts** detail of the product page and add the list of all
  contacts that promote the product. The information about the product will be
  automatically added to the **Products** detail of a contact page.

- Alternatively, add the promoted products to the **Products** detail of the
  contact page of the contact who promotes the product. The information about
  the product will be automatically added to the **Products** detail of a
  contact page.

As a result, the connection between promoted products and accounts/contacts will
be set. During a visit to a pharmacy, when performing the **SKU monitoring**
action, a med rep will see only the products promoted via this account. During a
visit to a doctor, when performing the **Promoted products** action, a med rep
will see only the products promoted via this contact.

note

If an account has more than one subsidiary companies, when adding products to
the **Products** tab of the parent company, added products will appear on the
corresponding tabs of the subsidiary companies. However, when adding new
products to subsidiary company pages, the products will not be added to the
parent company page. When deleting products from the **Products** tab of the
parent company, the products will not be removed from the subsidiary companies’
pages.

---

## See also​

[Install Pharma Creatio](https://academy.creatio.com/documents?id=1715)

[Schedule med rep visits](https://academy.creatio.com/documents?id=2479)

[Conduct visits](https://academy.creatio.com/documents?id=2480)

[Monitor check-in performance](https://academy.creatio.com/documents?id=2481)

[Categorization of physicians](https://academy.creatio.com/documents?id=2482)

- Manage med rep visit actions
  - Pre-configured rules for "Visit to the doctor"
  - Pre-configured rules for "Visit to the pharmacy"
- Add a presentation to a visit
- Set up a list of promoted products
- See also
