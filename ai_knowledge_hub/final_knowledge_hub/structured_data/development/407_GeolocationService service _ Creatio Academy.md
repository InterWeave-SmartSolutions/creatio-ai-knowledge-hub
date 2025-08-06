# GeolocationService service | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 324 **URL:**
https://academy.creatio.com/docs/8.x/mobile/mobile-development/customization/work-with-gps-data/references/geolocationservice

## Description

GeolocationService service returns current location using the
getCurrentCoordinates() method. Learn more: Work with GPS data in Mobile
Creatio.

## Key Concepts

user permissions, operation, case

## Use Cases

## Content

Level: beginner

`GeolocationService` service returns current location using the
`getCurrentCoordinates()` method. Learn more:
[Work with GPS data in Mobile Creatio](https://academy.creatio.com/documents?id=15173).

    getCurrentCoordinates()

Returns the result of bar code scanning.

Input parameters

GeolocationAccuracy| Accuracy to retrieve the coordinates. The time needed to
determine the coordinates depends on specified accuracy.Accuracy depends on the
following factors:

- **Environmental factors**. Buildings, trees, and other obstructions can affect
  signal strength and accuracy.
- **Device quality**. Modern mobile devices generally have more advanced
  location capabilities than older mobile devices.
- **Used technology**. GPS is typically more accurate (5-10 meters) than
  cellular data (100-1000 meters).

Available values| lowest| On Android: approximately 500 meters.  
On iOS: approximately 3000 meters.| low| On Android: approximately 500 meters.  
On iOS: approximately 1000 meters.| medium| On Android: approximately 100-500
meters.  
On iOS: approximately 100 meters.| high| On Android: approximately 0-100
meters.  
On iOS: approximately 10 meters.| best| On Android: approximately 0-100
meters.  
On iOS: approximately 0 meters.| bestForNavigation| On Android: approximately
0-100 meters.  
On iOS: optimized for navigation.| reduced| On Android: not applicable.  
On iOS 14 and later: approximately 3000 meters, consistent with the accuracy
level on iOS 13 and earlier, as well as other platforms.  
---|---

Output parameters

| latitude\* | Latitude, in degrees. If the latitude is undefined, return "0." | longitude\* | Longitude, in degrees. If the longitude is undefined, return "0." | errorCode | Error code.Available values | serviceDisabled | The `GeolocationService` service is disabled. | permissionDenied | Access to the `GeolocationService` service is limited by user permissions. | permissionDeniedForever | Access to the `GeolocationService` service is denied permanently. The Mobile Creatio does not request access again until the user enables it manually in the mobile device settings. | timeout | Operation timeout has passed. | unknown | For other unexpected cases. |
| ---------- | --------------------------------------------------------------- | ----------- | ----------------------------------------------------------------- | --------- | --------------------------- | --------------- | --------------------------------------------- | ---------------- | -------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------- | ----------------------------- | ------- | --------------------------- |

| errorMessage | Error message. | accuracy | Accuracy, in meters. | isMocked | The flag that specifies whether the location is provided by mocked provider. Android only.Available values | true | The location is provided by mocked provider. | false | The location is not provided by mocked provider. |
| ------------ | -------------- | -------- | -------------------- | -------- | ---------------------------------------------------------------------------------------------------------- | ---- | -------------------------------------------- | ----- | ------------------------------------------------ |
