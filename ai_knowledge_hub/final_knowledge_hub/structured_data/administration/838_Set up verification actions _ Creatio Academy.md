# Set up verification actions | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 556
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/set-up-verification-actions

## Description

Validation actions may differ for applications for different products. You can
configure the required parameters for existing validation actions or create new
ones to match the actions performed by the verifier with the bank's security
policy.

## Key Concepts

detail, lookup, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Lending

On this page

Validation actions may differ for applications for different products. You can
configure the required parameters for existing validation actions or create new
ones to match the actions performed by the verifier with the bank's security
policy.

## Add new validation actions​

To create new validation action:

1. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_5.png)
   to open the System Designer.
2. Click the **Lookups** link in the **System setup** block.
3. Open the **Validation items** lookup.
4. Click the **New validation action** button.
5. Specify the name of the new validation action and save it by clicking on the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_2.png)
   button.

As a result, a new validation action will be added to Creatio. You can also
enrich the validation action with a conversation script, control questions, and
any attachments.

### Add a conversation script​

Conversation scripts are created by the verifier supervisor. They used the
employees as the basis for the conversation while checking the data of the
participants of the deal. To add the conversation script to the validation
action:

1. Open the **Validation items** lookup and select the action to which the
   conversation script will be added. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_2.png).
2. On the opened edit page, select the **Conversation script** tab.
3. Enter the conversation script text.
4. Save the changes.

As a result, the conversation script will be available in the validation action
window on the application page.

### Add control questions​

The checklist is needed to commit the validation results. To add the checklist
to the validation action:

1. Open the **Validation items** lookup and select the action to which the
   checklist will be added. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_2.png).
2. On the opened edit page, select the **Check list** tab. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_chapter_mobile_wizard_new_role_2.png).
3. Enter the question and specify if it is required. If the answer to the
   required question is not specified in the validation action window, the
   verifier will not be allowed to save the results of the action.  
   When adding questions, take into account that they have "Yes", "No" and
   "Other" configured answers. In the case of the latter, a comment field will
   appear near the question.
4. Repeat steps 1 through 3 to add all the questions.
5. Click **Save**.

### Add attachments to the validation action​

You can attach files (for example, regulatory documentation, internal
regulations of the bank, instructions, examples of successful implementation of
the validation action by bank employees, etc.) to validation actions. To do
this:

1. Open the **Validation items** lookup and select the action to which the
   attachments will be added. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_edit_2.png).
2. On the opened edit page, select the **Attachments** tab.
   - To add a file to the validation action, click the
     ![](https://academy.creatio.com/docs/sites/default/files/inline-images/icn_add_attachment_2.png)
     button on the **Attachments** detail and upload the file. You can also drag
     the file and drop it on the detail.
   - To add a link to the validation action, click the
     ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_roles_actions_menu_1.png)
     button on the **Attachments** detail. On the displayed page, enter the link
     address in the **Name** field and save the page. As a result, the link will
     be added to the detail.
3. Repeat step 2 for all files and links to add them to the validation action.
4. Click **Save**.

As a result, the attachments will be available in the validation action window
on the application page.

---

## See also​

[Create an application](https://academy.creatio.com/documents?id=1664)

[Set up the consultation panel](https://academy.creatio.com/documents?id=1620)

[Conduct a consultation](https://academy.creatio.com/documents?id=1621)

- Add new validation actions
  - Add a conversation script
  - Add control questions
  - Add attachments to the validation action
- See also
