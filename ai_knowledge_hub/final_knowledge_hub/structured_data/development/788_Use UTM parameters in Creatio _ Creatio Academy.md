# Use UTM parameters in Creatio | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 1365 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/marketing-tools/lead-generation/landing-pages/website-tracking/use-utm-parameters

## Description

UTM parameters are essential tools for tracking the effectiveness of marketing
campaigns, understanding lead sources, and enhancing lead generation efforts.
Creatio provides robust tools for leveraging UTM parameters in various marketing
activities, including email marketing, website tracking, social media
integration, and more. This article explores how to best use UTM parameters
within the Creatio platform and integrate them with other tracking and lead
generation features.

## Key Concepts

business process, workflow, detail, integration, campaign, lead, contact,
account, automation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Marketing

On this page

UTM parameters are essential tools for tracking the effectiveness of marketing
campaigns, understanding lead sources, and enhancing lead generation efforts.
Creatio provides robust tools for leveraging UTM parameters in various marketing
activities, including email marketing, website tracking, social media
integration, and more. This article explores how to best use UTM parameters
within the Creatio platform and integrate them with other tracking and lead
generation features.

UTM parameters are parameters added to URLs that help you track the performance
of your campaigns across different platforms. These parameters typically include
parameters like `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, and
`utm_content` that give detailed insights into how visitors arrive at a website
and what actions they take.

For example, you are running an email campaign to promote a new product launch.
You have a newsletter that includes a call-to-action (CTA) button that directs
recipients to the product landing page. You want to track how effective this
email is at driving traffic and conversions. You can build the following link
using URL building tools, such as Campaign URL Builder by Google Analytics:
`https://yourwebsite.com/new-product?utm_source=newsletter&utm_medium=email&utm_campaign=product_launch&utm_term=summer&utm_content=cta_button`.
View the parameter breakdown in the table below.

| **Parameter** | **Explanation** | `utm_source=newsletter` | Identifies the source of the traffic. For this example, since the traffic is coming from your email newsletter, you set `utm_source=newsletter`. | `utm_medium=email` | Specifies the medium through which the link was shared. For this example, because this is an email campaign, you use `utm_medium=email`. | `utm_campaign=product_launch` | Names the specific campaign with which the link is associated. For this example, since the purpose of this email is to promote a new product, the campaign name is `utm_campaign=product_launch`. | `utm_term=summer` | Identifies the keyword or search term associated with the campaign. For this example, if the product is part of a summer promotion or you are targeting the keyword "summer" in your email content, you use `utm_term=summer`. This can help to track seasonal interest or keyword performance related to "summer." | `utm_content=cta_button` | Differentiates between similar content or links within the same email or campaign. For this example, if your email contains multiple links, such as a text link and a CTA button, you use `utm_content=cta_button` to track clicks specifically on the button. This helps you determine which element in your email drives the most engagement. |
| ------------- | --------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

UTM parameters are especially crucial when it comes to paid ads. By
incorporating UTM parameters into the URLs used in your paid campaigns, you can
effectively track the performance and quality of your ads, keywords, and lead
forms. This data lets you see which ads are driving the most traffic and
conversions. This, in turn, lets you optimize your ad spending and improve ROI.

Additionally, UTM parameters are invaluable for A/B testing landing pages. By
assigning different UTM parameters to each variation of a page, you can clearly
identify which version performs better. This provides critical insights into
user behavior and preferences.

In Creatio, UTM parameters are particularly valuable for tracking the origin of
leads or contacts, measuring the success of email campaigns, integrating data
from social media platforms like Facebook and LinkedIn, etc.

## Take advantage of UTM tracking in Creatio​

### Track prospect sources and channels using UTM parameters​

Creatio lets you track lead sources and channels using UTM parameters
seamlessly. When a prospect clicks on a link that contains UTM parameters and
completes a form on an integrated landing page, Creatio captures the UTM data
and attributes it to the corresponding lead or submitted form. This helps to
understand which campaigns or platforms are driving the most valuable traffic.

The **Populating Contact with Submitted Form's Data** business process available
in the **Lead Generation** app automates the collection of this data. When a
form is submitted, this process populates the Contact record in Creatio using
the submitted information. This includes the **Source** and **Channel** fields
based on the UTM parameters. This automation ensures that you have accurate and
up-to-date information on the origins of their leads.

