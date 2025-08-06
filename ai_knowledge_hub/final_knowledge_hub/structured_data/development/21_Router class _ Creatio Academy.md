# Router class | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 226 **URL:**
https://academy.creatio.com/docs/8.x/mobile/mobile-development/mobile-basics/architecture-mobile/references/router

## Description

Routing is used for managing visual components

## Key Concepts

case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

On this page

Level: advanced

Routing is used for managing visual components: pages, pickers, etc. The route
has 3 states:

1. `Load` – opens a current route.
2. `Unload` – closes current route on return.
3. `Reload` – restores the previous route on return.

The `Terrasoft.Router` class is used for routing and it’s main methods are
`add()`, `route()`, `back()`.

## Methods​

    add(name, config)

Adds a route.

Parameters

| name | unique name of the route. In case of re-adding, the latest route will override the previous one | config | describes names of the functions that handle route states. Handlers of the route states are set in the `handlers` property |
| ---- | ----------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------- |

Example of method use

    Terrasoft.Router.add("record", {
      handlers: {
         load: "loadPage",
         reload: "reloadPage",
         unload: "unloadLastPage"
      }
    });



    route(name, scope, args, config)

Starts the route.

Parameters

| name | name of the route | scope | context of the function of the state handlers | args | parameters of the functions of the state handlers | config | additional route parameters |
| ---- | ----------------- | ----- | --------------------------------------------- | ---- | ------------------------------------------------- | ------ | --------------------------- |

Example of method use

    var mainPageController = Terrasoft.util.getMainController();
    Terrasoft.Router.route("record", mainPageController, [{pageSchemaName: "MobileActivityGridPage"}]);



    back()

Closes current route and restores previous.

- Methods
