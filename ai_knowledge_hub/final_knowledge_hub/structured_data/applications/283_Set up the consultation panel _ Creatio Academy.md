# Set up the consultation panel | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 769 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/finance-and-banking/financial-services/set-up-consultation-panel

## Description

The consultation panel is designed to facilitate the process of providing
consultations to bank clients. Click the button on the side panel to open the
consultation panel.

## Key Concepts

business process, detail, lookup, database, system setting

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3Bank Customer Journey

On this page

The consultation panel is designed to facilitate the process of providing
consultations to bank clients. Click the
![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_com_consultation_tab.png)
button on the side panel to open the consultation panel.  
Use the consultation panel to search the client database, select consultation
themes, postpone or end the consultation, as well as view additional information
about the client, such as previous applications, noteworthy events, and
individual offers.  
Before you start using the consultation panel, you need to set up the list of
blocks, groups, and themes of consultations. You can customize the rules for
searching clients by name or phone number, as well as rules for displaying
clients' noteworthy events.

## Set up consultation blocks and themes​

When communicating with the client using the consultation panel, the manager can
select consultation themes.  
The consultation themes are displayed as buttons grouped by blocks. For example,
the **Sell** block contains themes that are connected with selling bank
products. Similar themes can be combined into groups. Groups of themes can be
identified by the **& gt;** character on the right (Fig. 1). Click a theme group
to open the list of themes that are combined in the group.

Fig. 1 Displaying themes for conducting a consultation

![Fig. 1 Displaying themes for conducting a consultation](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultations_group_on_panel.png)

To set up how the consultation theme blocks and consultation themes are
displayed in the consultation panel:

1. Click to open the System Designer.

2. Go to the **System setup** block → click **Lookups**.

3. Select the **Consultation theme blocks** lookup and click **Open**.

4. Click the **Add** button to create a new consultation theme block.

5. On the consultation theme block page (Fig. 2):

Fig. 2 Filling out the page of the consultation theme block

![Fig. 2 Filling out the page of the consultation theme block](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultations_page_block.png)

     1. Enter the name of the consultation block.
     2. Select the **Show on the consultation panel** checkbox.
     3. Select the color for the title of the block and its items.

6. Select the **Group** command in the menu of the **Consultation themes**
   detail (Fig. 3).

Fig. 3 Adding a new consultation theme group

![Fig. 3 Adding a new consultation theme group](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultations_new_group.png)

7. On the **Consultation theme group** page, enter the consultation theme name
   and description. Click **Save**.
8. On the **Consultation themes** detail, select the **Theme** command.
9. Fill out the **Consultation theme** page:
   1. Enter the name and a description of the consultation theme.
   2. Select a group for the consultation theme in the **Theme group** field.
      Leave the field empty to display the consultation theme in the block,
      rather than in a group.
   3. Select the business process that will launch automatically when a theme is
      selected during the consultation. You will need to set up business
      processes for custom consultation themes separately in the Process
      Designer.
10. Click **Save**.
11. Add remaining groups and consultation themes to the block (Fig. 4).

Fig. 4 Example of a complete list of groups and consultation themes

![Fig. 4 Example of a complete list of groups and consultation themes](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultations_topic_list.png)

12. Save the consultation theme block
13. Use the same procedure to add the remaining blocks with groups and themes to
    the consultation panel.

## Set up client search conditions​

Before starting a consultation, the manager must find the individual for whom
the consultation is initiated. You can configure a minimum number of characters
that the manager must enter the search fields for the search to work.  
To set up search conditions in the consultation panel:

1. Click
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_6.png)
   to open the System Designer.

2. Click **System settings** in the **System setup** block.

3. Select the **Minimum number of characters for the Full name field**.

4. Specify the number of characters for the **Full name** field in the **Default
   value** field of the system setting page (Fig. 5).

Fig. 5 Setting up a minimum number of characters for the Name field

![Fig. 5 Setting up a minimum number of characters for the Name field](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_enter_surname.png)

5. Click **Save**.

6. Similarly, enter the default value for the **Minimum number of characters for
   the Phone number field** system setting.

7. Click **Save**.

## Set up conditions for displaying noteworthy events​

You can set up a display of the noteworthy events of your clients in the
consultation panel during the consultation.  
To set up the noteworthy events display on the consultation panel:

1. Open the System Designer by clicking
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_system_designer_6.png).
2. Click **System settings** in the **System setup** block.
3. Select the **Number of days to show noteworthy event after its occurrence**.
4. Enter the number of days, during which noteworthy events of your clients will
   be displayed in the consultation panel after they have occurred (Fig. 6).

Fig. 6 Setting the default value

![Fig. 6 Setting the default value](https://academy.creatio.com/docs/sites/en/files/2020-11/scr_bank_consultation_enter_days.png)

5. Click **Save**.
6. Specify the default value for the **Number of days to show noteworthy event
   before its occurrence** system setting.
7. Click **Save**.

---

## See also​

[Create an application](https://academy.creatio.com/documents?id=1664)

[Process an application](https://academy.creatio.com/documents?id=1666)

[Conduct a consultation](https://academy.creatio.com/documents?id=1621)

- Set up consultation blocks and themes
- Set up client search conditions
- Set up conditions for displaying noteworthy events
- See also
