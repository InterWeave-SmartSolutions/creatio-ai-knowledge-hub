# LocalizableValue<T> class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 375 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/back-end-development/localizable-resources/operations-with-localizable-resources/references/localizablevaluet

## Description

The Terrasoft.Common namespace.

## Key Concepts

lookup

## Use Cases

## Content

Version: 8.3

On this page

Level: advanced

The `Terrasoft.Common` namespace.

The `Terrasoft.Common.LocalizableValue<T>` class is a base class for the
`Terrasoft.Common.LocalizableString` (displays localizable strings) and
`Terrasoft.Common.LocalizableImage` (displays localizable images) classes that
work with localizable resources.

The `Terrasoft.Common.LocalizableValue<T>` class is a template for localizable
values of different types. It also provides methods that work with them.

note

View the full list of the properties, methods, and implemented interfaces of the
`LocalizableValue<T>` class in the
[.NET class reference](https://academy.creatio.com/api/netcoreapi/8.0.0/api/Terrasoft.Common.LocalizableValue%601.html).

## Properties​

    Value T

Returns and sets the localizable value based on the current language culture.

    HasValue bool

Returns the flag that determines whether a localizable value of the current type
exists for the current language culture.

    CultureValues IDictionary<CultureInfo,T>

Returns a localizable value lookup of the current instance for available
language cultures.

## Methods​

    void ClearCultureValue(CultureInfo culture)

Deletes the localizable value for available language cultures.

Parameters

| culture | A language culture. |
| ------- | ------------------- |

    T GetCultureValue(CultureInfo culture, bool throwIfNoManager)

Retrieves a localizable value of the specified type for available language
cultures. Depending on the `throwIfNoManager` parameter value, the method can
throw an exception of the `ItemNotFoundException` type if the resource manager
is not set for that localizable value.

Parameters

| culture | A language culture. | throwIfNoManager | Flag that determines whether to call the `ItemNotFoundException` exception. |
| ------- | ------------------- | ---------------- | --------------------------------------------------------------------------- |

    T GetCultureValueWithFallback(CultureInfo culture, bool throwIfNoManager)

Retrieves a localizable value of the specified type for available language
cultures. If no localizable resource value is found for the specified language
culture, returns the value for the primary language culture. Depending on the
`throwIfNoManager` parameter value, the method can throw an exception of the
`ItemNotFoundException` type if the resource manager is not set for that
localizable value.

Parameters

| culture | A language culture. | throwIfNoManager | Flag that determines whether to call the `ItemNotFoundException` exception. |
| ------- | ------------------- | ---------------- | --------------------------------------------------------------------------- |

    bool HasCultureValue(CultureInfo culture)

Determines whether a localizable value exists for the specified language
culture.

Parameters

| culture | A language culture. |
| ------- | ------------------- |

    void LoadCultureValues()

Loads an index of localizable values of the specified type for all cultures
defined in the global resource storage.

    void SetCultureValue(CultureInfo culture, T value)

Sets the specified localizable value for the specified language culture.

Parameters

| culture | A language culture. | value | A localizable value. |
| ------- | ------------------- | ----- | -------------------- |

- Properties
- Methods
