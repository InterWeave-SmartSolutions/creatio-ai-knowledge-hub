# Google Analytics tracking solution | Creatio Academy

**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/marketing-tools/lead-generation/landing-pages/website-tracking/google-analytics
**Category:** development **Word Count:** 1607

## Content

Google Analytics tracking solution | Creatio Academy

Skip to main content

- [Creatio](https://www.creatio.com/)
- [Community](https://community.creatio.com/)
- [Marketplace](https://marketplace.creatio.com/)
- [Knowledge Hub](https://knowledge-hub.creatio.com/)

Version: 8.3Marketing

On this page

In Creatio, you can use Google Analytics 4 (GA4) to collect data about your
website visitors and analyze their behavior through web form submissions. The
integration provides detailed insights into the real online behavior of
prospects, effectively helping convert them into marketing qualified leads.

You can use Google Analytics data associated with specific Creatio contacts to
personalize product and service offers as well as improve the UX of your
website. For example, you can do the following:

- **Track** visitor journeys across your website pages and identify key
  conversion points
- **Evaluate** user engagement metrics like session duration, bounce rates, and
  page depth
- **Create** detailed marketing reports using filters by traffic sources, user
  demographics, and behavior patterns
- **Analyze** which products or services interest specific contacts the most
- **Review** which devices and platforms your visitors use to optimize site
  experience
- **Measure** the effectiveness of your marketing campaigns through UTM tracking

The imported data integrates seamlessly with Creatio apps, enabling you to
segment contacts for bulk emails and marketing campaigns as well as build
detailed analytical reports.

## Preliminary setup​

Before setting up Google Analytics integration with Creatio:

1. Ensure you have an active Google Analytics 4 property.
2. Acquire administrator access to your Google Analytics account.
3. Verify your website domain is properly configured in Google Analytics.
4. Make sure you have permission to modify your website's HTML.

## General procedure to integrate Google Analytics with Creatio​

1. Create a web page and connect it to Creatio. Read more >>>
2. Create a Google Analytics account and connect your web page to Google
   Analytics. Read more >>>
3. Connect your Google Analytics account to Creatio. Read more >>>
4. Connect the contact registration form. Read more >>>

### Step 1. Create a web page and connect it to Creatio​

Select an existing website or web page to track visitor behavior or create a new
page. This could be either of the following:

- A dedicated landing page promoting specific products or services (ideal for
  small to medium businesses).
- An entire website that has multiple pages (common for enterprise customers).

You can have both a custom-developed website, or have a website built with
no-code content management systems like WordPress or landing page builders like
Landingi.

### Step 2. Create a Google Analytics account and connect your web page to Google Analytics​

1. Follow the steps in the official Google documentation to **create an
   account** and **add data streams** to your Google Analytics property:
   [[GA4] Set up Analytics for a website and/or app](https://support.google.com/analytics/answer/9304153?hl=en).
   You only need to add data streams to your Google Analytics property.

2. **Add the tracking code** to your website. The implementation method depends
   on your website platform.

Landingi.com

For a landing page created using the **Landingi.com** builder, open your landing
page dashboard to add a new script. If you already have a Google Analytics
script, which begins with `<!-- Google tag (gtag.js) -->` and ends with
`</script>`, replace it with the script for a Landingi page provided below. Make
sure to select the Head position and add the script to all pages you want to
track.

         <script>
             window.TAG_ID='{Measurement ID}';
         </script>

         <script async src="https://www.googletagmanager.com/gtag/js?id={Measurement ID}"></script>

         <script src="https://webtracking-v01.creatio.com/JS/create-object.js"></script>

         <script src="https://webtracking-v01.creatio.com/JS/crt-gtag-with-tracking-form-data.js"></script>


Replace the `{Measurement ID}` in the script with your actual Measurement ID. To
find your Measurement ID, follow the official Google documentation:
[[GA4] Measurement ID](https://support.google.com/analytics/answer/12270356?hl=en).

Custom-developed pages or pages created with a Content Management System

For all other landing pages, such as **custom-developed** pages or pages created
using a **Content Management System (CMS)** , add the script for other pages
immediately after the opening <head> tag in your base template or immediately
after the opening <head> tag on each page that you want to track.

         <script>
            window.TAG_ID='{Measurement ID}';
         </script>

         <script async src="https://www.googletagmanager.com/gtag/js?id={Measurement ID}"></script>

         <script src="https://webtracking-v01.creatio.com/JS/create-object.js"></script>

         <script src="https://webtracking-v01.creatio.com/JS/crt-gtag.js"></script>


If you use a CMS, check your platform's documentation for GA4 integration first.
You will still need to embed the script below on any custom-developed landing
pages.

Replace the `{Measurement ID}` in the script with your actual Measurement ID. To
find your Measurement ID, follow the official Google documentation:
[[GA4] Measurement ID](https://support.google.com/analytics/answer/12270356?hl=en).

If you already have a Google Analytics JavaScript section of code within your
page that begins in `<!-- Google tag (gtag.js) -->` and ends in `</script>`,
replace it with the code provided above.

3. **Add custom dimensions** in Google Analytics. Custom dimensions in GA4 are
   additional attributes you can create to track specific data points. In this
   case, you need the following custom parameters to link website visitors to
   Creatio contacts:
   - **Session ID** : Tracks individual website visits.
   - **User ID** : Identifies specific visitors.

To do this:

     1. Go to **Admin** → **Custom definitions** → **Create custom dimensions**.

     2. Create custom dimensions that have the following parameters:

| Dimension name | Scope | Event parameter | crt_session_id | event | crt_session_id | crt_user_id | event | crt_user_id |
| -------------- | ----- | --------------- | -------------- | ----- | -------------- | ----------- | ----- | ----------- |

Custom dimension values in the following format:
`{crt_user_id}:{crt_session_id}`.

Learn more on how to add an event-scoped custom dimension in the official Google
documentation:
[[GA4] Create event-scoped custom dimensions](https://support.google.com/analytics/answer/14239696?sjid=5785372480522799313-EU&hl=en).

**As a result** , your web page will be connected to Google Analytics.

### Step 3. Connect your Google Analytics account to Creatio​

1. **Go** to the **Web analytics** section.

2. **Click** **Settings** → **Connect**.

3. **Sign in** using your Google account and grant Creatio access to Google
   Analytics data. Select all required permissions when prompted (Fig. 1).

Fig. 1 Connecting Google Analytics account

![Fig. 1 Connecting Google Analytics account](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/NoCode_Customization/web_analytics/scr_google_analytics_connecting_google_analytics.gif)

**As a result** , your Google Analytics account will be connected to Creatio.
You will be able to view your connected Google Analytics accounts and their
connection status in the **Settings** panel of the **Web analytics** section.

### Step 4. Connect the contact registration form​

Learn more about connecting a form on a Landingi page that creates ontacts or
submitted forms:
[Import data from Landingi web page](https://academy.creatio.com/documents?id=2414).
Learn more about connecting a form on a page created using a different service:
[Retrieve a webhook in Creatio](https://academy.creatio.com/documents?id=2516).

**As a result** , you will start receiving web analytics data for the last 90
days of contacts in Creatio after they submit a form on a landing page. The web
analytics data is updated once a day. Google Analytics data for contact actions
is usually received for the previous day or the day before as Google Analytics
takes up to 48 hours to properly gather and structure all the web analytics
data. Learn more in the official Google documentation:
[[GA4] Data freshness](https://support.google.com/analytics/answer/11198161?hl=en).

## Imported data reference​

Creatio imports web session and web action data from Google Analytics. A **web
session** is a website visit during which a contact takes particular steps. A
**web action** is a particular step the contact takes as part of a web session.

Learn more about **web session data** in the table below.

| Data type | Details | Session | The custom dimension values in the following format: `{crt_user_id}:{crt_session_id}`. | Session start date | The combined values of the date, hour, and minute when the first web action took place. | Referrer URL | The full referring URL that includes the hostname and path. This referring URL is the previous URL of the user and can be this website domain or other domains. | utm_source | The referrer. Populated by the `utm_source` URL parameter. | utm_medium | The marketing medium the referral uses. For example, `cpc`. Populated by the `utm_medium` URL parameter. | utm_campaign | The name of the manual campaign. Populated by the `utm_campaign` URL parameter. Learn more in the official Google documentation: [[GA4] URL builders: Collect campaign data with custom URLs](https://support.google.com/analytics/answer/10917952?hl=en). | Language | The language setting of the user's browser or device. Follows the ISO 639 standard. For example, `en-us`. | Country code | The ID of the country from which the user activity originated, derived from their IP address. Follows the ISO 3166-1 alpha-2 standard. | City | The ID of the city from which the user activity originated, derived from their IP address. | Source | Creatio selects the lookup value from the **Lead sources** lookup based on UTM parameters and source identification rules. | Channel | Creatio selects the lookup value from the **Lead channel** lookup. |
| --------- | ------- | ------- | -------------------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------ |

Learn more about **web action data** in the table below.

| Data type | Details | Action start date | The combined values of date, hour, and minute when the action was triggered in Google Analytics. | Type | The name of the GA4 event. Common events include `page_view`, `click`, `form_submit` for general interactions, and `view_item`, `add_to_cart`, `purchase` for ecommerce tracking. Learn more in the official Google documentation: [[GA4] Automatically collected events](https://support.google.com/analytics/answer/9234069?hl=en&ref_topic=13367566&sjid=5677599456360580448-EU).Creatio adds new lookup values if the imported data contains values missing from the lookup. | Web page | Creatio selects the lookup value from the lookup of the **Web page** object. The imported data is matched to the **Page URL** column.Creatio adds new lookup values if the imported data contains values missing from the lookup. | Page URL | The hostname, page path, and query string for web pages visited. For example, the `fullPageUrl` portion of "https:​//www​.example.com/store/contact-us?query_string=true" is "www​.example.com/store/contact-us?query_string=true". |
| --------- | ------- | ----------------- | ------------------------------------------------------------------------------------------------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

---

## See also​

[Track contact data](https://academy.creatio.com/documents?id=2372)

[Matomo tracking solution](https://academy.creatio.com/documents?id=2520)

[Official Google Analytics documentation](https://support.google.com/analytics/topic/14088998?hl=en&ref_topic=14090456&sjid=14394906845141504947-EU)

- Preliminary setup
- General procedure to integrate Google Analytics with Creatio
  - Step 1. Create a web page and connect it to Creatio
  - Step 2. Create a Google Analytics account and connect your web page to
    Google Analytics
  - Step 3. Connect your Google Analytics account to Creatio
  - Step 4. Connect the contact registration form
- Imported data reference
- See also
