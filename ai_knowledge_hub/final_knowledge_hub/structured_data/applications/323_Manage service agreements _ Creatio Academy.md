# Manage service agreements | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 1214
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.0/service-tools/itsm-tools/manage-service-agreements

## Description

Creatio implements the "Service level management" ITSM process in the Service
agreements section. Use this section to determine the customer service
requirements, manage your agreements, and in-house service agreements. For each
agreement, you can define the individual terms of service and view the
statistics.

## Key Concepts

section, detail, lookup, operation, system setting, package, contact, account,
case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/creatio-apps/overview/platform-overview)** (8.3).

Version: 8.0Service Enterprise

On this page

Creatio implements the "Service level management" ITSM process in the **Service
agreements** section. Use this section to determine the customer service
requirements, manage your agreements, and in-house service agreements. For each
agreement, you can define the individual terms of service and view the
statistics.

## Add service agreements​

To add a new service agreement:

1. Open the **Service agreements** section and click **New** in the section
   list.

2. Populate the service agreement page:

| Title | Name of the service agreement. By default, it consists of the service agreement number and the name of the account: "24 – Axiom". | Number | Service agreement number. Creatio automatically generates numbers according to the pattern specified in the "Service agreement current number" (ServicePactLastNumber) system setting. This is a non-editable field. | Type | Type of service agreement: _ SLA – service level agreement. This type is used to define the service parameters for the end-users. _ OLA – operational level agreement. This type is used to indicate the internal service agreements of your company. For example, the agreements between departments or employee groups. \* UC – underpinning contract. These are the agreements between your company and its suppliers. If you select the "UC" type on the **Contract provisions** tab, additional fields will be available to enter information about the service provider. | Status | Current status of the service agreement, for example, "Draft" or "Active". | Start/End | The start and end dates of the service agreement validity. | Owner | Name of the user responsible for managing and updating information about the service agreement. | Calendar | The calendar that determines workdays and business hours of the support team. Creatio uses calendars to [calculate the response and resolution time](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1552) for service-related cases. By default, the field is populated with the value specified in the "Base calendar" (BaseCalendar) system setting. Use the **Calendars** lookup to set up custom calendars. | Support level | The support package that is provided according to the service agreement. Creatio calculates the response and resolution deadline values based on the support level. |
| ----- | --------------------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------- | --------- | ---------------------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

3. On the **Contract provisions** tab, populate information about the
   [service objects](https://academy.creatio.com#HT_manage_service_agreements_service_objects)
   and
   [services](https://academy.creatio.com#HT_manage_service_agreements_services).

4. On the **Attachments and notes** tab, enter additional information about the
   service agreement and related links to web resources. For example, attach a
   photocopy of the signed agreement. Read more >>>

5. Click **Save** to save the service agreement.

As a result, the new service agreement record with the specified parameters will
appear in the list of the **Service agreements** section.

## Default service agreement​

In addition to the agreements with the specific service consumers, the **Service
agreements** section must include an agreement that includes the minimum set of
services, provided to any consumer i.g., a "default service agreement."

This agreement can be used to obtain customer support service when no
appropriate service agreement is found for a particular case.

The default service agreement should be specified in the "Default service
agreement" (DefaultServicePact) system setting.

## Add service objects to SLA​

Information about the service objects is represented on the **Service
recipients** detail of the service agreement page.

To specify service objects for a service agreement:

1. Open the **Service agreements** section, select the needed record and click
   **Open**.

2. Add accounts and contacts to the **Service recipients** detail:
   1. Click
      ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_service_agreements/btn_com_add_tab.png)
      → **Account** or **Contact**.

   2. In the window that opens, select the needed account or contact and click
      **Select**.

3. Add departments of the service recipient accounts, if only specific
   departments can use this service level:
   1. Select an account under **Service recipients** , then click
      ![btn_com_roles_actions_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_service_agreements/btn_com_roles_actions_menu.png)
      → **Select department**.

   2. In the window that opens, select the departments that will receive
      services under the service agreement → click **Select**.

4. Click **Save** on the service agreement page.

As a result:

- Creatio will use the information on the **Service recipients** detail when
  [selecting a service agreement](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1553)
  on the
  [case page](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1550).

- If you added departments, a record for each selected department will appear on
  the **Service recipients** detail. The service agreement will be valid for the
  selected departments only.

## Add services to SLA​

Set up a list of services provided under a service agreement on the **Services**
detail of the service agreement page.

To add a service to a service agreement:

1. Open the **Service agreements** section, select the needed record and click
   **Open**.

2. Go to **Contract provisions** → **Services** → click
   ![btn_com_add_tab00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_service_agreements/btn_com_add_tab00001.png).
   A lookup window opens, displaying a list of all services from the
   [**Services** section](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1061).

3. Select the services provided under this service agreement and click
   **Select**.

As a result, the service(s) will be added to the **Services** detail list with
the default terms of service provision.

## Modify service provision terms in SLA​

Services are added to the service agreements with their default terms of
provision: calendars, response, and resolution deadlines. You can modify the
terms within the framework of a specific SLA:

1. Open the **Service agreements** section, select the needed record and click
   **Open**.

2. Select a service on the **Services** detail, click
   ![btn_com_roles_actions_menu00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_service_agreements/btn_com_roles_actions_menu00002.png)
   → **Edit**. A **Service in service contract** page opens.

3. Specify the service provisions within the selected service agreement:

| Service | Name of service provided under the selected agreement. It is defined after adding the service to the agreement. This is a non-editable field. | Response time | Estimated response and resolution time used for processing service-related cases under the corresponding service agreement. By default, the fields are populated with the response and resolution time values specified on the service page of the [**Services** section](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1061). However, you can set other values for the selected service. Creatio will use the entered data to calculate the response and resolution time values for cases under the selected service agreement. | Resolution time | Status | Status of the service provided under the selected service agreement. | Calendar | The calendar that is used for providing services under the selected service agreement. If this field is empty, Creatio will calculate the case-related response and resolution time values using the calendar specified in the **Calendar** field of the service agreement page. |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ------ | -------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

4. Click **Save**.

As a result, Creatio will use the information of the **Services** detail when
selecting customer service provisions and
[calculating the response and resolution time](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1552)
for cases.

## Set service providers for UC​

If you add an "Underpinning contract" in the **Service agreements** section by
selecting "UC" on the **Type** field, additional fields for entering information
on the subcontractor service provider become available in a separate **Service
provider** group on the **Contract provisions** tab of the service agreement
page:

- Populate the **Service provider** → **Account** field by specifying the
  company that provides services under the corresponding service agreement. If
  you populate the **Contact** field, the **Account** field will be
  automatically populated with the account specified on the page of the selected
  agreement.

- Populate the **Service provider** → **Contact** field by specifying the
  contact person of the supplier that you work with under the agreement. If you
  populate the **Account** field, the contact lookup will contain contacts of
  the selected company only.

---

## See also​

[Calculate response and resolution time](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1552)

[Select service agreement](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1553)

[Manage service catalog](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1061)

- Add service agreements
- Default service agreement
- Add service objects to SLA
- Add services to SLA
- Modify service provision terms in SLA
- Set service providers for UC
- See also
