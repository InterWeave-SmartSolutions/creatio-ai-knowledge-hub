# Pricing model and its caps | Creatio Academy

**Category:** administration **Difficulty:** beginner **Word Count:** 1371
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/administration/pricing-model-limits

## Description

Creatio pricing model lets you select one of multiple subscription plans Creatio
pricing.

## Key Concepts

business process, section, detail, lookup, web service, odata, rest api,
database, role, operation

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Creatio pricing model lets you select one of multiple subscription plans:
Growth, Enterprise, or Unlimited. These plans provide different levels of
functionality and resources. You can view the full list of levels in the current
price list here: [Creatio pricing](https://www.creatio.com/products/pricing).

The subscription plans offer tiered access to features and resources, designed
to accommodate varying business needs. Specifically, the plans provide the
following:

- **Features**. For example, the ability to use single sign-on. Only Enterprise
  and Unlimited customers can use it.
- **Resources**. These are mostly connected to server capabilities. For example,
  drive space usage and the number of executed business process elements.

The cap on resources is soft. This means when you reach it, Creatio does not
block anything immediately. Instead, we talk to you about changing the
subscription plan or purchasing an addon, such as additional drive space.

You can monitor server resource consumption in the **Subscriptions** section of
the Application Hub. The feature is available for beta testing. To gain access
to the section, contact Creatio support. If you have any feedback, contact us
at: [beta@creatio.com](mailto:beta@creatio.com). All feedback is appreciated.

Fig. 1 Viewing resource consumption details

![Fig. 1 Viewing resource consumption details](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/images/Setup_and_Administration/pricing_model_limits/gif_subscription_details.gif)

All services you can use as part of your Creatio experience can be divided into
the following groups:

- **Account level services**. These are not limited on the level of a specific
  environment and are applied to your entire organization. For example, data
  stored for every separate environment can have varied size, but total size of
  data stored for all environments has a cap.
- **Environment level services**. These are applied to every specific
  environment. For example, if you have Growth subscription plan and
  **alphabusiness** and **pre-alphabusiness** websites, you can execute up to
  50000 process elements per month for each environment.

## Resource management​

#### Total Database storage size​

Account level service. Covers records that are displayed in all out-of-the-box
and custom Creatio sections, lookup records, logs of executed business
processes, etc. Comprises total size of your environment databases. This
includes both data and indexes. Excludes the technical space that the database
reserves and some specific Creatio technical tables. Measured in megabytes.

The cap depends on the following parameters:

- subscription plan
- number of active full user licenses
- purchased add-ons

For example, you have 30 Studio Growth licenses and no add-ons. In this case,
the available data storage size is 1 Gb \* 30 licenses = 30 Gb total.

Alternatively, you have 50 Studio Enterprise license and an add-on for 40 Gbs.
In this case, the available data storage size is 2 Gb \* 50 licenses + 40 from
add-ons = 140 Gbs total.

The cap is not bound to data of any specific user but rather to the total size
of your data storage. One user can create data that takes up 3 Gb and another
one data that takes up 15 Mb.

#### Total attachment storage size​

Account level service. Covers files that are attached to records in both
out-of-the-box and custom Creatio sections. Comprises total size of all files
that are stored in external file storage, such as AWS S3, Azure Blob, in Creatio
Cloud for all your environments. Measured in megabytes

If you store your files in database instead of external file storage, the
attachment file storage usage is 0, and data storage consumption is higher
because files are taken into account during data storage size calculation.

The cap depends on the following parameters:

- subscription plan
- number of active full user licenses
- purchased add-ons

For example, you have 30 Studio Growth licenses and no add-ons. In this case,
the available attachment storage size is 1 Gb \* 30 licenses = 30 Gb total.

Alternatively, you have 50 Studio Enterprise licenses and an add-on for 40
Gbs.In this case, the available data storage size is 2 Gb \* 50 licenses + 40
from add-ons = 140 Gbs total.

The cap is not bound to data of any specific user but rather to the total size
of your data storage. One user can create data that takes up 3 Gb and another
one data that takes up 15 Mb.

#### Number of environments​

Account level service. Comprises the number of your environments in Creatio
Cloud. Takes into account only environments that have production,
pre-production, and development types.

The cap depends on the pricing plan.

#### Monthly business process executed​

Environment level service. Comprises the number of custom business process
elements that were executed. Custom means business processes that were created
by you from scratch or a new version of an out-of-the-box process that you
created. Out-of-the-box business processes that were not replaced using a custom
new version are not taken into account. Includes processes launched by all
internal and external users.

Usage refresh term is 1 month. The number is reset to 0 every first day of the
month.

The cap is applied only to customers that have Growth plan and has fixed value
of 50000 executed elements.

The service has no add-ons. If you want to use more elements, upgrade your
subscription plan.

#### Daily OData REST API calls​

Environment level service. Comprises the number of API requests made to both
OData 4 and 3, i.e., "/OData" or "/EntityDataService." For batch queries, every
operation inside the batch body is calculated as a separate request.

Usage refresh term is 1 day. The number is reset to zero every day at 0:00 AM
UTC.

The cap is applied only to customers that have Growth plan and depends on the
number of full user licenses. One full user license provides you with 10000 API
calls.

For example, you have 50 Studio Growth licenses. In this case, the number of
available daily OData API calls is 50 \* 10 000 = 500000 total.

The service has no add-ons. If you want to use more calls, upgrade your
subscription plan.

The cap is not applied to specific users. Any user can make any number of API
calls.

#### Daily webhook service calls​

Environment level service. Comprises the number of API requests made to the
Creatio webhook service.

Usage refresh term is 1 day. The number is reset to zero every day at 0:00 AM
UTC.

The cap is applied only to customers that have Growth plan and depends on the
number of full user licenses. One full user license provides you with 10000
calls.

For example, you have 50 Studio Growth licenses. In this case, the number of
available daily webhook service calls is 50 \* 10 000 = 500000 total.

The service has no add-ons. If you want to use more calls, upgrade your
subscription plan.

The cap is not applied to specific users. Any user can make any number of calls.

#### Daily custom web service calls​

Environment level service. Comprises the number of API requests made to custom
web services developed by you using C# code. Both authorized and anonymous web
services are taken into account.

Usage refresh term is 1 day. The number is reset to zero every day at 0:00 AM
UTC.

The cap is applied only to customers that have Growth plan and depends on the
number of full user licenses. One full user license provides you with 10000
calls.

For example, you have 50 Studio Growth licenses. In this case, the number of
available daily custom web service calls is 50 \* 10 000 = 500000 total.

The service has no add-ons. If you want to use more calls, upgrade your
subscription plan.

The cap is not applied to specific users. Any user can make any number of calls.

#### Number of functional and organizational roles​

Environment level service. Comprises functional and organizational roles that
are included in both **All employees** and **All external users** branches. The
following roles are excluded from the calculation:

**Functional roles** :

- Studio
- Administrator
- Developer
- All employees
- All external users
- Administrator for the organization on the portal

**Organizational roles** :

- System administrator
- All employees
- All external users

The cap is applied only to customers that have Growth plan and has a fixed value
of 50 organizational and functional roles.

The service has no add-ons. If you want to use more roles, upgrade your
subscription plan.

---

## See also​

[Creatio licensing](https://academy.creatio.com/documents?id=1264)

[Manage user licenses](https://academy.creatio.com/documents?id=1472)

- Resource management
- See also
