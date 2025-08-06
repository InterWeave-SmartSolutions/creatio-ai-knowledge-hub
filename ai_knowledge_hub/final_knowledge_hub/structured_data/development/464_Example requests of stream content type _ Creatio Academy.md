# Example requests of stream content type | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 1919 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/integrations-and-api/data-services/odata/examples/stream-data-type-request-examples

## Description

odata service lets you work with the following Stream content types:

## Key Concepts

odata, sql, database, role, campaign, lead, contact, account

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

On this page

Level: advanced

`odata` service lets you work with the following `Stream` content types:

- **Images**
- **Files**
- **Binaries**

## Retrieve content of the Stream type​

To implement the example:

1. Retrieve the ID of the contact photo. Read more >>>
2. Retrieve the contact photo. Read more >>>

Example

Retrieve the photo of a specified Creatio contact using the `odata` service.

- Response

  Status: 200 OK

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_Alexander_Wilson_photo.png)

### 1\. Retrieve the ID of the contact photo​

For this example, retrieve the ID of the following photo for "Alexander Wilson"
contact.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_Alexander_Wilson_in_Creatio.png)

To do this, execute the SQL query to the `SysImage` database table whose `Data`
column stores the contact photos.

SQL query

    select Id from SysImage where Id = (select PhotoId from Contact where Name = 'Alexander Wilson')

**As a result** , the database will return the ID of the contact photo. For this
example, the ID is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."

### 2\. Retrieve the contact photo​

For this example, retrieve the photo of "Alexander Wilson" contact. To do this,
execute the request using the `odata` service.

Request

    // Retrieve the "Data" column value of the "SysImage" database table for the contact whose ID is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."
    GET CreatioURL/0/odata/SysImage(E07885D2-90AB-42AC-59B5-EF80EB6B8F09)/Data

**As a result** , Creatio will return the photo of "Alexander Wilson" contact.
[View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15433&anchor=view-result)

## Add content of the Stream type​

To implement the example:

1. Add a contact. Read more >>>
2. Add a record to the database. Read more >>>
3. Upload the file of contact photo to the database. Read more >>>
4. Bind the photo to the contact. Read more >>>

Example

Add a new contact using the `odata` service. The contact must contain the photo.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_John_Best_in_Creatio_with_photo.png)

### 1\. Add a contact​

For this example, add the "John Best" contact using the `odata` service. To do
this, execute the request to the `Contact` database table that stores contacts.

Request

    // Add the contact to the "Contact" database table.
    POST CreatioURL/0/odata/Contact

    Accept: application/json; odata=verbose
    Content-Type: application/json; odata=verbose; IEEE754Compatible=true
    // Specify "BPMCSRF" header when using cookie-based authentication.
    BPMCSRF: SomeBPMCSRFToken

    {
        // Set the "John Best" contact name to the "Name" field.
        "Name": "John Best"
    }

**As a result** :

- Creatio will return the following response.

