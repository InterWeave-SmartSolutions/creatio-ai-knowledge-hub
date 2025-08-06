# Main menu overview | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 328 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/classic-ui/overview

## Description

The main menu is displayed in the working area (1) of the UI after the
application has been loaded. The main menu can be opened using the Menu button
located at the top (3) of the side panel (2).

## Key Concepts

section, dashboard, mobile app

## Use Cases

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

Level: beginner

The main menu is displayed in the working area (1) of the UI after the
application has been loaded. The main menu can be opened using the **Menu**
button located at the top (3) of the side panel (2).

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots.en/BasicUIElements/MainMenu/scr_intro_ui_mainmenu.PNG)

Main menu commands used for opening system sections are also available in the
section area (5) of the side panel (2). The list of available section navigation
commands depends on the selected workplace (4).

Two schemas correspond to the main menu: the base schema of the
`ApplicationMainMenu` business object and the product main menu schema inherited
from the base product main menu schema `SimpleIntro`. For the `SalesEnterprise`
product, the main menu schema is named `EnterpriseIntro`.

The element composition of the main menu UI depends on the product. All elements
are placed in corresponding containers that are set up in the base or inherited
schema of the main menu. The primary containers of the SalesEnterprise product
include:

- Menu main container (`MainContainer`), which contains all main menu elements.
- Section and setting container (`LeftContainer`), which contains areas for
  commands that open sections and settings.
- Resource container (`RightContainer`), which contains areas with links to
  various resources.
- Base functionality container (`BasicTile`), which contains commands for
  opening sections that are available in all products.
- Sales container (`SalesTile`), which contains commands for opening sections of
  the Sales product family.
- Analytics container (`AnalyticsTile`), which contains command for opening the
  **Dashboards** section.
- Settings container (`SettingsTile`), which contains commands for opening the
  settings sections.
- Video container (`VideoPanel`), which contains video player and name of the
  linked video.
- Link container (`LinksContainer`), which contains links to training web
  resources and social networks.
- Mobile app links container (`MobileAppLinksPanel`), which contains links to
  Creatio mobile app in various app stores.
