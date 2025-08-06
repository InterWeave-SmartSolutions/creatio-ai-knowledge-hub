# Process an application | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 438 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/process-application

## Description

After all, information has been filled in, the application processing starts.
The processing is performed in three steps:

## Key Concepts

detail, lookup, role, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer JourneyLending

On this page

After all, information has been filled in, the application processing starts.
The processing is performed in three steps:

- Validation
- Approval
- Deal closure

After all these steps are completed, the application will be closed.

## Application validation​

At the validation stage, the information provided by deal participants is
verified. The validation results are entered on the **Validation** detail of the
application page.  
On the "Validation" stage in the action panel of the application page, a task
will be created. When you click on the task title, a validation action window
will open (Fig. 1). The window will display a field group with general
validation results. If the **Validation items** lookup contains files for the
current action (for example, regulations or guidelines), they will be displayed
in the validation window.

Fig. 1 Application validation

![Fig. 1 Application validation](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_validation_action.png)

In the validation window:

1. Fill in the **Result** field group.
2. Specify the action decision by clicking **Confirmed**.
3. Click the **Complete** button to save the result.

If you need to validate other data for the application, enter the validation
results manually. To do this:

1. On the application page, open the **Application decision** tab.
2. On the **Validation** detail, click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_add_tab_8.png)
   button.
3. On the opened validation page, select the validation action you want to
   perform, for example, "Verify contact’s communication options."
4. Specify the results, for example, "Confirmed".
5. Set the role of the verifier, for example, "Security", and the employee who
   performed the validation.
6. Fill in the **Application participant role** and **Participant** fields with
   information about the contact whose application form was verified.

You can also leave a comment on the verification results. For example, leave a
comment that specified communication options are not primary (Fig. 2).

Fig. 2 Filled in validation page example

![Fig. 2 Filled in validation page example](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_verification_page.png)

## Application approval​

At the approval stage, the application's initial information and its validation
results are analyzed. The analysis results are the basis for the decision on
whether to close or cancel the deal. The information about the decision is
recorded in the **Application decision** tab of the application page.

## Deal closure​

The deal closure is the final stage of application processing. As a result of
the validation and approval of sale conditions, the agreement documents are
issued. When the agreement is signed, the application is closed.  
When you proceed to the "Settlement" stage, the activity that will be displayed
on the action panel of the application page and the agreement connected to that
activity will be created automatically.

---

## See also​

[Create an application](https://academy.creatio.com/documents?id=1664)

[Set up verification actions](https://academy.creatio.com/documents?id=2158)

[Set up the consultation panel](https://academy.creatio.com/documents?id=1620)

[Conduct a consultation](https://academy.creatio.com/documents?id=1621)

- Application validation
- Application approval
- Deal closure
- See also