Response

        Status: 201 Created

        {
            "@odata.context": "CreatioURL/0/odata/$metadata#Contact/$entity",
            "Id": "509c189d-37a0-49d5-80f4-7de9ab389f3a",
            "Name": "John Best",
            "OwnerId": "76929f8c-7e15-4c64-bdb0-adc62d383727",
            "CreatedOn": "2024-09-16T07:46:44.5045174Z",
            "CreatedById": "76929f8c-7e15-4c64-bdb0-adc62d383727",
            "ModifiedOn": "2024-09-16T07:46:44.5045174Z",
            "ModifiedById": "76929f8c-7e15-4c64-bdb0-adc62d383727",
            "ProcessListeners": 0,
            "Dear": "",
            "SalutationTypeId": "00000000-0000-0000-0000-000000000000",
            "GenderId": "00000000-0000-0000-0000-000000000000",
            "AccountId": "00000000-0000-0000-0000-000000000000",
            "DecisionRoleId": "00000000-0000-0000-0000-000000000000",
            "TypeId": "00000000-0000-0000-0000-000000000000",
            "JobId": "00000000-0000-0000-0000-000000000000",
            "JobTitle": "",
            "DepartmentId": "00000000-0000-0000-0000-000000000000",
            "BirthDate": "0001-01-01T00:00:00Z",
            "Phone": "",
            "MobilePhone": "",
            "HomePhone": "",
            "Skype": "",
            "Email": "",
            "AddressTypeId": "00000000-0000-0000-0000-000000000000",
            "Address": "",
            "CityId": "00000000-0000-0000-0000-000000000000",
            "RegionId": "00000000-0000-0000-0000-000000000000",
            "Zip": "",
            "CountryId": "00000000-0000-0000-0000-000000000000",
            "DoNotUseEmail": false,
            "DoNotUseCall": false,
            "DoNotUseFax": false,
            "DoNotUseSms": false,
            "DoNotUseMail": false,
            "Notes": "",
            "Facebook": "",
            "LinkedIn": "",
            "Twitter": "",
            "FacebookId": "",
            "LinkedInId": "",
            "TwitterId": "",
            "TwitterAFDAId": "00000000-0000-0000-0000-000000000000",
            "FacebookAFDAId": "00000000-0000-0000-0000-000000000000",
            "LinkedInAFDAId": "00000000-0000-0000-0000-000000000000",
            "PhotoId": "00000000-0000-0000-0000-000000000000",
            "GPSN": "",
            "GPSE": "",
            "Surname": "Best",
            "GivenName": "John",
            "MiddleName": "",
            "Confirmed": true,
            "Completeness": 0,
            "LanguageId": "6ebc31fa-ee6c-48e9-81bf-8003ac03b019",
            "Age": 0,
            "IsEmailConfirmed": false,
            "AdCampaignId": "00000000-0000-0000-0000-000000000000",
            "CustomerNeedId": "00000000-0000-0000-0000-000000000000",
            "ChannelId": "00000000-0000-0000-0000-000000000000",
            "SourceId": "00000000-0000-0000-0000-000000000000",
            "RegisterMethodId": "00000000-0000-0000-0000-000000000000",
            "LeadConversionScore": 0,
            "IsNonActualEmail": false,
            "ContactPhoto@odata.mediaEditLink": "Contact(509c189d-37a0-49d5-80f4-7de9ab389f3a)/ContactPhoto",
            "ContactPhoto@odata.mediaReadLink": "Contact(509c189d-37a0-49d5-80f4-7de9ab389f3a)/ContactPhoto",
            "ContactPhoto@odata.mediaContentType": "application/octet-stream"
        }


The "John Best" ID is "509c189d-37a0-49d5-80f4-7de9ab389f3a."

- The `odata` service will add the "John Best" contact to Creatio.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_John_Best_in_Creatio.png)

### 2\. Add a record to the database​

To do this, execute the request to the `SysImage` database table using the
`odata` service. The `SysImage` database table stores the contact photos.

Request

    // Add the record to the "SysImage" database table.
    POST CreatioURL/0/odata/SysImage

    Accept: application/json; odata=verbose
    Content-Type: application/json; odata=verbose; IEEE754Compatible=true
    // Specify "BPMCSRF" header when using cookie-based authentication.
    BPMCSRF: SomeBPMCSRFToken

    {
        // Set the file name of the contact photo to the "Name" column.
        "Name": "src_John_Best_photo.png",
        // Set an arbitrary record ID to the "Id" column.
        "Id": "410006E1-CA4E-4502-A9EC-E54D922D2C02",
        // Set the file type of the contact photo to the "MimeType" column.
        "MimeType": "image/png"
    }

**As a result** :

- Creatio will return the following response.

