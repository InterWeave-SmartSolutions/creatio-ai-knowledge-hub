# Replace configuration elements | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 379 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/creatio-ide/replace-configuration-elements

## Description

Creatio development is based on the main principles of object-oriented
programming. In particular, the Creatio extension model is based on the
open-closed principle: the major Creatio logic is open for extension but closed
for modification. This means that new features must be developed by introducing
new entities rather than modifying the existing entities.

## Key Concepts

configuration, freedom ui, classic ui, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/replace-configuration-elements)**
(8.3).

Version: 8.1

On this page

Level: beginner

Creatio development is based on the main principles of object-oriented
programming. In particular, the Creatio extension model is based on the
**open-closed principle** : the major Creatio logic is open for extension but
closed for modification. This means that new features must be developed by
introducing new entities rather than modifying the existing entities.

The configuration elements in pre-installed packages are closed for modification
on the system level. Develop and modify the functionality in user-made
[packages](https://academy.creatio.com/documents?ver=8.1&id=15121) using the
**replacement mechanism**. In Creatio, the replacement implementation is based
on the concepts of replacing and replaced configuration elements.

The **replacing configuration element** is a configuration element that replaces
another configuration element of the corresponding type.

The **replaced configuration element** is a configuration element that is
replaced by another configuration element of the corresponding type.

Creatio IDE lets you replace the following **configuration elements** :

- **Client module that defines the view model**.

Client modules implement the front-end part of Creatio. To create a replacing
client module, use the replacing view model schema. To do this, follow the guide
in a separate article:
[Client module](https://academy.creatio.com/documents?ver=8.1&id=15106&anchor=title-3028-4).

- **Object**.

Objects implement the back-end of Creatio. To create a replacing object, use the
replacing object schema. To do this, follow the guide in a separate article:
[Object](https://academy.creatio.com/documents?ver=8.1&id=15107&anchor=title-3028-7).

- **Source code**.

Source code implements the back-end of Creatio. Classes serve as replacing
configuration elements. To create a replacing class, use the schema of the
**Source code** type. To do this, follow the guide in a separate article:
[Source code (C#)](https://academy.creatio.com/documents?ver=8.1&id=15108&anchor=title-3028-16).

After you implement the replacing configuration element, Creatio will execute
the logic of the replacing configuration element when accessing the element.

Creatio IDE lets you replace a single configuration element in multiple
user-made packages. The hierarchy of packages that contain the replacing
configuration elements defines the resulting implementation of the replacing
configuration element in the compiled configuration.

---

## See also​

[Packages basics](https://academy.creatio.com/documents?ver=8.1&id=15121)

[Client module](https://academy.creatio.com/documents?ver=8.1&id=15106)

[Object](https://academy.creatio.com/documents?ver=8.1&id=15107)

[Source code (C#)](https://academy.creatio.com/documents?ver=8.1&id=15108)

---

## Resources​

[Back-end development Creatio documentation](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/back-end-development)

[Front-end development Freedom UI Creatio documentation](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/freedom-ui)

[Front-end development Classic UI Creatio documentation](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/category/classic-ui)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/online-courses/development-creatio-platform-0)

- See also
- Resources
- E-learning courses
