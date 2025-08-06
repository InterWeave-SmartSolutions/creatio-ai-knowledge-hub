# Module class | Creatio Academy

**Category:** development **Difficulty:** beginner **Word Count:** 2221 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.0/front-end-development/classic-ui/modules/overview

## Description

Declare a module class

## Key Concepts

configuration, lookup, package, case

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

Level: intermediate

## Declare a module class​

**Class declaration** is a function of the `ExtJS` JavaScript framework. To
**declare a class** , use the `define()` method of the global `Ext` object. This
is the standard library mechanism.

Example that declares a class using the define() method

    /* Class name that uses a namespace. */
    Ext.define("Terrasoft.configuration.ExampleClass", {
        /* The short class name. */
        alternateClassName: "Terrasoft.ExampleClass",
        /* Name of the class from which the current class inherits. */
        extend: "Terrasoft.BaseClass",
        /* The configuration object that contains declarations of static properties and methods. */
        static: {
            /* Example of a static property. */
            myStaticProperty: true,

            /* Example of a static method. */
            getMyStaticProperty: function () {
                /* Example that accesses a static property. */
                return Terrasoft.ExampleClass.myStaticProperty;
            }
        },
        /* Example of a dynamic property. */
        myProperty: 12,
        /* Example of a dynamic class method. */
        getMyProperty: function () {
            return this.myProperty;
        }
    });

View the examples that create class instances below.

- Example that creates a class instance using the full name
- Example that creates a class instance using a short name

  /_ Create a class instance using the full name. _/  
  var exampleObject = Ext.create("Terrasoft.configuration.ExampleClass");

  /_ Create a class instance using the alias (the short name). _/  
  var exampleObject = Ext.create("Terrasoft.ExampleClass");

## Inherit from a module class​

In most cases, you need to inherit the module class from the `BaseModule` or
`BaseSchemaModule` classes of the `Terrasoft.configuration` namespace.

The `BaseModule` and `BaseSchemaModule` classes implement the following
**methods** :

- `init()`. Implements the logic that is executed when loading the module. The
  client core calls this method first automatically when loading the module. The
  `init()` method usually subscribes to events of other modules and initializes
  the module values.
- `render(renderTo)`. Implements the module visualization logic. The client core
  calls this method automatically when loading the module. To ensure data is
  displayed correctly, trigger the mechanism that binds the view (`View`) and
  view model (`ViewModel`) before data visualization. Usually, this mechanism is
  initiated in the `render()` method by calling the `bind()` method in the view
  object. If you load the module into a container, pass the link to the
  container to the `render()` method as an argument. The `render()` method is
  required for visual modules.
- `destroy()`. Responsible for deleting the module view, deleting the view
  model, unsubscribing from previously subscribed messages, and deleting the
  module class object.

View the example of a module class that inherits from the `Terrasoft.BaseModule`
class below. The module adds a button to DOM. When you click the button, Creatio
displays a message and deletes the button from DOM.

