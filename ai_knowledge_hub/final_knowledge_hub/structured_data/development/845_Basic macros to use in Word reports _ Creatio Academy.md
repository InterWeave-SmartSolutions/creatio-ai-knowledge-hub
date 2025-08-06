# Basic macros to use in Word reports | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 335 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/platform-customization/classic-ui/ms-word/references/basic-macros

## Description

Creatio lets you use both basic and custom macros in Word reports. Macro is a
tool that lets you convert data retrieved from Creatio into data suitable for a
Word report.

## Key Concepts

contact, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.0**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/getting-started/development-recommendations)**
(8.3).

Version: 8.0

Level: beginner

Creatio lets you use both basic and custom macros in Word reports. **Macro** is
a tool that lets you convert data retrieved from Creatio into data suitable for
a Word report.

View the structure of macro to use in Word reports below.

Structure of macro in Word reports

    ColumnName[#MacroTag|Parameters#]

View basic macros in the table below.

| Macro | Macro description | [#Date#] | Converts a date to a specified date format. Out of the box, date format is `dd.MM.yyyy`. If the date format is not specified, the retrieved date will be converted to the out-of-the-box format. Learn more about date formats: [official vendor documentation](https://learn.microsoft.com/en-us/dotnet/standard/base-types/custom-date-and-time-format-strings?redirectedfrom=MSDN). The parameter is optional.Macro usage example | Column name along with the macro | Retrieved data | Converted data | ColumnName[#Date#] | 07/15/2024 11:48:24 AM | 15.07.2024 | ColumnName[#Date | MM/dd/yyyy#] | 15/07/2024 08:25:48 AM | 07/15/2024 |
| ----- | ----------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | -------------- | -------------- | ------------------ | ---------------------- | ---------- | ---------------- | ------------ | ---------------------- | ---------- |

| [#Lower#] | Converts the string value to lowercase.Macro usage example | Column name along with the macro | Retrieved data | Converted data | ColumnName[#Lower#] | ConTaCt | contact |
| --------- | ---------------------------------------------------------- | -------------------------------- | -------------- | -------------- | ------------------- | ------- | ------- |

| [#Upper#] | Converts the string value to uppercase.Parameters | FirstChar | The first character in the string is converted to uppercase. |
| --------- | ------------------------------------------------- | --------- | ------------------------------------------------------------ |

Macro usage example

| Column name along with the macro | Retrieved data | Converted data | ColumnName[#Upper#] | contact | CONTACT | ColumnName[#Upper | FirstChar#] | contact | Contact |
| -------------------------------- | -------------- | -------------- | ------------------- | ------- | ------- | ----------------- | ----------- | ------- | ------- |

| [#NumberDigit#] | Converts a fractional number to a thousandth-separated number. Out of the box, the thousandth part is separated by space character. If the fractional part of a number is null, it is not displayed. The parameter is optional.Parameters | ,   | Thousandth part is separated by comma. |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | -------------------------------------- |

Macro usage example

| Column name along with the macro | Retrieved data | Converted data | ColumnName[#NumberDigit#] | 345566777888.567 | 345 566 777 888.567 | ColumnName[#NumberDigit | ,#] | 345566777888.567 | 345,566,777,888.567 | 345566777888.000 | 345,566,777,888 |
| -------------------------------- | -------------- | -------------- | ------------------------- | ---------------- | ------------------- | ----------------------- | --- | ---------------- | ------------------- | ---------------- | --------------- |

| [#Boolean#] | Converts a boolean value to a custom representation. The parameter is required.Parameters | CheckBox | Converts the retrieved data to `☑` or `☐`. | Yes,No | Converts the retrieved data to `Yes` or `No`. |
| ----------- | ----------------------------------------------------------------------------------------- | -------- | ------------------------------------------- | ------ | --------------------------------------------- |

Macro usage example

| Column name along with the macro | Retrieved data | Converted data | ColumnName[#Boolean | CheckBox#] | true | ☑  | ColumnName[#Boolean | Yes,No#] | true | Yes |
| -------------------------------- | -------------- | -------------- | ------------------- | ---------- | ---- | --- | ------------------- | -------- | ---- | --- |