Response

        Status: 201 Created

        {
            "@odata.context": "CreatioURL/0/odata/$metadata#SysImage/$entity",
            "Id": "410006e1-ca4e-4502-a9ec-e54d922d2c02",
            "CreatedOn": "2024-09-17T06:27:20.1826947Z",
            "CreatedById": "410006e1-ca4e-4502-a9ec-e54d922d2c00",
            "ModifiedOn": "2024-09-17T06:27:20.1826947Z",
            "ModifiedById": "410006e1-ca4e-4502-a9ec-e54d922d2c00",
            "ProcessListeners": 0,
            "UploadedOn": "0001-01-01T00:00:00Z",
            "Name": "src_John_Best_photo.png",
            "MimeType": "image/png",
            "HasRef": false,
            "Hash": "",
            "Data@odata.mediaEditLink": "SysImage(410006e1-ca4e-4502-a9ec-e54d922d2c02)/Data",
            "Data@odata.mediaReadLink": "SysImage(410006e1-ca4e-4502-a9ec-e54d922d2c02)/Data",
            "Data@odata.mediaContentType": "application/octet-stream",
            "PreviewData@odata.mediaEditLink": "SysImage(410006e1-ca4e-4502-a9ec-e54d922d2c02)/PreviewData",
            "PreviewData@odata.mediaReadLink": "SysImage(410006e1-ca4e-4502-a9ec-e54d922d2c02)/PreviewData",
            "PreviewData@odata.mediaContentType": "application/octet-stream"
        }


- The `SysImage` database table will include the record, however the value of
  the `Data` column will be "0x."

### 3\. Upload the file of contact photo to the database​

Upload the file of contact photo to the `Data` column of the `SysImage` database
table:

1. **Check the file name**. To do this, ensure the file name of contact photo
   matches the value specified in the `Name` property of the request body on the
   previous step.

2. **Execute the request to the** `SysImage` **database table** using the
   `odata` service.
   - Request


    // Update the value of the "Data" column in the "SysImage" database table whose "Id" column value is "410006e1-ca4e-4502-a9ec-e54d922d2c02."
    PUT CreatioURL/0/odata/SysImage(410006e1-ca4e-4502-a9ec-e54d922d2c02)/Data

    Accept: application/json; text/plain; /*/
    Content-Type: application/octet-stream; IEEE754Compatible=true
    // Specify "BPMCSRF" header when using cookie-based authentication.
    BPMCSRF: SomeBPMCSRFToken

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_John_Best_photo.png)

**As a result** , Creatio will return the following response.

Response

    Status: 200 OK

### 4\. Bind the photo to the contact​

For this example, bind the photo to the "John Best" contact.

Bind the `Data` column value of the `SysImage` database table to the `PhotoId`
column value of the `Contact` database table:

1. **Execute the request to the** `Contact` **database table** using the `odata`
   service.

Request

         // Update the value of the "PhotoId" column in the "Contact" database table whose "Id" column value is "509c189d-37a0-49d5-80f4-7de9ab389f3a."
         PATCH CreatioURL/0/odata/Contact(509c189d-37a0-49d5-80f4-7de9ab389f3a)

         Accept: application/json;odata=verbose
         Content-Type: application/json; odata=verbose; IEEE754Compatible=true
         // Specify "BPMCSRF" header when using cookie-based authentication.
         BPMCSRF: SomeBPMCSRFToken

         {
             // Set the ID of the contact photo specified in the "SysImage" database table to the "PhotoId" column.
             "PhotoId": "410006e1-ca4e-4502-a9ec-e54d922d2c02"
         }


2. **Clear the browser cache**.

**As a result** :

- Creatio will return the following response.

Response

        Status: 204 No Content


- The `odata` service will add the photo of the "John Best" contact to Creatio.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15433&anchor=view-result-1)

## Modify content of the Stream type​

To implement the example:

1. Retrieve the ID of the contact photo. Read more >>>
2. Upload the file of new contact photo to the database. Read more >>>

Example

Change the photo of the existing contact using the `odata` service.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_new_photo_of_Alexander_Wilson_in_Creatio.png)

### 1\. Retrieve the ID of the contact photo​

For this example, retrieve the ID of the following photo for "Alexander Wilson"
contact.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_Alexander_Wilson_in_Creatio.png)

To do this, execute the SQL query to the `SysImage` database table whose `Data`
column stores the contact photos.

SQL query

    select Id from SysImage where Id = (select PhotoId from Contact where Name = 'Alexander Wilson')

**As a result** , the database will return the ID of the contact photo. For this
example, the ID is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."

### 2\. Upload the file of new contact photo to the database​

Upload the file of contact photo to the `Data` column of the `SysImage` database
table:

1. **Execute the request to the** `SysImage` **database table** using the
   `odata` service.
   - Request


    // Update the value of the "Data" column in the "SysImage" database table whose "Id" column value is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."
    PUT CreatioURL/0/odata/SysImage(E07885D2-90AB-42AC-59B5-EF80EB6B8F09)/Data

    Accept: application/json; text/plain; /*/
    Content-Type: application/octet-stream; IEEE754Compatible=true
    // Specify "BPMCSRF" header when using cookie-based authentication.
    BPMCSRF: SomeBPMCSRFToken

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_John_Best_photo.png)