Example of a module class that inherits from the Terrasoft.BaseModule class

    define("ModuleExample", [], function () {
        Ext.define("Terrasoft.configuration.ModuleExample", {
            /* The short class name. */
            alternateClassName: "Terrasoft.ModuleExample",
            /* Name of the class from which the current class inherits. */
            extend: "Terrasoft.BaseModule",
            /* Required. If omitted, Creatio generates an error on the Terrasoft.core.BaseObject level because the class inherits from the Terrasoft.BaseModule class. */
            Ext: null,
            /* Required. If omitted, Creatio generates an error on the Terrasoft.core.BaseObject level because the class inherits from the Terrasoft.BaseModule class. */
            sandbox: null,
            /* Required. If omitted, Creatio generates an error on the Terrasoft.core.BaseObject level because the class inherits from the Terrasoft.BaseModule class. */
            Terrasoft: null,
            /* View model. */
            viewModel: null,
            /* View. The example uses a button. */
            view: null,
            /* If you do not implement the init() method in the current class, Creatio calls the init() method of the Terrasoft.BaseModule parent class when you create an instance of the current class. */
            init: function () {
                /* Execute the logic of the init() method of the parent class. */
                this.callParent(arguments);
                this.initViewModel();
            },
            /* Initialize the view model. */
            initViewModel: function () {
                /* Save the scope of a module class to provide access to the module from the view model. */
                var self = this;
                /* Create a view model. */
                this.viewModel = Ext.create("Terrasoft.BaseViewModel", {
                    values: {
                        /* Button caption. */
                        captionBtn: "Click Me"
                    },
                    methods: {
                        /* Button click handler. */
                        onClickBtn: function () {
                            var captionBtn = this.get("captionBtn");
                            alert(captionBtn + " button was pressed");
                            /* Call the method that unloads the view and view model to delete the button from DOM. */
                            self.destroy();
                        }
                    }
                });
            },
            /* Create a view (button), link it to a view model, and add it to DOM. */
            render: function (renderTo) {
                /* Create a button as a view. */
                this.view = this.Ext.create("Terrasoft.Button", {
                    /* Container to add the button. */
                    renderTo: renderTo,
                    /* The id HTML attribute. */
                    id: "example-btn",
                    /* Class name. */
                    className: "Terrasoft.Button",
                    /* Caption. */
                    caption: {
                        /* Link the button caption to the captionBtn property of the view model. */
                        bindTo: "captionBtn"
                    },
                    /* Handler method for the button click event. */
                    click: {
                        /* Link the handler method for the button click event to the onClickBtn() method of the view model. */
                        bindTo: "onClickBtn"
                    },
                    /* Button style. */
                    style: this.Terrasoft.controls.ButtonEnums.style.GREEN
                });
                /* Bind the view and view model. */
                this.view.bind(this.viewModel);
                /* Return the view that is added to DOM. */
                return this.view;
            },
            /* Delete unused objects. */
            destroy: function () {
                /* Delete the view to delete the button from DOM. */
                this.view.destroy();
                /* Delete the unused view model. */
                this.viewModel.destroy();
            }
        });
        /* Return the module object. */
        return Terrasoft.ModuleExample;
    });

## Overload module class members​

When you inherit from a module class, you can overload public and private
properties and methods of a base module in an inheritor class.

**Private class properties or methods** are properties or methods whose names
start with an underscore character, for example, `_privateMemberName`.

