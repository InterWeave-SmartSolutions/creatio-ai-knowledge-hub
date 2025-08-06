# Matomo tracking solution | Creatio Academy

**Category:** applications **Difficulty:** beginner **Word Count:** 2075
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/marketing-tools/lead-generation/landing-pages/website-tracking/matomo-tracking-solution

## Description

In Creatio, you can use Matomo tracking service to collect detailed reports on
your website and its visitors using web form submissions. The reports include
the search engines and keywords the visitors used, the language they speak,
which pages they like, and the files they download. You can also identify
contacts who follow links in bulk emails if you use Marketing Creatio products.

## Key Concepts

business process, section, detail, lookup, dashboard, integration, system
setting, synchronization, campaign, lead

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Marketing

On this page

In Creatio, you can use Matomo tracking service to collect detailed reports on
your website and its visitors using web form submissions. The reports include
the search engines and keywords the visitors used, the language they speak,
which pages they like, and the files they download. You can also identify
contacts who follow links in bulk emails if you use Marketing Creatio products.

You can use Matomo data associated with specific Creatio contacts to personalize
product and service offers as well as improve your website UX. For example:

- **Evaluate** which products or services interest the contact the most.
- **Create** detailed marketing reports using filters by contact channels,
  traffic sources, and location.
- **Analyze** which site pages users visit the most or on which pages they spend
  the most time.
- **Review** which OS and devices your customers use the most and optimize the
  site accordingly.

It is also possible to use the imported data with Creatio apps, for example,
segment contacts for bulk emails and marketing campaigns as well as build
detailed analytical reports.

note

Before you can use Matomo data in Creatio, make sure you have an active Matomo
account.

## Connect Matomo tracking service​

To use Matomo tracking service, retrieve connection data from Matomo, then
connect Matomo in Creatio and connect your landing page to Creatio.

Before you perform the setup, make sure you have an active Matomo account and an
existing landing page connected to Matomo.

### Step 1. Retrieve connection data from Matomo​

1. **Log in** to Matomo as a superuser of the relevant website.
2. Go to **Administration** → **Personal** → **Security** → **Auth tokens** and
   **retrieve the Auth token**. Make sure to set **Only allow secure requests**
   to "No."

### Step 2. Connect Matomo in Creatio​

1. **Go to** the **System settings** section → "Matomo connector settings"
   folder.
2. **Specify the Matomo analytics URL** in the **Default value** field of the
   "Address of Matomo API service" (the "MatomoAPIAddress" code) system setting.
   To retrieve the URL, go to Matomo dashboard and copy only the root URL in the
   address bar.
3. **Specify the Matomo Auth token** in the **Default value** field of the
   "Matomo API key" (the "MatomoAPIKey" code) system setting.

**As a result** , Marketing Creatio product will be able to identify contacts
who follow links in bulk emails.

To import Matomo data of users who submit web forms, proceed to the next step.

### Step 3. Connect your landing page to Creatio​

We recommend connecting landing pages to Creatio using **webhooks**.