2. **Clear the browser cache**.

**As a result** :

- Creatio will return the following response.

Response

        Status: 200 OK


- The `odata` service will change the photo of "Alexander Wilson" contact in
  Creatio.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15433&anchor=view-result-2)

## Delete content of the Stream type​

To implement the example:

1. Retrieve the ID of the contact photo. Read more >>>
2. Delete the contact photo. Read more >>>

Example

Delete the photo of the existing contact using the `odata` service.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_Alexander_Wilson_in_Creatio_without_photo.png)

### 1\. Retrieve the ID of the contact photo​

For this example, retrieve the ID of the following photo for "Alexander Wilson"
contact.

![](https://d3a7ykdi65m4cy.cloudfront.net/ac-en/s3fs-public/documentation/sdk/en/BPMonlineWebSDK/Screenshots/StreamData/8.1/src_Alexander_Wilson_in_Creatio.png)

To do this, execute the SQL query to the `SysImage` database table whose `Data`
column stores the contact photos.

SQL query

    select Id from SysImage where Id = (select PhotoId from Contact where Name = 'Alexander Wilson')

**As a result** , the database will return the ID of the contact photo. For this
example, the ID is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."

### 2\. Delete the contact photo​

Delete the file of contact photo from the `Data` column of the `SysImage`
database table:

1. **Execute the following request to the** `SysImage` **database table** using
   the `odata` service.

Request

         // Delete the value of the "Data" column in the "SysImage" database table whose "Id" column value is "E07885D2-90AB-42AC-59B5-EF80EB6B8F09."
         DELETE CreatioURL/0/odata/SysImage(E07885D2-90AB-42AC-59B5-EF80EB6B8F09)/Data

         Accept: application/json; text/plain; /*/
         Content-Type: application/octet-stream; IEEE754Compatible=true
         // Specify "BPMCSRF" header when using cookie-based authentication.
         BPMCSRF: SomeBPMCSRFToken


2. **Clear the browser cache**.

**As a result** :

- Creatio will return the following response.

Response

        Status: 204 No Content


- The `odata` service will delete the photo of "Alexander Wilson" contact in
  Creatio.
  [View the result >>>](https://academy.creatio.com/documents?ver=8.0&id=15433&anchor=view-result-3)

---

## Resources​

[Creatio API documentation](https://documenter.getpostman.com/view/10204500/SztHX5Qb?version=latest#a3eb86a2-c11d-4c55-ad19-4481a8bf4876)

- Retrieve content of the Stream type
  - 1\. Retrieve the ID of the contact photo
  - 2\. Retrieve the contact photo
- Add content of the Stream type
  - 1\. Add a contact
  - 2\. Add a record to the database
  - 3\. Upload the file of contact photo to the database
  - 4\. Bind the photo to the contact
- Modify content of the Stream type
  - 1\. Retrieve the ID of the contact photo
  - 2\. Upload the file of new contact photo to the database
- Delete content of the Stream type
  - 1\. Retrieve the ID of the contact photo
  - 2\. Delete the contact photo
- Resources