The **purpose** of tracking is to check if overloads of private properties or
methods declared in parent classes are executed when declaring a custom class.
The browser console displays an overload warning in debug mode. Learn more in a
separate article:
[Front-end debugging](https://academy.creatio.com/documents?ver=8.0&id=15193).

To **track overloads of private members of a module class** , use the
`Terrasoft.PrivateMemberWatcher` class.

For example, a user-made package includes the `UsrPrivateMemberWatcher` module
schema.

UsrPrivateMemberWatcher

    define("UsrPrivateMemberWatcher", [], function() {
        Ext.define("Terrasoft.A", {_a: 1});
        Ext.define("Terrasoft.B", {extend: "Terrasoft.A"});
        Ext.define("Terrasoft.MC", {_b: 1});
        Ext.define("Terrasoft.C", {extend: "Terrasoft.B", mixins: {ma: "Terrasoft.MC"}});
        Ext.define("Terrasoft.MD", {_c: 1});
        /* Override the _a property. */
        Ext.define("Terrasoft.D", {extend: "Terrasoft.C", _a: 3, mixins: {mb: "Terrasoft.MD"}});
        /* Override the _c property. */
        Ext.define("Terrasoft.E", {extend: "Terrasoft.D", _c: 3});
        /* Override the _a and _b properties. */
        Ext.define("Terrasoft.F", {extend: "Terrasoft.E", _b: 3, _a: 0});
    });

After Creatio loads the `UsrPrivateMemberWatcher` module, the browser console
will display a warning about overloading the private members of the base
classes.

![](https://academy.creatio.com/sites/default/files/documentation/sdk/ru/BPMonlineWebSDK/Screenshots/PrivateMemberWatcher/scr_result.png)

## Initialize a module class instance​

You can initialize a module class instance in the following **ways** :

- synchronous initialization
- asynchronous initialization

### Initialize a module class instance synchronously​

The module is initialized synchronously if the `isAsync: true` property of the
configuration object that is passed as a parameter of the `loadModule()` method
is not specified explicitly on load. For example, the module's class methods are
loaded synchronously when the code below is executed.

    this.sandbox.loadModule([moduleName])

Creatio calls the `init()` method first, then the `render()` method.

Example that implements a synchronously initialized module

    define("ModuleExample", [], function () {
        Ext.define("Terrasoft.configuration.ModuleExample", {
            alternateClassName: "Terrasoft.ModuleExample",
            Ext: null,
            sandbox: null,
            Terrasoft: null,
            init: function () {
                /* Execute first when initializing the module. */
            },
            render: function (renderTo) {
                /* Execute after init() method when initializing the module. */
            }
         });
    });

### Initialize a module class instance asynchronously​

The module is initialized asynchronously if the `isAsync: true` property of the
configuration object that is passed as a parameter of the `loadModule()` method
is specified explicitly on load. For example, the module class methods are
loaded asynchronously when the code below is executed.

    this.sandbox.loadModule([moduleName], {
        isAsync: true
    })

Creatio calls the `init()` method first. A callback function that has the scope
of the current module is passed as a parameter of the `init()` method. When the
callback function is called, Creatio executes the `render()` method. The view is
added to DOM only after the `render()` method is executed.

Example that implements an asynchronously initialized module

    define("ModuleExample", [], function () {
        Ext.define("Terrasoft.configuration.ModuleExample", {
            alternateClassName: "Terrasoft.ModuleExample",
            Ext: null,
            sandbox: null,
            Terrasoft: null,
            /* Execute first when initializing the module. */
            init: function (callback) {
                setTimeout(callback, 2000);
            },
            render: function (renderTo) {
                /* Execute with a 2-second delay specified in the parameter in the setTimeout() function of the init() method. */
            }
        });
    });

## Module chain​

A **module chain** is a mechanism that lets you display a view of a model
instead of a view of a different model. For example, to set the field value on
the current page, display the `SelectData` page that enables users to select a
lookup value. I. e., display the module view of the lookup selection page in
place of the module container of the current page.

To **create a chain** , add the `keepAlive` property to the configuration object
of the module to load.

View an example that calls the `selectDataModule` module from the `CardModule`
current page module below. The `CardModule` module enables users to select a
lookup value.

Example that calls a module from a different module

    sandbox.loadModule("selectDataModule", {
        /* The view ID of the module to load. */
        id: "selectDataModule_id",
        /* Add the view to the current page container. */
        renderTo: "cardModuleContainer",
        /* Specify not to unload the module. */
        keepAlive: true
    });

After the code is executed, Creatio generates a chain from the current page
module and page module that lets you select a lookup value. If you add another
element to the chain, users will be able to click the **Add new record** button
to open a new page from the `selectData` current page module. You can add as
many modules to a chain as needed.

An **active module** is the last chain element that is displayed on the page. If
you use a module from the middle of a chain as the active module, Creatio
deletes all elements after the active module from the chain. To **activate a
module in the chain** , pass the module ID to the `loadModule()` function as a
parameter.

Example that calls the loadModule() function

    sandbox.loadModule("someModule", {
        id: "someModuleId"
    });

The core will delete the elements of the chain, then call the `init()` and
`render()` methods. The container that includes the previous active module is
passed to the `render()` method. The presence of a module in a chain does not
affect the module operability.

If you omit the `keepAlive` property or add it as `keepAlive: false` to a
configuration object when calling the `loadModule()` method, Creatio deletes the
module chain.

---

## See also​

[Front-end debugging](https://academy.creatio.com/documents?ver=8.0&id=15193)

- Declare a module class
- Inherit from a module class
- Overload module class members
- Initialize a module class instance
  - Initialize a module class instance synchronously
  - Initialize a module class instance asynchronously
- Module chain
- See also