If you use a landing page created using Landingi.com builder, take the steps in
the following Landingi article:
[Landingi, Creatio, and Matomo integration](https://landingi.com/help/landingi-creatio-and-matomo-integration).

If you use a different landing page service that can be integrated using
webhooks, take the steps from **Step 1. Connect the external webhook service**
section of the following article:
[Set up external webhook service integration](https://academy.creatio.com/documents?id=2412#title-2501-1).
After that, perform additional setup:

1. Add the following script to the landing page:

   <script>  
   function createOrReplaceInput(inputName,inputValue, formSelector, currentForm) {  
   var existingInput = jQuery(formSelector + " input[name='" + inputName +"']")[0];  
   if (existingInput) {  
   existingInput.value = inputValue;  
   } else {  
   var newInput = document.createElement('input');  
   newInput.setAttribute('type', 'hidden');  
   newInput.setAttribute('name',inputName);  
   newInput.setAttribute('value',inputValue);  
   currentForm.appendChild(newInput);  
   }  
   }  
   /* The function below generates individual VisitorId and sync it with Matomo. */  
   function defineVisitor() {  
   _paq.push([ function () {  
   var visitorId = this.getVisitorId();  
   var currentUrl = window.location.href;  
     
   //for each form add hidden fields with names: TrackingUserId  
   var formsCollection = document.getElementsByTagName('form');  
   for(var i = 0;i < formsCollection.length; i++) {  
   var formSelector = "";  
   if (formsCollection[i].id) {  
   formSelector = "#"+formsCollection[i].id;  
   } else if(formsCollection[i].name) {  
   formSelector = "form[name='" + formsCollection[i].name + "']";  
   }  
   createOrReplaceInput("TrackingUserId", visitorId, formSelector, formsCollection[i]);  
   createOrReplaceInput("PageUrl", currentUrl, formSelector, formsCollection[i]);  
   }  
   }])  
   }  
   jQuery(document).ready(defineVisitor);  
   </script>

2. Add extra **TrackingUserId** and **PageUrl** hidden fields to the relevant
   landing page.

3. Ensure the webhook is connected to the "Submitted form" ("FormSubmit" code)
   Creatio object.

If you use a
[web-to-object mechanism](https://academy.creatio.com/documents?id=1081#title-2504-2)
to integrate your landing page with Creatio, take the following steps:

1. Go to the **Landing pages and web forms** section in Creatio → **open** the
   relevant landing page record. The record must have "Contact registration
   form" type.
2. **Copy the code snippet** in the **STEP 2. Copy the code and configure and
   map the fields** block.
3. **Replace the old snippet** with the new snippet in the source code of the
   relevant landing page.

## Import Matomo data​

Creatio imports Matomo data of a specific contact recorded over the past year
once the contact is identified. This is done **in several ways** :

- The standard contact identification mechanism is executed after a user submits
  a form on a landing page that involves contact creation.
- The contact ID is used after a user follows a link in a bulk email sent using
  Creatio Marketing tools.

If the contact is identified **after they submit a form** , Creatio imports
Matomo data immediately. If the contact is identified **after they follow a link
in a bulk email** , Creatio imports Matomo data as part of the next update
scheduled by the "Matomo data synchronization for contacts by userId" business
process.

By default, Creatio updates most Matomo data of identified contacts **once a
day**. To modify the update time and frequency, edit the start timer of the
"Matomo data synchronization for contacts by userId" business process.

Important

Importing large volumes of data can affect website performance negatively. As
such, optimize synchronization time and frequency for your particular business
case.

Matomo data passed with form submissions is always updated in real time. View
the imported data on the **Marketing** tab of Creatio contact page.

Creatio uses a unified contact identification mechanism for form submissions on
landing pages that involve contact creation. Learn more:
[Identify contacts that submit web forms](https://academy.creatio.com/documents?id=2371).
The contact identification procedure has the following **restrictions** :

- If a user enters data of a different contact in the form, Creatio associates
  Matomo data with the contact whose data was specified.
- If a user submits multiple website forms as part of a single session and
  enters different contact data in each submission, Creatio associates Matomo
  data with the contact whose data was specified in the earliest submission.
- If a user forwards a bulk email and the new recipient follows the link,
  Creatio associates Matomo data of the user who followed the link with the
  original recipient.

## Imported data reference​

Creatio imports **web session** and **web action** data from Matomo. Web session
is a website visit during which contact takes particular steps. Web action is a
particular step the contact takes as part of a web session.

Learn more about **web session data** in the table below.

**Data type**| **Details**| **Session start date**| Date and time when the first
web action took place.| **Session duration**| Time between the session start
date and time of the last web action, in seconds.| **Country**| Imported into
"Country" (string), "Country Code," and "Country" (lookup) fields. Creatio
selects the lookup value based on the code from the **Countries** lookup.You can
add custom values to the **Countries** lookup manually. Creatio does not add new
lookup values if imported data contains values missing from the lookup.|
**Region**| Imported into "Region" (string), "Region Code," and "Region"
(lookup) fields. Creatio selects the lookup value based on the code from the
**States/provinces** lookup.Creatio does not add new lookup values if imported
data contains values missing from the lookup.| **City**| Imported into "City"
(string) and "City" (lookup) fields. Creatio selects the lookup value based on
the English name in the **Cities** lookup among the values filtered by the
specified **Countries** and **States/provinces** lookup values.You can add
custom values to the lookup. Creatio does not add new lookup values if imported
data contains values missing from the lookup.| **Location**| Geographic latitude
and longtitude imported as a string.| **Source**| Creatio selects the lookup
value from the **Lead sources** lookup.Imported data is matched to the lookup
values based on the following rules, from higher to lower priority:

1. If data includes the utm_source code and the lookup of the **Source code**
   object maps the tag to a **Lead sources** lookup record, Creatio populates
   the **Source** field with the mapped lookup record. To edit the lookup of the
   **Source code** object, add the lookup manually in the **Lookups** section.
2. If data includes the utm_campaign code and the lookup of the **Source code**
   object maps the tag to a **Lead sources** lookup record, Creatio populates
   the **Source** field with the mapped lookup record.
3. If the first two rules do not apply, Creatio uses
   [lead source identification rules](https://academy.creatio.com/documents?id=1597#title-2960-14)
   4 and 5.

| You can add custom values to the **Lead sources** lookup. Make sure to fill out the **Default channel** field of the lookup record if you add a custom value. Creatio does not add new lookup values if imported data contains values missing from the lookup. | **Channel** | Creatio selects the lookup value from the **Lead channels** lookup.If the imported data includes the utm_medium code and the lookup of the **Channel code** object maps the tag to a **Lead channels** lookup record, Creatio populates the **Channel** field with the mapped lookup record.If the "Channel" field is not populated based on channel data, Creatio can populate it based on the **Lead source** lookup.To edit the lookup of the **Channel code** object, add the lookup manually in the **Lookups** section.You can add custom values to the **Lead channels** lookup. Creatio does not add new lookup values if imported data contains values missing from the lookup. | **Referrer type and name** | Imported into "Referrer name" (string) and "Referrer type" (lookup) fields. Creatio selects the lookup value based on the "Matomo code" field. The "Referrer name" (lookup) field is not populated.Developers can add custom values to the lookup. Creatio adds new lookup values if the imported data contains values missing from the lookup. | **Referrer keyword** | Keywords the user entered into search engine before loading the page referrer URL. | **Page referrer URL** | URL of the page from which the user went to your landing page. | **utm_id** | Marketing codes | **utm_source** | **utm_medium** | **utm_campaign** | **utm_term** | **utm_content** | **Platform** | Operating system of the user | **Device** |     | **IP address** |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------------------- | ---------- | --------------- | -------------- | -------------- | ---------------- | ------------ | --------------- | ------------ | ---------------------------- | ---------- | --- | -------------- |

Learn more about **web action data** in the table below.

| **Data type** | **Details** | **ID of the relevant web session** |     | **Action start date** | Date and time when the action was triggered in Matomo. The value roughly corresponds to when the user performed the action. The difference between this value and the time of the actual action is usually negligible. | **Action type** | Creatio selects the lookup value from the **Web tracking action types** lookup. The imported data is mapped to lookup records via the **Matomo Code** field. The values of the **Name** field can be arbitrary but cannot be localized. The **Name** and **Matomo Code** fields of the lookup records added by Creatio are populated automatically.Developers can add custom values to the lookup. Creatio adds new lookup values if the imported data contains values missing from the lookup. | **Web page** | Creatio selects the lookup value from the lookup of the **Web page** object. The imported data is matched tothe **Name** and **Page URL** lookup columns.To edit the lookup of the **Web page** object, add the lookup manually in the **Lookups** section.Creatio adds new lookup values if the imported data contains values missing from the lookup. | **Page URL address** | URL of the page where the event took place. |
| ------------- | ----------- | ---------------------------------- | --- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------- |

---

## See also​

[Track contact data](https://academy.creatio.com/documents?id=2372)

- Connect Matomo tracking service
  - Step 1. Retrieve connection data from Matomo
  - Step 2. Connect Matomo in Creatio
  - Step 3. Connect your landing page to Creatio
- Import Matomo data
- Imported data reference
- See also
