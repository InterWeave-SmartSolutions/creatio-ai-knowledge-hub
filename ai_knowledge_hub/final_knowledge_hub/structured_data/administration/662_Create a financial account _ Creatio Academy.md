# Create a financial account | Creatio Academy

**Category:** administration **Difficulty:** advanced **Word Count:** 341
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-products/create-financial-account

## Description

The Financial accounts section is used to store information about the bank
accounts of your customers. Here, you can update and retrieve any important data
about a bank account, including its number, customer's name, the current status
of the account.

## Key Concepts

section, detail, lookup, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer JourneyLendingBank Sales

On this page

The **Financial accounts** section is used to store information about the bank
accounts of your customers. Here, you can update and retrieve any important data
about a bank account, including its number, customer's name, the current status
of the account.

To add a bank account:

1. Open the **Financial accounts** section and click **New financial account**.

2. On the opened card setup page, specify the general information about the
   account:

| Account number | Unique financial account number. The field is required. | Contract | The contract for which the financial account was opened. The field is required. | Customer | An individual or legal entity whose account this is. The field is required. | Product | Name of the banking product that is connected to the financial account. The field is non-editable and is populated automatically with the product specified in the contract. The field is required. |
| -------------- | ------------------------------------------------------- | -------- | ------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

3. On the **General information** tab, specify the main bank account
   information:

Type| Account type, for example, "Deposit", "Card", "Credit". The field is
required.| Currency| The currency of the account. The field is required.|
Balance| Actual financial account balance.| Branch| Name of the branch or office
in which a financial account is opened. Fields lookups contain the lists of
legal entities of the "Our bank" type.| Office

---

4. Populate the following fields on the **Status** detail on the **General
   information** tab.

| Opened on | Dates on which the current financial account was opened and activated. | Activated on | Status | Status of the current financial account, for example, "Active", "Blocked", "Closed". By default, the "Active" value is set. The field is required. |
| --------- | ---------------------------------------------------------------------- | ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |

5. If necessary, add the [cards](https://academy.creatio.com/documents?id=1076)
   that are connected to this bank account to the **Cards** detail.

6. On the **Attachments and notes** tab, add more information about the bank
   account, as well as attachments and links to the web resources related to the
   bank account.

7. Click **Save**.

As a result, a new financial account record will be added to Creatio.

---

## See also​

[Create a card](https://academy.creatio.com/documents?id=1076)

[Form bank product categories and types](https://academy.creatio.com/documents?id=1921)

- See also
