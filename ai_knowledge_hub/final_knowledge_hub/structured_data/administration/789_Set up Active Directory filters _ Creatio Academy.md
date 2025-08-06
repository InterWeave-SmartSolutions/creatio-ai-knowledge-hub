# Set up Active Directory filters | Creatio Academy

**Category:** administration **Difficulty:** advanced **Word Count:** 695
**URL:**
https://academy.creatio.com/docs/8.x/setup-and-administration/8.1/administration/user-and-access-management/synchronize-users-with-ldap/set-up-active-directory-filters

## Description

Configure Active Directory filters to set the synchronization parameters for
users, groups, and users of a specific group.

## Key Concepts

integration, role, operation, synchronization, account, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/setup-and-administration/administration/user-and-access-management/synchronize-users-with-ldap/set-up-active-directory-filters)**
(8.3).

Version: 8.1

On this page

Configure Active Directory filters to set the synchronization parameters for
users, groups, and users of a specific group.

## The filter format​

In general, the Active Directory filter format is as follows:

    (<operator><filter1><filter2>)

Where `<filter1>` is as follows:

    (<attribute><operator><value>)

You can use any number of filters and operators during the setup. Use the
following operators to add and set up filters:

`=` – equal to

`~=` – approximately equal to

`=>` – greater than or equal to

`<=` – less than or equal to

`&` – "AND"

`|` – "OR"

`!` – "NOT"

The values represent the actual values of Active Directory attributes. The
values are not case-sensitive and should not be enclosed in quotes. You can also
use the wildcard character "**\***." For example, this condition will retrieve
all elements: `(objectClass=*)`.

Enclose each logical expression in brackets "()" to ensure the filter works
correctly both on Windows and Linux.

- A correctly set up filter
- An incorrectly setup filter

  (&(objectClass=group)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(cn=szgroup)(cn=CoreCC\*)(cn=GroupCoreCC3)))

  (&(objectClass=group)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(cn=szgroup)(cn=CoreCC\*)(cn=GroupCoreCC3)))

## Filter users​

If your company uses the Active Directory service, we recommend the standard
active user synchronization filter:

    (&(objectClass=user)(objectClass=person)(!(objectClass=computer))(!(isDeleted=TRUE)))

Where:

`&` – the "AND" operator. Indicates that all filter conditions must be met.

`objectClass=user` – selects all "user" objects in the array.

`objectClass=person` – selects all "person" objects in the array.

`!(objectClass=computer)` – excludes all "computer" objects.

`!(isDeleted=TRUE)` – specifies that the objects are not deleted.

## Filter groups​

Set up group filtering to synchronize Active Directory users with Creatio
organizational structure. The standard user group filter for all active users is
as follows:

    (&(objectClass=group)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))

Where:

`&` – the "AND" operator. Indicates that all filter conditions must be met.

`objectClass=group` – selects all "group" objects in the array.

`userAccountControl` – user account control flags, in numerical format.

`:1.2.840.113556.1.4.803:` – the bitwise "AND" in LDAP format.

`2` – the "ACCOUNTDISABLE" flag.

As such, the `(!(userAccountControl:1.2.840.113556.1.4.803:=2))` filter excludes
deactivated (inactive) user accounts. Read more in the
[Microsoft Docs](https://support.microsoft.com/en-us/kb/305144) article.

## Standard Active Directory group user filters​

Besides user and organizational structure filters, you also need to retrieve a
list of users included in the Active Directory group and therefore in LDAP. The
standard filter that retrieves a list of all group users is as follows:

    (memberOf=[#LDAPGroupDN#])

Where:

`memberOf` – standard Active Directory object attribute that determines the
object group.

`#LDAPGroupDN#` – Creatio macro used to retrieve the list of group users with
unique DN (Distinguished Name) attribute values.

The macros are not a standard LDAP attribute. Creatio only uses them to form an
object selection request. Depending on the AD settings, you can also use the
following parameters:

`#LDAPGroupName#` – the name of the group specified in the **LDAP group name**
field of LDAP integration settings.

`#LDAPGroupIdentity#` – the unique group Id specified in the **Group Id** field
of LDAP integration settings.

## Set up user/group synchronization filters​

You can create custom user and group synchronization filters depending on your
business needs.

Example

Distinguish between employees with identical full names during the Active
Directory synchronization.

To do this, make changes to the user synchronization filter. By default, Creatio
uses the CN (Common Name) attribute to select objects. This attribute is
required for correct operation as it is connected with the **User name** field.
You can also include the "displayName" attribute in the filter conditions. This
attribute will be unique for each user. As such, you need to synchronize users
with the "displayName" attribute. To do this:

1. Open the LDAP synchronization settings.

2. Add the "(displayName=\*)" condition to the default user list filter. This
   condition requires the "displayName" attribute to contain data. The filter
   will look as follows:

   (displayName=\*)(&(objectClass=user)(objectClass=person)(!(objectClass=computer))(!(isDeleted=TRUE)))

3. Add the logical "AND" operator to make both filter conditions required:

   (&(displayName=\*)(&(objectClass=user)(objectClass=person)(!(objectClass=computer))(!(isDeleted=TRUE))))

4. Replace the standard filter in the **List of users** field with the new
   filter.

5. Save the settings and run the LDAP synchronization.

---

## See also​

[Set up LDAP synchronization](https://academy.creatio.com/documents?id=513)

[Set up LDAP authentication](https://academy.creatio.com/documents?id=2367)

[Import new users and roles from Active Directory](https://academy.creatio.com/documents?id=1996)

- The filter format
- Filter users
- Filter groups
- Standard Active Directory group user filters
- Set up user/group synchronization filters
- See also
