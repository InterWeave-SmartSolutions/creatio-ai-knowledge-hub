# Manage configuration items (CI) | Creatio Academy

**Category:** administration **Difficulty:** intermediate **Word Count:** 1209
**URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/8.0/service-tools/itsm-tools/manage-configuration-items

## Description

Creatio implements the "Configuration management"/"Asset management" ITSM
process in the Configuration items section. Use this section to manage
information about your configuration items (CI) to keep them operational and
maintain the high quality of the service delivery.

## Key Concepts

configuration, section, detail, lookup, dashboard, operation, contact, account,
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

Creatio implements the "Configuration management"/"Asset management" ITSM
process in the **Configuration items** section. Use this section to manage
information about your configuration items (CI) to keep them operational and
maintain the high quality of the service delivery.

note

A "configuration item" in Creatio represents some form of software or hardware
that affects the provided IT services.

## Add configuration items​

1. Open the **Configuration items** section and click **New** in the section
   list.

2. Populate the configuration item page:

| Name | Name of the configuration item. | Category | Configuration item category, for example, "Peripherals" or "Software." | Type | Configuration item type, for example, "Printer" or "Operating system." A list of possible values for this field depends on the selected configuration item. Configuration item type dependency on the category is defined in the **CI types** lookup. | Model | Model of the configuration item. A list of possible values for this field depends on the type of the selected configuration item. Configuration item model dependency on the category is defined in the **CI models** lookup. | Status | The current status of the configuration item, for example, "Active" or "Under maintenance." | Inventory number | Configuration item inventory number defined by the company to manage infrastructure items. | Serial number | The serial number of the configuration item as specified by the manufacturer. |
| ---- | ------------------------------- | -------- | ---------------------------------------------------------------------- | ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------ | ------------- | ----------------------------------------------------------------------------- |

3. On the **General information** tab, populate additional information related
   to the configuration item, such as the information about the CI users and
   components:

| Owner | Creatio user responsible for updating the information on the configuration item. | Parent CI | The configuration item that has the current CI as one of its components. When you save the record, the current configuration item displays on the **Components** detail of the configuration item selected in the field. | Purchased on | The purchase date of the configuration item. | Warranty valid until | The expiry date of the warranty period of the configuration item. | Retired on | Date when the configuration item goes out of service. |
| ----- | -------------------------------------------------------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------ | -------------------------------------------- | -------------------- | ----------------------------------------------------------------- | ---------- | ----------------------------------------------------- |

4. On the **Location** detail, specify the location of the configuration item.
   This data enables tracking the movement of the configuration item at
   different periods:

| Country | The location of the configuration item. The **State/province** and **City** fields are connected to the **Country** field. For example, the **Country** field will be populated automatically when you populate the **City** field. Similarly, if you enter a state, Creatio will populate the **Country** field automatically. When you populate the **Country** field, the **State** and **City** fields will display only those states and cities that correspond to the selected country. You can associate a state/province with a certain country in the **States/provinces** lookup and associate a city with a country – in the **Cities** lookup. | Region | City | Street | Start | The time when the configuration item is on the location. | End | Address | The full address of the configuration item location. Creatio populates the field automatically based on the information in the **Country** , **Region** , **City** , **Street** fields/ You can change the field value manually. |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---- | ------ | ----- | -------------------------------------------------------- | --- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

5. On the **Users** detail, specify the list of the main users of the
   configuration item. The list of CI users can include contacts, accounts, or
   departments.
   1. Click
      ![btn_com_add_tab.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_add_tab.png)
      → **Account** or **Contact**.

   2. In the window that opens, select one or more accounts → click **Select**.
      As a result, the selected account will be added to the **Users** detail
      list.

6. Add department of an account if the CI is used by separate departments only:
   1. On the **Users** detail, select an account, then click
      ![btn_com_roles_actions_menu.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_roles_actions_menu.png)
      → **Select departments**.

   2. In the window that opens, select the departments that use the
      configuration item → click **Select**.