Learn more about the rules that identify the source and channel for prospects in
a separate article:
[Lead source tracking](https://academy.creatio.com/documents?id=1597#title-2960-9).

### Utilize UTM parameters in email marketing​

In email marketing, UTM parameters are essential for understanding which emails
drive the most traffic and conversions. Creatio lets you include UTM parameters
in all the links within your emails automatically. This can be done for emails
sent manually or through campaign automation workflows. Learn more about the
setup process in separate articles:
[Create a bulk email](https://academy.creatio.com/documents?id=1008#title-1551-3),
[Create a trigger email](https://academy.creatio.com/documents?id=1506#title-2046-3).

This functionality ensures that when a recipient clicks on a link in your email,
the action is tracked back to the following:

- The web analytics of the page the recipient visited. For example, you might
  see information about the traffic source being email in your Google Analytics
  account.

- The lead, submitted form, or contact data where the information about the
  source, channel, and other parameters is stored after the email is sent and
  new prospects or leads are generated.

### Integrate Facebook and LinkedIn with UTM parameters​

Social media platforms like Facebook and LinkedIn are key channels for
generating leads. Creatio supports seamless integration with these platforms,
allowing you to set up UTM tracking and capture lead source data efficiently.

**Facebook Integration** : when setting up Facebook lead generation, you can
include UTM parameters or direct source or channel values by assigning default
values for form submissions. This will help you to track the source and channel
of the prospects generated from Facebook.

**LinkedIn Integration** : LinkedIn integration can be configured with UTM
parameters or direct source or channel values for tracking. This can be done
either through default mapping effective for all integrated LinkedIn forms or
through the custom mapping that can be different for each of the integrated
LinkedIn form.

Learn more in a separate article:
[Create a trigger email](https://academy.creatio.com/documents?id=1506#title-2046-3)

### UTM parameters in web analytics​

When Matomo or Google Analytics integration is enabled, information about UTM
parameters can be captured upon form submission from a landing page
automatically. If a contact follows a link that contains specific UTM parameters
and submits a form on the landing page, the information about these parameters
will be included in the submitted form. Based on this information, the
**Source** and **Channel** fields in both the submitted form and the
corresponding contact record can be populated accordingly. Learn more:
[Matomo tracking solution](https://academy.creatio.com/documents?id=2520).

### Best practices for using UTM parameters​

- **Consistency in naming conventions**. Use consistent naming conventions for
  UTM parameters to ensure accurate tracking and reporting. For example, always
  use `utm_source=google` instead of variations like `utm_source=Google` or
  `utm_source=GOOGLE`.
- **Regular monitoring and analysis**. Regularly monitor UTM data in Creatio to
  adjust your campaigns as needed. Analyze which sources, channels, or campaigns
  are driving the highly convertible prospects and focus your efforts on those
  areas.
- **Integration with the sales data**. Combine UTM data with sales data in
  Creatio to get a holistic view of the revenue attribution. For example, you
  can analyze the number of successfully closed opportunities for the prospects
  from the particular source. This will help you understand which source of
  prospects is the most effective for your business.
- **Leveraged automation** : Use Creatio automation features, like including UTM
  parameters to all links in the email or **Populating Contact with Submitted
  Form's Data** business process to streamline the capture and utilization of
  UTM data. Automation reduces manual effort and enhances accuracy.

UTM parameters in Creatio provide a powerful way to track the effectiveness of
your marketing campaigns, understand prospect sources and channels, optimize
your lead generation efforts, and improve your marketing ROI. By following the
setup and best practices, you can ensure that you are making the most of the UTM
tracking capabilities within Creatio.

---

## See also​

[Create a trigger email](https://academy.creatio.com/documents?id=1506)

[Lead source tracking](https://academy.creatio.com/documents?id=1597)

[Set up lead source tracking](https://academy.creatio.com/documents?id=1607)

[Set up automatic lead registration from social networks](https://academy.creatio.com/documents?id=2499)

[Set up automatic lead registration from LinkedIn](https://academy.creatio.com/documents?id=2368)

[Matomo tracking solution](https://academy.creatio.com/documents?id=2520)

[Add a campaign](https://academy.creatio.com/documents?id=1074)

- Take advantage of UTM tracking in Creatio
  - Track prospect sources and channels using UTM parameters
  - Utilize UTM parameters in email marketing
  - Integrate Facebook and LinkedIn with UTM parameters
  - UTM parameters in web analytics
  - Best practices for using UTM parameters
- See also
