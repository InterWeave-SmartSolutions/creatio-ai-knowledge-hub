# FAQ | Creatio Academy

**Category:** administration **Difficulty:** beginner **Word Count:** 596
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.0/marketing-tools/digital-ads/faq-on-digital-ads-app

## Description

How can I check the campaign as part of which a contact was added?

## Key Concepts

section, campaign, contact, account

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/overview/platform-overview)** (8.3).

Version: 8.0Marketing

On this page

## How can I check the campaign as part of which a contact was added?​

Creatio links the new contact to a campaign if the user sends their first form
submission as part of the campaign. To check the campaign as part of which the
contact was added, view the **Ad campaign** field of the contact. Creatio
populates the field based on form submissions if they contain **utm-campaign**
and **utm_source** parameters.

## How can I check the campaign as part of which the contact was acquired?​

Creatio considers the contact acquired as part of a specific campaign if the
contact sent their first submission as part of the campaign. The campaign is
specified in the **Ad campaign** contact field. The field is populated based on
contact form submissions if the submissions contain **utm-campaign** and
**utm_source** parameters.

## How can I view contacts that participated in an ad campaign?​

Set up a filter by form submissions in the **Contacts** section and specify the
relevant ad campaigns in the **Ad campaign** parameter (Fig. 1).

Fig. 1 Filter contacts by form submissions

![Fig. 1 Filter contacts by form submissions](https://academy.creatio.com/docs/sites/en/files/images/Marketing_Tools/digital_ads/faq/scr_contact_filter.png)

## Why will Creatio not calculate the "Number of submissions" and "Number of contacts" metrics?​

This can happen due to multiple reasons. Troubleshoot the following:

- Creatio must pass form submission to the Submitted forms object.

- The form submissions have **utm-campaign** and **utm_source** parameters
  populated, and the parameter values are valid.

If the issue persists, contact Creatio support.

## Why do conversion metrics in Creatio differ from the ad service?​

Creatio calculates the number of conversions gained from an ad campaign based on
UTM parameters. This calculation principle might differ from the mechanism that
tracks conversions in the ad service. As such, discrepancies can occur. The most
common reasons for them are as follows:

- Contact clicked on an ad Creatio did not track. For example:
  - The ad account is not connected to Creatio.
  - The contact clicked the ad before Creatio started tracking it.
  - The ad has a tracking error.

- Columns of UTM marks in the linked contact records of the "Submitted forms"
  object were updated manually. If this occurs, Creatio cannot match contact
  data to the contact and does not display the contact in the Digital Ads app.

- Creatio has not yet calculated the number of contacts. This is done in
  intervals rather than real time.

## Why will my Facebook Ads account not connect?​

Make sure you meet the connection requirements and are using the correct
Facebook user. Learn more:
[Connect Facebook Ads to Creatio](https://academy.creatio.com/documents?id=2462).
If the issue persists, update Creatio Ads app permissions and reset Creatio app
permissions in Facebook.

## Why will my Google Ads account not connect?​

Make sure you meet the connection requirements and are using the correct Google
user. Learn more:
[Connect Google Ads to Creatio](https://academy.creatio.com/documents?id=2463).
If the issue persists, reset Creatio app permissions in Google Ads.

---

## See also​

[Overview of Digital Ads app](https://academy.creatio.com/documents?id=2461)

[Integrate Facebook Ads with Creatio](https://academy.creatio.com/documents?id=2462)

[Integrate Google Ads with Creatio](https://academy.creatio.com/documents?id=2463)

- How can I check the campaign as part of which a contact was added?
- How can I check the campaign as part of which the contact was acquired?
- How can I view contacts that participated in an ad campaign?
- Why will Creatio not calculate the "Number of submissions" and "Number of
  contacts" metrics?
- Why do conversion metrics in Creatio differ from the ad service?
- Why will my Facebook Ads account not connect?
- Why will my Google Ads account not connect?
- See also
