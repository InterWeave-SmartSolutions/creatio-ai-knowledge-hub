# Create an application | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 756 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/create-application

## Description

In Creatio, you can manage all applications in a single section. Retrieve vital
information about the deal participants, such as their roles and credibility,
and use that information to decide on a deal on a per-application basis.

## Key Concepts

section, detail, role, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer JourneyLending

On this page

In Creatio, you can manage all applications in a single section. Retrieve vital
information about the deal participants, such as their roles and credibility,
and use that information to decide on a deal on a per-application basis.  
The **Applications** section stores all customer information starting with the
initial customer need and up until the deal closure. Use this section to manage
customer applications, view the application history, general information about
customers, and selected products.  
Financial Services Creatio, lending edition, has a default application
processing case designed for consumer loans with preconfigured tasks and hints.
It includes:

- Product selection
- Filling in the application form
- Validation.
- Deal closure.

You can modify the existing case or set up other cases in the section via case
designer.  
An application for bank products is created by the loan processor employee at
the bank office based on the information provided by a borrower. Applications
are created in two stages: quick application creation and filling in the
detailed application information.

Example

A consumer wishes to take a loan of $50,000 for a period of 3 months.

## Create a new application​

1. Click the **New application** button in the **Applications** section.
2. Select the required application type: "Financial accounts and investments" or
   "Loan services."
3. Populate the **Product type** field in the opened mini-page. The other fields
   will be populated automatically. If the customer is interested in the
   products of a different category, change the corresponding value. Information
   about bank subsidiaries and branches is filled in based on the data about the
   place of work of the employee who creates an application (Fig. 1).

Fig. 1 Application mini page

![Fig. 1 Application mini page](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_application_minicard.png)

4. Save the application.

As a result, a new application will be added to the system.

## Fill out the application​

Financial Services Creatio, lending edition, requires the following information:
product, deal participants, and the documents required for the deal before you
can start [processing](https://academy.creatio.com/documents?id=1666) the
application. Creatio uses this information to validate the application, during
which the final decision on the deal is made.

### Select product​

On the new application page, you will be asked to fill in the information about
the selected product. The corresponding activity will be displayed on the action
panel. Ask the customer about the product and its conditions. Enter the
information on the application page:  
On the application page, fill out the **Selected product** tab.

1. Specify the product for which the application is created. Only products whose
   [category and type](https://academy.creatio.com/documents?id=2156) coincide
   with those specified during application creation are available for selection
   in the **Products** field. If the terms of sale are set for the selected
   product, select the product with the most suitable conditions in the list. In
   this case, we select the Lending/Consumer lending/Short-term loans. After
   selecting a product, the list of conditions on the application page will be
   filled in automatically.
2. Specify the currency of the loan, its amount, term, and other required
   parameters. In our case, it is a $50 000 loan for 3 months (Fig. 2).

Fig. 2 An example of filled out [Selected product] tab

![Fig. 2 An example of filled out [Selected product] tab](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_product_conditions.png)

### Submit the application form​

Fill in the information about deal participants after entering the product
information in the application. You can do this on the "Filling in the
application form" stage.  
On the "Filling in the application form" stage, another activity will be
created. When you click on the activity, the automatically created borrower
application form will open. Fill out the application form. A list of documents
for the borrower will be generated automatically. Learn more in the
["Fill out the application form"](https://academy.creatio.com/documents?id=1665)
article. When the application form is saved, you will be asked to send the
application for validation:

1. If all information on the application has been entered, click **Yes** →
   **Save**. The application will enter the "Validation" stage.
2. To add information to the application (for example, the "Guarantor"
   application form), click the **Perform later** button and specify the start
   time, activity duration, and reminder time. The created task will appear on
   the application action panel.
3. If the application requires significant revision, click **No**. After
   revising the application, send it for validation by clicking on the
   corresponding stage of the indicator on the application page.  
   The application page provides a complete list of documents for all deal
   participants. The list of documents for each participant is available on the
   application form page.

---

## See also​

[Process an application](https://academy.creatio.com/documents?id=1666)

[Fill out an application](https://academy.creatio.com/documents?id=1681)

- Create a new application
- Fill out the application
  - Select product
  - Submit the application form
- See also
