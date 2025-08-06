# Front-end (JS) development basics | Creatio Academy

**Category:** development **Difficulty:** intermediate **Word Count:** 1179
**URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/architecture/development-in-creatio/front-end-js

## Description

The front-end platform is a set of modules that are defined and loaded
asynchronously on demand.

## Key Concepts

configuration, section, detail, operation, package, customization

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

Version: 8.3

On this page

Level: beginner

The front-end platform is a set of modules that are defined and loaded
asynchronously on demand.

The core is the basis of Creatio's front-end.

The core level provides:

- the ability to use the object-oriented approach and inheritance technique
- the tools to define and asynchronously load modules and their dependencies
- the functionality of base Creatio elements
- the module communication mechanism

Front-end development in Creatio is done on the configuration level and comes
down to creating new and expanding base visual modules, as well as non-visual
modules, view models.​

## Creatio's front-end core components​

![](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots.en/Frontend/scr_frontend_core.png)

### External JS libraries​

**ExtJS** – a JavaScript framework used for web application and UI development.
Creatio uses ExtJS as a mechanism to establish the class structure of the core's
client segment. ExtJS enables an object-oriented approach, which is not
implemented in pure JavaScript. Use it to establish classes, implement an
inheritance hierarchy, and group classes into namespaces.

**RequireJS** – a library that implements the
[Asynchronous Module Definition (AMD)](http://en.wikipedia.org/wiki/Asynchronous_module_definition)
approach. The AMD approach declares the mechanism for the definition and
asynchronous loading of modules and their dependencies.

**Angular** – a JavaScript framework for single-page application development.
Use it to expand browser applications based on the MVC template as well as to
streamline testing and development. Creatio supports embedding custom Angular
components using a common Angular core.

### Base JS classes​

An unmodifiable part of Creatio. These classes:

- Ensure the operation of the client configuration modules.
- Define the functionality of base Creatio objects, controls, lists, and
  constants.
- Are stored as executable files in Creatio folders on the drive.

### Messaging​

**Sandbox** – the core component that manages the interaction of Creatio
modules. The sandbox lets Creatio exchange data between the modules
(`sandbox.publish()` and `sandbox.subscribe()` methods) and load the modules
into the Creatio UI on demand (`sandbox.load()` module).

## Asynchronous module definition​

The front-end platform has a **modular structure**.

**Module** – a functionality set encapsulated in a separate block that can also
use other modules as dependencies.

Module creation in JavaScript is determined by the "Module" design pattern. A
classic example of this pattern's implementation is using anonymous functions
that return a specific value (an object, a function, etc.) associated with the
module. The module's value is then exported to the global object.

To manage a large number of modules, Creatio loads modules and their
dependencies according to the **Asynchronous Module Definition** (AMD) approach.

The AMD approach declares the mechanism that defines modules and loads them
alongside their dependencies asynchronously. This mechanism allows Creatio to
load only the data that is necessary for a particular task. Creatio uses
**RequireJS** loader for working with modules.

Module definition **principles** in Creatio:

- The module is defined by a special `define()` function that registers a
  function factory for the module's instantiation. However, this function does
  not immediately load the module when called.
- The module's dependencies are passed as a string value array, not via the
  properties of the global object.
- The loader loads all dependency modules passed as the arguments to `define()`.
  The modules load asynchronously. The loader determines their actual load order
  arbitrarily.
- Once the loader loads all specified dependencies of the module, the function
  factory that returns the module's value is called. Loaded dependency modules
  are passed as arguments to the function factory.

## Modular development in Creatio​

Creatio uses **client modules** to implement the entirety of the custom
functionality.

The module hierarchy in Creatio

![The module hierarchy in Creatio](https://academy.creatio.com/sites/en/files/documentation/sdk/en/BPMonlineWebSDK/Screenshots.en/Frontend/scr_modules.png)

Despite some functional differences, all client modules in Creatio have the same
description structure that follows the AMD module description format.

General client module description structure

    define("ModuleName", "dependencies", function(dependencies) {
            // someMethods…
            return { moduleObject };
    });

- `ModuleName` – the module's name
- `dependencies` – dependency modules whose functionality the current module can
  use
- `moduleObject` – the module's configuration object

Creatio has several **types** of client modules.

- The non-visual module
- The visual module
- The view model scheme

### Non-visual module​

This module implements Creatio functionality that is not associated with data
binding and displaying data in the UI.

Non-visual module's description structure

    define("ModuleName", "dependencies", function(dependencies) {
        // Methods that implement the necessary business logic.
        return;
    });

Non-visual module examples: utility modules that fulfill service functions.

### Visual module​

Use this module to create custom visual elements in Creatio.

The view model follows the MVVM template. The visual module encapsulates data
displayed in the GUI's controls as well as the methods for working with such
data.

It has the following **methods** :

- `init()` – the module initialization method.

Manages the initialization of the class object's properties as well as the
message subscription.

- `render(renderTo)` – the module view's DOM rendering method.

Returns the view.

This method only accepts the `renderTo` argument that specifies the element
where the module object's view will be embedded.

- `destroy()` – the method that manages the deletion of the module's model or
  the view model, the unsubscription from the previously subscribed messages,
  and the destruction of the module class's object.

You can use the base core classes to create a visual module. For instance, you
can create a class that inherits from `Terrasoft.configuration.BaseModule` or
`Terrasoft.configuration.BaseSchemaModule` in the module. These base classes
already have a minimal implementation of the essential visual module methods –
`init()`, `render(renderTo)` and `destroy()`.

Structure description of a visual module that inherits from Terrasoft.BaseModule
base class

    define("ModuleName", "dependencies", function(dependencies) {
        // The definition of the module's class.
        Ext.define("Terrasoft..configuration.className") {
            alternateClassName: "Terrasoft.className"
            extend: "Terrasoft.BaseModule",
            ...
            // Properties and methods.
            ...
        };
        // Creating the module's object.
        return Ext.create(Terrasoft.className)
    });

Visual module examples: modules in charge of controls on Creatio pages.

### View model schema​

The most common Creatio customization problems include creating and tweaking
basic interface elements: sections, pages, details.

These elements' modules have a **pattern-based structure**. They are called view
model schemas.

A view model schema is a configuration object Creatio generators `ViewGenerator`
and `ViewModelGenerator` use to generate the view and the view model.

The base schema substitution mechanism is used for most problems related to
Creatio customization. This includes all the schemas in pre-installed
configuration packages.

The most common base view model schemas are as follows:

- `BasePageV2`
- `BaseSectionV2`
- `BaseDetailV2`

View model schema's structure

    define("SchemaName", "dependencies", function(dependencies) {
        return {
            entitySchemaName: "ExampleEntity",
            mixins: {},
            attributes: {},
            messages: {},
            methods: {},
            rules: {},
            businessRules: {},
            modules: {},
            diff:
        };
    });

View model schema examples: page, section and detail schemes.

---

## See also​

[Back-end (C#)](https://academy.creatio.com/documents?ver=8.3&id=15083)

---

## E-learning courses​

[Development on Creatio platform](https://academy.creatio.com/online-courses/node/529657)

- Creatio's front-end core components
  - External JS libraries
  - Base JS classes
  - Messaging
- Asynchronous module definition
- Modular development in Creatio
  - Non-visual module
  - Visual module
  - View model schema
- See also
- E-learning courses
