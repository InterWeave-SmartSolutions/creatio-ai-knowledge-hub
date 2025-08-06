# Check-in verification for sales reps | Creatio Academy

**Category:** applications **Difficulty:** advanced **Word Count:** 746 **URL:**
https://academy.creatio.com/docs/8.x/creatio-apps/products/more-apps/field-management/checkin-verification

## Description

You can control sales rep’s wok by setting up the check-in performance and
verification parameters during visits. Use custom details, dynamic folders, or
dashboards to display check-in results.

## Key Concepts

section, detail, dashboard, system setting, mobile app, synchronization, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

You can control sales rep’s wok by setting up the check-in performance and
verification parameters during visits. Use custom details, dynamic folders, or
dashboards to display check-in results.

Creatio stores detailed check-in information including the source of received
coordinates and the time of receiving the coordinates from GPS. Current time is
indicated for the coordinates received in real-time while the time of caching is
used for the cached coordinates.

## Check-in verification procedure​

Whenever a sales rep performs the check-in action, Creatio captures the current
or cached coordinates of the latest sales rep’s location and compares them to
the account’s address coordinates. The allowable discrepancy between these
coordinates is specified in meters in the "Check-in verification range" system
setting ("CheckInRadius" code).

The last added address marked as **Primary** is used for verification. The
check-in is not verified if it was not possible to obtain the coordinates and if
the value of the"Check-in verification range" system settings ("CheckInRadius"
code) is not specified.

- If the GPS coordinates of the sales rep and the visited account **are in the
  verification range** , the check-in will be verified and the status of the
  visit will be changed to "In progress." The "Check-in coordinates are within
  range" status will be displayed on the **Check-in and check-out performance
  result** detail.
- If the discrepancy between the GPS coordinates of the sales rep and the
  visited account **exceed the verification range** , the sales rep will receive
  the following message: "Check-in coordinates are out of range. Would you like
  to save check-in results?" If this result is saved, the check-in will have the
  "Check-in coordinates are out of range" status.
- If the **check-in verification is not possible** (the address of an account is
  not specified or a sales rep had no Internet connection during the
  verification process), the sales rep will receive the following message:
  "Unable to verify check-in coordinates. Would you like to save check-in
  results?" If the check-in results are saved, the check-in will have the
  "Unable to verify check-in coordinates" status.

## Set up check-in verification​

Use the following
[system settings](https://academy.creatio.com/documents?id=269) to set up
check-in verification:

- **"Use last known location of user"** ("UseMobileLastKnownLocation" code).
  This system setting enables a mobile device to use the latest cached sales
  rep’s location and save it as the check-in location if the actual check-in
  coordinates are unknown. This usually occurs when sales reps perform check-in
  inside buildings, where GPS signal may be unavailable.

note

Functions of working with cached coordinates are available for Android OS
devices.

- **"Check-in verification range"** ("CheckInRadius" code). This system setting
  enables you to control the check-in performance by a sales rep. It helps
  identify the acceptable discrepancy (in meters) between the sales rep’s
  coordinates at the time of check-in and the coordinates of the corresponding
  sales outlet. Specified distance will be used for check-in verification.

Important

If the range value is not specified, check-in verification will not be
performed.

You can
[add the **Check-in and check-out performance result** detail](https://academy.creatio.com/documents?id=2032)
based on the **Check-in and check-out performance result** object to display the
check-in results and show the columns in the detail list on Creatio primary
application page.

## Get check-in verification results​

To track the check-in results, you can
[configure a dynamic folder](https://academy.creatio.com/documents?id=1018) in
the **Activities** section, or a
[dashboard](https://academy.creatio.com/documents?id=1405) in the dashboards
view of this section. An example of configuring the filtering conditions for all
visits with unverified check-in (Fig. 1).

Fig. 1 Filtration conditions of all visits with unverified check-in

![Fig. 1 Filtration conditions of all visits with unverified check-in](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/field_module/check-in_filter_setup.png)

note

More information about work with folders and dashboards is available in the
separate articles: [Folders](https://academy.creatio.com/documents?id=1018) and
[Dashboard](https://academy.creatio.com/documents?id=1405) tiles.

## View coordinates on the map​

To track the coordinates of the sales rep check-in and check-out:

1. Open the visit page.

2. Click the
   ![](https://academy.creatio.com/docs/sites/default/files/inline-images/btn_show_on_map_check-in_check-out.png)
   button on the **Actions - Visit** detail (Fig. 2).

Fig. 2 Viewing check-in/check-out coordinates on the map

![Fig. 2 Viewing check-in/check-out coordinates on the map](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/field_module/chapter_field_force_open_check-in_map.png)

This will open a window with a map, that contain markers that represent GPS
coordinates of an account and sales rep during check-in and check-out (Fig. 3).

Fig. 3 Visit map with account coordinates, check-in, and check-out

![Fig. 3 Visit map with account coordinates, check-in, and check-out](https://academy.creatio.com/docs/sites/en/files/images/More_Apps/field_module/chapter_field_force_check-in_on_map.png)

Sales rep GPS coordinates will be displayed on the map after check-in and/or
check-out in the mobile app and synchronization of mobile app with Creatio
primary application.

---

## See also​

[Install Field Management for Creatio](https://academy.creatio.com/documents?id=1374)

[Set up rules and actions of a visit](https://academy.creatio.com/documents?id=1375)

[Schedule sales rep visits](https://academy.creatio.com/documents?id=2333)

[Sales rep visit actions](https://academy.creatio.com/documents?id=2334)

- Check-in verification procedure
- Set up check-in verification
- Get check-in verification results
- View coordinates on the map
- See also
