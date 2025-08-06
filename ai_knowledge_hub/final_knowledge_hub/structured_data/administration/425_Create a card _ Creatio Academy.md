# Create a card | Creatio Academy

**Category:** administration **Difficulty:** beginner **Word Count:** 591
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-products/create-a-card

## Description

The Cards section stores information about bank cards. Use this section to view
the type of the card, its payment system, current status, expiration date,
linked accounts, and other important information.

## Key Concepts

section, detail, lookup, contact, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer JourneyLendingBank Sales

On this page

The **Cards** section stores information about bank cards. Use this section to
view the type of the card, its payment system, current status, expiration date,
linked accounts, and other important information.  
To add a card:

1. Open the **Cards** section and click **New card**.

2. On the opened card setup page, specify the general information about the
   card:

| Card number | Card number. The field is required. | Contract | The contract under which the card has been issued. The field is required. | Customer | Contact or legal entity who is the owner of the card account. This field is non-editable and filled in automatically with the contact or legal entity specified in the contract. The field is required. | Product | Product for which the card has been issued. This field is non-editable and filled in automatically with the product specified in the contract. The field is required. | Primary | If a client has a number of cards for the same card account, select this checkbox for the primary card. |
| ----------- | ----------------------------------- | -------- | ------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------- |

3. On the **General information** tab, specify the card data:

| Type | Card type, "Credit" or "Debit". The field is required. | Payment system | Payment system type, for example, "Visa" or "MasterCard". The field is required. | Card category | Card category, for example, "VisaElectron" or "MasterCardGold". The **Card category** and **Payment system** fields are connected. If the **Card category** field is filled in, the **Payment system** field is filled in automatically. If the **Payment system** field is filled in, the **Card category** field displays only the categories that correspond to the selected payment system type. You can associate a card category with a payment system in the **Card categories** lookup. The field is required. | Cardholder | The contact who uses the card. | First and last name | First and last name of the cardholder, as printed on the card. | Branch | Branch that the card is serviced by. You can select legal entities of the "Our bank" type. | Office | The office that the card is serviced by. You can select legal entities of the "Our bank" type. | PayPass / PayWave | Select this checkbox if the wireless payments are enabled for this card. | Primary | If a client has a number of cards for the same card account, select this checkbox for the primary card. | Multicurrency | If a client has a number of cards for the same card account, select this checkbox for the primary card. |
| ---- | ------------------------------------------------------ | -------------- | -------------------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------ | ------------------- | -------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------- |

4. Use the same tab to add more information about the card:

| Status | Current card status, for example, "Active" or "Blocked." By default, the card will be "Active." The field is required. | Opened on | The date the card was issued on. | Valid until | Card expiration date. | Balance | The balance on the card account. | ATM withdrawal limit | Maximum cash withdrawal can be made from an ATM with this card. | Debt | Credit card debt. |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | --------- | -------------------------------- | ----------- | --------------------- | ------- | -------------------------------- | -------------------- | --------------------------------------------------------------- | ---- | ----------------- |

5. Populate the following fields on the **Status** detail on the **General
   information** tab.

| Opened on | The date the card was issued on. | Valid until | Card expiration date. | Status | Current card status, for example, "Active" or "Blocked". |
| --------- | -------------------------------- | ----------- | --------------------- | ------ | -------------------------------------------------------- |

6. If necessary, add the list of cards that are connected to this card to the
   **Linked cards** detail.

7. On the **Attachments and notes** tab, add more information about the card, as
   well as attachments and links to the web resources related to the card. For
   example, you can attach documents that reflect the history of interaction
   with the cardholder.

8. Click **Save**.

As a result, a new card record will be added to Creatio.

---

## See also​

[Create a financial account](https://academy.creatio.com/documents?id=1078)

- See also
