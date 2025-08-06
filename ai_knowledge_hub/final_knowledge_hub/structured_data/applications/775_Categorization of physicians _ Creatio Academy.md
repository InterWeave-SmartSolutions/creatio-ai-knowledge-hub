# Categorization of physicians | Creatio Academy

**Category:** applications **Difficulty:** intermediate **Word Count:** 819
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/pharma/categorization-of-physicians

## Description

Information about a doctor’s potential significance in terms of pharmacy product
promotion is critical for choosing a proper communication strategy with the
doctors. In Creatio, this information is available on the doctor’s contact page,
in the Potential, Loyalty and Category fields.

## Key Concepts

section, detail, lookup, contact

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Information about a doctor’s potential significance in terms of pharmacy product
promotion is critical for choosing a proper communication strategy with the
doctors. In Creatio, this information is available on the doctor’s contact page,
in the **Potential** , **Loyalty** and **Category** fields.

The **Potential** field contains doctor’s estimated potential, which is an
indicator of doctor’s capability to promote pharmacy products. The doctor’s
potential is based on the number of patients with specific diagnoses ("nosology"
or "ICDs") that a medical rep recorded during last visit to that doctor. The
number of patients is compared with the values in the **Doctor’s potential
setup** lookup.

The **Loyalty** field contains a general estimation of doctor’s loyalty towards
your brand. Loyalty is an indicator of how actively the doctor promotes your
products. By default, the loyalty can range from "1" (highest) to "3" (lowest).
The loyalty value is calculated based on the actual prescriptions of your
products by the doctor. The number of prescriptions is compared to the values in
the **Doctor’s loyalty setup** lookup.

The values in the **Potential** and **Loyalty** fields are calculated
automatically during doctor categorization.

The regional manager analyzes the "potential" and "loyalty" indicators and
assigns doctor’s category. Information about previously assigned categories is
automatically saved on the **Categorization history** detail on the contact’s
page.

## Set up calculation of a doctor’s potential and loyalty indicators​

A doctor’s **potential** indicator depends on the number of patients with
various diagnoses who visited the doctor. To set up calculation of the doctor’s
potential:

1. Open system designer. For example, click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_1.png)
   button.

2. Go to the **Lookups** section and open the **Doctor’s potential setup**
   lookup.

3. Add new lookup records and specify the values of doctor’s potential in the
   desired format. By default, there are three levels of potential (from highest
   to lowest): "A", "B" and "C".

4. Select the doctor specialty, for which the potential value is relevant.

note

Set up separate rules of calculating potential for different doctor specialties.

5. Assign the value range for the number of patients that visit a doctor of the
   selected specialty between the measurements (usually taken by a medical rep
   during visits).

note

To let medical reps enter data for calculation of potential, set up a connection
between the doctor specialties and diagnoses (nosology) of the patients that
visit each type of doctor. To do this, edit the records in the **Nosology**
lookup.

The doctor’s **loyalty** indicator depends on the number of prescriptions for
the promoted products the doctor makes between the medical rep’s visits. To set
up calculation of the doctor’s loyalty:

1. Open system designer. For example, click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_1.png)
   button.

2. Go to the **Lookups** section and open the **Doctor’s loyalty setup** lookup.

3. Add new lookup records and specify the values of doctor’s loyalty in the
   desired format. By default, the loyalty can range from "1" (highest) to "3"
   (lowest).

4. Select the doctor specialty, for which the potential value is relevant.

note

Set up separate rules for calculating loyalty for different doctor specialties.

5. Assign the value range for the number of prescriptions that a doctor of the
   selected specialty issues between measurements (usually taken by a medical
   rep during visits).

note

To let pharmaceutical reps enter data for calculation of doctor’s loyalty, enter
the list of the promoted products in Creatio. You can do this by adding the
products to the **Promoted products** detail on the **Products** tab of the
doctor’s contact page, or by adding doctors to the **Contacts** detail of the
product page.

## Perform doctor categorization​

Doctor’s category is assigned by a regional manager and is based on analysis of
the doctor’s potential and loyalty indicators. The doctor’s potential and
loyalty are calculated based on the information about the number of doctor’s
patients and the number of prescriptions of the promoted products issued by the
doctor. The information is gathered by medial reps during visits. Creatio
automatically assigns the doctor’s potential value if the number of patients is
within the range specified for this value in the **Doctor’s potential setup**
lookup.

To perform doctor categorization:

1. Select one or more doctor records in the **Contacts** section.

note

You can also run the categorization action from the contact page, if a contact
with the "Doctor" type is opened.

2. Click the **Actions** button and select **Categorize**.

As a result, doctor’s potential and loyalty indicators will be calculated. The
categorization will run on the background, and you will be notified when it
completes.

3. Select doctor’s category based on the calculated potential and loyalty
   indicators. Information about previously assigned categories is automatically
   saved on the **Categorization history detail** on the contact’s page.

note

You can set up the list of categories in the **Contact category** lookup.

---

## See also​

[Install Pharma Creatio](https://academy.creatio.com/documents?id=1715)

[Set up rules and actions of a med rep visit](https://academy.creatio.com/documents?id=2478)

[Schedule med rep visits](https://academy.creatio.com/documents?id=2479)

[Conduct med rep visits](https://academy.creatio.com/documents?id=2480)

- Set up calculation of a doctor’s potential and loyalty indicators
- Perform doctor categorization
- See also