7. On the **Components** detail, specify the list of configuration items that
   comprise the current CI.
   1. Click the
      ![btn_com_add_tab00001.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_add_tab00001.png)
      → **Related component** to add a component that affects the functioning of
      the current configuration item. When the related component is added, the
      current and related configuration items will be automatically connected on
      the **Connected configuration items** detail on the **Connected to** tab.

   2. Click the
      ![btn_com_add_tab00002.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_add_tab00002.png)
      → **Component** to add a component that is a part of the current
      configuration item. The current configuration item and the component will
      not be automatically connected through the **Connected configuration
      items** detail.

8. Select a record → click **Select**. As a result, the current configuration
   item will be specified as the parent for the added components.

note

A configuration item can only be a component of a single configuration item.

9. On the **Attachments and notes** tab, add additional information about the
   selected configuration item. Read more >>>

10. Click **Save** to save the configuration item record.

As a result, the new configuration item record with the specified parameters
will appear in the list of the **Configuration items** section.

## Link assets with services to create a service model​

A **service model** is a diagram that displays dependencies between various
elements in the IT infrastructure. The model is based on the connections between
the services and the configuration items.

To create a service model for a configuration item:

1. In the **Configuration items** section, open the record to specify the
   services and connected configuration items.

2. Click the **Connected to** tab.

3. Click
   ![btn_com_add_tab00003.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_add_tab00003.png)
   on the **Services** detail. A new record with blank fields will appear on the
   detail.

4. Select the connection category with the service in the **Category** field
   ([Fig. 1](https://academy.creatio.com#XREF_79270_96)):

Fig. 1 Selecting the connection category

![Fig. 1 Selecting the connection category](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/scr_specs_services_connected_category.png)

5. Select the "Dependent" connection category to add a link to a service, whose
   delivery depends on the current configuration item.

6. Select the "Influencer" connection category to add a link to a service whose
   operation affects the current configuration item.

7. In the **Service** field, select the linked service. For example, the "WiFi
   access" service depends on the "Router" configuration item
   ([Fig. 2](https://academy.creatio.com#XREF_13770_97)).

Fig. 2 Selecting the connected configuration item

![Fig. 2 Selecting the connected configuration item](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/scr_specs_services_connected_ci.png)

8. In the **Type** field, select a short description of connections between the
   current configuration item and the selected service. For example, the
   "Required for" connection type can be specified for the "WiFi access" service
   and the "Router" configuration item
   ([Fig. 3](https://academy.creatio.com#XREF_46967_98)).

Fig. 3 Selecting the connection type

![Fig. 3 Selecting the connection type](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/scr_specs_services_connected_type.png)

As a result, you will create a **connection** between the service and the
configuration item. If you selected the "Influencer" category, the corresponding
service will have an **inverse relation** (i.e., "Dependent") on the **Connected
to** tab of the **Configuration items** detail. The **Type** field of the
inverse relationship will be automatically populated with the inverse connection
type according to the " **Object dependency type** " lookup content. For
example, if the type of the connection is "Required for," the inverse relation
is "Installed on."

9. Specify other connections to the configuration items.

10. Add connections to the relevant configuration items by clicking
    ![btn_com_add_tab00004.png](https://academy.creatio.com/guides/sites/en/files/documentation/user/en/itsm_tools/BPMonlineHelp/manage_configuration_items/btn_com_add_tab00004.png)
    on the **Connected configuration item** detail. The procedure for linking
    configuration items is similar to that of linking services (see steps 3-6).

11. If required, open the **Services** section and add the missing connections
    between the services.

As a result, Creatio will add connections between the services and configuration
items which make the visual display of the service model possible when handling
the cases or planning the changes.

---

## See also​

[Dashboards](https://academy.bpmonline.com/documents?product=base&ver=7&id=1236)

[Manage service catalog](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1061)

[Manage service agreements](https://academy.creatio.com/documents?product=service%20enterprise&ver=7&id=1062)

- Add configuration items
- Link assets with services to create a service model
- See also
