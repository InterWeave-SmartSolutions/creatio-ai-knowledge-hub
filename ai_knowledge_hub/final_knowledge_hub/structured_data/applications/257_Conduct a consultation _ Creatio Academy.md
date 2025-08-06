# Conduct a consultation | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 360 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/conduct-consultation

## Description

During a consultation with a client, you can create a new client record in the
system and sell a product. You can also interrupt the consultation and continue
it at a later time.

## Key Concepts

business process, detail, lookup, database, contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer Journey

On this page

During a consultation with a client, you can create a new client record in the
system and sell a product. You can also interrupt the consultation and continue
it at a later time.

## Start a consultation​

1. Click the **Start consultation** button (Fig. 1). The button is available if
   the client was found in the database.

Fig. 1 Beginning a consultation

![Fig. 1 Beginning a consultation](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_start_process.png)

If the client was not found, the consultation process will start as soon as the
manager clicks the **New customer** button.  
After the manager starts the consultation, the contact page will open. The
system will automatically create a case, in which all consultation themes will
be recorded.

2. Select the product name in the consultation panel block (Fig. 2).

Fig. 2 Selecting a theme in the consultation panel

![Fig. 2 Selecting a theme in the consultation panel](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_choose_product.png)

When you click a theme in the consultation block, the system runs the business
process specified for that theme in the **Consultation theme blocks** lookup.

## Postpone the consultation​

Click the **Postpone** button (Fig. 3) to postpone a consultation for a later
time.

Fig. 3 Postponing a consultation with the client

![Fig. 3 Postponing a consultation with the client](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_pausa.png)

The consultation timer will pause and the postponed consultation will appear in
the **Continue consultation** block.

note

The **Continue consultation** block can contain multiple postponed
consultations.

Click the **Continue** button in the **Continue consultation** block (Fig. 4) to
resume the selected consultation.

Fig. 4 Resuming a consultation

![Fig. 4 Resuming a consultation](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_start_process.png)

## Complete the conversation​

To complete the consultation, click the **End** button (Fig. 5).

Fig. 5 Completing a consultation

![Fig. 5 Completing a consultation](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_finish.png)

The status of the consultation will be changed to **Closed**.

## Handle consultation results​

After you complete the consultation, a page will open where you can enter the
consultation results and close the corresponding case (Fig. 6).

Fig. 6 Page for entering the consultation results

![Fig. 6 Page for entering the consultation results](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_results.png)

To enter results for the consultation:

1. Click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_chapter_mobile_wizard_new_role_3.png)
   button on the **Consultation themes** detail.
2. Select the consultation theme in the **Theme** field.
3. Enter the result of consultation regarding the selected theme in the
   **Result** field.
4. Click the **Complete** button.

---

## See also​

[Set up the consultation panel](https://academy.creatio.com/documents?id=1620)

- Start a consultation
- Postpone the consultation
- Complete the conversation
- Handle consultation results
- See also
