# Install Pharma Creatio | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 524
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/pharma/install-pharma-creatio

## Description

Pharma Creatio functionality is designed to efficiently schedule the med reps'
visits to doctors and pharmacies, build routes on the map, manage the visit
activities and assist med reps during the visits.

## Key Concepts

section, detail, lookup, package, contact, account, marketplace

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Pharma Creatio functionality is designed to efficiently schedule the med reps'
visits to doctors and pharmacies, build routes on the map, manage the visit
activities and assist med reps during the visits.

Important

This function is unavailable for the Oracle DBMS.

**Use a mobile device** with the Creatio application installed during your
visits. After selecting the required visit in the calendar, you will be
transferred to the visit page, which will display the visit action list and
switches for each action.

During a visit, the system will prompt the required steps. For example, when
performing the **Presentation** action, the screen will automatically display a
presentation of new products, etc.

During a visit, you can add orders based on visit results, create a list of
products and their number and write down stock keeping unit (SKU) monitoring
results and product facing check results.

You need to install the app from the marketplace to access the field
functionality. To do this:

1. Click
   ![btn_system_designer.png](https://academy.creatio.com/docs/sites/default/files/documentation/user/ru/field_sales/BPMonlineHelp/field_sales_install_app/btn_system_designer.png)
   in the main Creatio application.

2. Click **Installed applications**. The app management page opens.

3. Click **Add application** → **Choose from Marketplace**.

4. Install the "Pharma Creatio" app.

If your Creatio application is deployed on-site, make sure that the application
is not restricted from accessing the Internet, before you attempt to install
"Pharma Creatio." To do this:

1. Grant access to the web site
   [http://marketplace.creatio.com/](https://marketplace.creatio.com/).

2. Install the "Pharma Creatio" app:
   [http://marketplace.creatio.com/app/pharma-creatio](https://marketplace.creatio.com/app/pharma-creatio).

Learn more: [Manage apps](https://academy.creatio.com/documents?id=1836).

Important

Pharma functionality requires at least 1 Pharma Creatio package license. To
access the pharma functionality, all med rep users must be licensed separately.

When the pharma package is installed, several new elements will appear in
Creatio:

For example, the **Contacts** section will now display the "Doctor" and
"Pharmacist" contact types. The contact page will display the **Specialty** ,
**Category** , **Potential** , **Loyalty** fields and the **Categorization
history** detail. Additionally, the **Products** tab with a detail that contains
a list of drugs that are promoted via this contact.

The **Accounts** section will display new account types — "Pharmacy", "Pharmacy
network," and the **Products** tab with a detail containing a list of products
promoted via an account.

The product page **General information** tab will display the **Contacts** and
**Accounts** details. The details contain a list of contacts and accounts that
promote the product. The product page **Categorization** detail will display a
new **Nosology** field. This field is used to specify the disease the medicine
is subscribed for.

The **Accounts** and **Contacts** tabs will become available in the **Visit
scheduling** view of the **Activities** section. The **Contacts** tab shows the
list of physicians. The **Accounts** tab shows the list of pharmacies, pharmacy
networks and hospitals.

The "Pharma" folder in the **Lookups** section will contain the following
lookups: **Doctor potential setup** , **Doctor loyalty setup** , **Nosology** ,
**Doctor specialties**. New activity categories will be added: "Doctor visit"
and "Pharmacy visit.". Two new rules will be added in the field sales lookup:
"Doctor visit rule" and "Pharmacy visit rule".

---

## See also​

[Set up rules of a med rep visit](https://academy.creatio.com/documents?id=2478)

[Schedule med rep visits](https://academy.creatio.com/documents?id=2479)

[Conduct visits](https://academy.creatio.com/documents?id=2480)

[Monitor check-in performance](https://academy.creatio.com/documents?id=2481)

[Categorization of physicians](https://academy.creatio.com/documents?id=2482)

- See also
