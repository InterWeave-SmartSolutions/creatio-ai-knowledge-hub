# Add a financial indicator | Creatio Academy

**Category:** administration **Difficulty:** advanced **Word Count:** 545
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/add-financial-indicator

## Description

Creatio enables users to track financial indicators of the customers, for
example, revenue for a certain time period, net income, account receivables etc.

## Key Concepts

section, lookup, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Sales

On this page

Creatio enables users to track financial indicators of the customers, for
example, revenue for a certain time period, net income, account receivables etc.

Use the **Financial indicators** section to analyze the information about the
number of current accounts with the customer, account balance, total revenue,
amount of accounts receivable and accounts payable and other aggregates of
company activity. The section provides the following features:

- Add new indicators.
- Compare planned and actual indicators.
- Analyze indicator dynamics.
- View data from the perspective of a financial account, customer, or segment.

The **Financial indicators** section provides folders for easy selection of the
time period for the financial indicators.

To add a financial indicator:

1. Navigate to the **Financial indicators** section.

2. Click **Add financial indicator**.

3. Populate the fields on the **General information** tab of the user page:

| Indicator type | Select the type of the financial indicator, for example, "Revenue" or "Number of open accounts". The field is required. To add a new indicator to the lookup, click ![btn_com_lookup.png](https://academy.creatio.com/sites/default/files/documents/docs/product/bpm'online%20bank%20sales/bank%20sales/7.12.0/BPMonlineHelp/section_financial_indicators/btn_com_lookup.png), then click **New** in the dialog box. Specify the name of the indicator on the page that opens and click **Save** to apply the changes. | Value | Specify a numeric value of the financial indicator, for example, the amount of funds. | Currency | Select the currency that the amount of funds is specified in, for example, "Euro." | Type of value | Select the value type of the financial indicator, for example, "Actual" or "Planned." The field is required. | Time period | Specify the time period of the financial indicator. Select the value from the time period lookup.The field is filled in automatically if the values specified in the **Start date** and **End date** fields match a period specified in the lookup. If the lookup does not contain the needed time period, you can add it manually. To add a period to the lookup, click ![btn_com_lookup00001.png](https://academy.creatio.com/sites/default/files/documents/docs/product/bpm'online%20bank%20sales/bank%20sales/7.12.0/BPMonlineHelp/section_financial_indicators/btn_com_lookup00001.png), then **New** in the dialog box. Populate the required fields on the page that opens and click **Save** to apply the changes.You can also add a time period when saving the financial indicator page if the values in the **Start date** and **End date** fields do not match any period specified in the lookup. The system will ask you to confirm adding the time period. | Start date | Populate the start and end dates of the period. These required fields are populated automatically when a value is selected in the **Time period** field. Once the **Time period** field is filled in, the fields become non-editable. | End date | Time period type | The field is populated automatically based on the period specified in the **Start date** and **End date** fields. The field is non-editable if the **Time period** field is filled in. |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

4. If necessary, specify connections to other Creatio records in the **Connected
   to** field group.

| Legal entity | Select the customer that the financial indicator is specified for. | Legal entity segment | Specify the group of customers that the financial indicator is specified for. Select from the folders that are set up in the **Legal entities** section. | Account | Specify the customer's bank account. |
| ------------ | ------------------------------------------------------------------ | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------ |

As a result, a new financial indicator will be added in Creatio.

---

## See also​

[Create an application](https://academy.creatio.com/documents?id=1664)

[Fill out an application](https://academy.creatio.com/documents?id=1681)

[Set up verification actions](https://academy.creatio.com/documents?id=2158)

[Set up the consultation panel](https://academy.creatio.com/documents?id=1620)

- See also
