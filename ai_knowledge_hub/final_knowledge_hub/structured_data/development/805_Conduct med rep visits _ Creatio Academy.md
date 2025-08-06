# Conduct med rep visits | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 858 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/pharma/conduct-visits

## Description

Pharma Creatio manages med rep’s "to-do" list during the visits and records
results of each activity. While in the field, med reps use mobile devices to
perform visit actions (presentation, SKU monitoring, order placement, etc.) and
report on their results. We recommend that med reps use tablets for the best
experience when working in the field. Visit pages are most informative when
viewed in horizontal layout.

## Key Concepts

section, detail, lookup, role, operation, system setting, mobile app,
synchronization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Pharma Creatio manages med rep’s "to-do" list during the visits and records
results of each activity. While in the field, med reps use mobile devices to
perform visit actions (presentation, SKU monitoring, order placement, etc.) and
report on their results. We recommend that med reps use tablets for the best
experience when working in the field. Visit pages are most informative when
viewed in horizontal layout.

Important

Only the users that are included to the "Sales representatives" role can use the
Pharma features in the mobile app.

Medical rep action results are recorded in Creatio on the **Actions - Visit**
detail of the visit activity page.

note

Use the **Field sales rules** lookup to customize the list of visit actions.

All actions during a visit can be performed in both online and offline modes of
the mobile app. When working
[offline](https://academy.creatio.com/documents?product=mobile&ver=7&id=1390#title-773-5),
you do not need to maintain a constant Internet connection. It is required to
periodically synchronize the mobile application with the main application to
save the changes made when using the mobile device on Creatio server. You can
select the preferable mode in the "Mobile application operation mode" system
setting ("MobileApplicationMode" code).

To synchronize the mobile application with the main application:

1. Make sure that the mobile device has established an Internet connection.

2. Open the **Settings** section of the mobile application.

3. Click the **Synchronization** button.

As a result, the data from the primary application will be displayed in the
mobile app and the primary application will display the records that were
created using the mobile app.

note

Online mode does not require regular manual synchronization.

To perform an action during a visit:

1. Open the visit page.

2. On the **Visit actions** detail, set the switcher next to the needed action
   to the "Completed" position.  
   The switcher of a completed action is highlighted in blue (Fig. 1).

As a result, the visit action will be considered completed. You can finish the
visit once all required actions are completed (you can skip optional visit
actions). A field employee cannot complete a required action unless all
preceding required actions on the agenda have been completed. Once the last
required action is completed, the visit is considered finished. The action that
is not required can be skipped.

Fig. 1 Completing visit actions in the mobile app

![Fig. 1 Completing visit actions in the mobile app](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_mobile_actions_performing.png)

You can finish the visit once all required actions are completed. To perform the
next required action, the previous required action must be completed. As a
result, once the last required action is completed, the visit is considered
finished. The action that is not required can be skipped.

## Show a presentation​

If the visit agenda requires conducting a presentation, the "Presentation"
action becomes available to the employee. To do this, set the switcher next to
the needed action to the "Completed" position.

As a result, a presentation file will open in your mobile app, so you can use it
during the presentation.

## Specify the number of patients​

Filling out the number of patients whose diagnoses require treatment with the
promoted products, is an important visit action, which affects the
categorization of the corresponding physician. Set the switcher next to the
needed action to the "Completed" position to complete the "Number of patients"
action before filling in the actual number.

A window will open with the list of medical conditions (nosology) that the
physician treats and a **Potential** field next to each condition. Specify the
number of patients that you learned from the physician in the **Potential**
field of the corresponding nosology (Fig. 2).

Fig. 2 Completing the Number of patients action

![Fig. 2 Completing the Number of patients action](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_mobile_actions_number_of_patients.png)

## Specify promoted products​

Information about the number of prescriptions of the promoted products is used
to calculate the physician’s loyalty and the corresponding categorization. The
"Promoted products" action is required. To specify the number of prescriptions,
mark the corresponding action as "Completed."

As a result, the app will display the list of promoted products. Enter the
number of prescriptions for each product in the **Prescriptions** field (Fig.
3).

Fig. 3 Completing the Promoted products action

![Fig. 3 Completing the Promoted products action](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_mobile_actions_promoted_products.png)

## Monitor SKU​

During a visit, tap the **SKU Monitoring** action. To do this, set the switcher
next to the needed action to the "Completed" position.

After you complete this action, a page will open, where you can enter how much
of each of the promoted products is left in stock (Fig. 4).

Fig. 4 The SKU monitoring page

![Fig. 4 The SKU monitoring page](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_mobile_actions_sku.png)

You can use your mobile device’s camera to take a **photo of the product
facings** and attach it to the visit. To do this:

1. On the section page, click the **Edit** button (Fig. 5).

Fig. 5 Opening a visit for editing

![Fig. 5 Opening a visit for editing](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/pharma/scr_pharma_mobile_actions_sku_edit_button.png)

2. On the **Attachments** detail, click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_ff_add_0.png)
   button.

3. Select the photo you made earlier and attach it to the activity. You can also
   use the **Take picture** action. The mobile device will switch to its camera
   mode. The picture taken will be automatically added to the **Files** detail.

---

## See also​

[Install Pharma Creatio](https://academy.creatio.com/documents?id=1715)

[Set up rules and actions of a med rep visit](https://academy.creatio.com/documents?id=2478)

[Schedule med rep visits](https://academy.creatio.com/documents?id=2479)

- Show a presentation
- Specify the number of patients
- Specify promoted products
- Monitor SKU
- See also
