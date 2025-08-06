# Create an Angular component for Creatio | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 1900 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/development-tools/packages/file-content/create-an-angular-component

## Description

Install Angular components in Creatio using the Angular Elements functionality.
Angular Elements is an npm package that enables packing Angular components to
Custom Elements and defining new HTML elements with standard behavior. Custom
Elements is a part of the Web-Components standard.

## Key Concepts

section, operation, package, case

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/development-tools/packages/file-content/create-an-angular-component)**
(8.3).

Version: 8.1

On this page

Level: advanced

Install Angular components in Creatio using the Angular Elements functionality.
**Angular Elements** is an `npm` package that enables packing Angular components
to Custom Elements and defining new HTML elements with standard behavior. Custom
Elements is a part of the Web-Components standard.

## Create a custom Angular component​

### 1\. Set up the Angular CLI development environment​

To do this, install:

1. [Node.js® and npm package manager](https://nodejs.org/en/).

2. Angular CLI.

To install Angular CLI, run the following command at the command prompt:

     * Install Angular CLI
     * Angular CLI version 8 installation example

    npm install -g @angular/cli


    npm install -g @angular/cli@8

### 2\. Create an Angular application​

Run the `ng new` command at the command prompt and specify the application name.
For example, `angular-element-test`.

Create an Angular application

    ng new angular-element-test --style=scss

### 3\. Install the Angular Elements package​

Go to the Creatio directory added on the previous step and run the following
command at the command prompt.

Install the Angular Elements package

    ng add @angular/elements

### 4\. Create an Angular component​

To create a component, run the following command at the command prompt.

Create an Angular component

    ng g c angular-element

### 5\. Register the component as a Custom Element​

To transform the component into a custom HTML element, modify the
`app.module.ts` file:

1. Add the import of the `createCustomElement` module.

2. Specify the component name in the `entryComponents` section of the module.

3. Register the component under the HTML tag in the `ngDoBootstrap` method.

app.module.ts

         import { BrowserModule } from "@angular/platform-browser";
         import { NgModule, DoBootstrap, Injector, } from "@angular/core";
         import { createCustomElement } from "@angular/elements";
         import { AppComponent } from "./app.component";
         import { AngularElementComponent } from './angular-element/angular-element.component';

         @NgModule({
             declarations: [AppComponent, AngularElementComponent],
             imports: [BrowserModule],
             entryComponents: [AngularElementComponent]
         })
         export class AppModule implements DoBootstrap {
             constructor(private _injector: Injector) {}
             ngDoBootstrap(appRef: ApplicationRef): void {
                 const el = createCustomElement(AngularElementComponent, {
                     injector: this._injector
                 });
                 customElements.define('angular-element-component', el);
             }
         }



### 6\. Build the application​

1. Several \*.js files will be generated as part of the project build. We
   recommend deploying the generated files as a single file to streamline the
   use of the web component. To do this, create the `build.js` script in the
   root of Angular project.

build.js example

         const fs = require('fs-extra');
         const concat = require('concat');
         const componentPath = './dist/angular-element-test/angular-element-component.js';

         (async function build() {
             const files = [
                 './dist/angular-element-test/runtime.js',
                 './dist/angular-element-test/polyfills.js',
                 './dist/angular-element-test/main.js',
                 './tools/lodash-fix.js',
             ].filter((x) => fs.pathExistsSync(x));
             await fs.ensureFile(componentPath);
             await concat(files, componentPath);
         })();



If the web component uses the lodash library, merge `main.js` (as well as
`styles.js`, if necessary) with the script that resolves lodash conflicts to
ensure the library's compatibility with Creatio. To do this, create the `tools`
directory and the `lodash-fix.js` file in the Angular project root.

lodash-fix.js

         window._.noConflict();


Important

If you are not using the lodash library, do not create the `lodash-fix.js` file,
rather, delete the `'./tools/lodash-fix.js'` string from the `files` array.

To execute the `build.js` script, install the `concat` and `fs-extra` packages
in the project as dev-dependency. To do this, run the following commands at the
command prompt:

Install additional packages

         npm i concat -D
         npm i fs-extra -D


By default, you can set the settings of the `browserslist` file in the new
application. These settings create several builds for browsers that support
ES2015 and those that require ES5. For this example, build an Angular element
for modern browsers.

browserslist example

         \# This file is used by the build system to adjust CSS and JS output to support the specified browsers below.

         # For additional information regarding the format and rule options, please see:

         # https://github.com/browserslist/browserslist#queries

         # You can see what browsers were selected by your queries by running:

         # npx browserslist

         last 1 Chrome version
         last 1 Firefox version
         last 2 Edge major versions
         last 2 Safari major versions
         last 2 iOS major versions
         Firefox ESR
         not IE 11



Important

If you must deploy the web component to browsers that do not support ES2015,
either modify the file array in `build.js` or edit the `target` in
`tsconfig.json` so that it reads `target: "es5"`. After you finish the build,
review the filenames in the `dist` directory. If they do not match the names in
the `build.js` array, modify them in the file.

2. Add the element building commands to `package.json`. After the commands are
   executed, the business logic will be placed in a single
   `angular-element-component.js` file. Use this file going forward.

package.json

         ...
         "build-ng-element": "ng build --output-hashing none && node build.js",
         "build-ng-element:prod": "ng build --prod --output-hashing none && node build.js",
         ...



Important

We recommend building the application without the `--prod` parameter during the
development.

## Connect the Custom Element to Creatio​

Install the `angular-element-component.js` file you built in a Creatio package
as [file content](https://academy.creatio.com/documents?ver=8.1&id=15126).

### 1\. Place the file in the package static content​

To do this, copy the file to the `User-made package name\Files\src\js`
directory. For example, `MyPackage\Files\src\js`.

### 2\. Install the build in Creatio​

To do this, configure the build path in the bootstrap.js file of the package to
which to upload the component.

Configure the build path

    (function() {
        require.config({
            paths: {
                "angular-element-component": Terrasoft.getFileContentUrl(
                    "MyPackageName",
                    "src/js/angular-element-component.js"
                ),
            },
        });
    })();

To upload `bootstrap`, specify the path to this file. To do this, create
`descriptor.json` in `User-made package name\Files`.

descriptor.json

    {
        "bootstraps": [
            "src/js/bootstrap.js"
        ]
    }


Upload the file from the file system and compile Creatio.

### 3\. Load the component to the required schema/module​

Create a schema or module in the package to which to load the custom element.
Load the schema or module to the dependency load block of the module.

Load the component

    define("MyModuleName", ["angular-element-component"], function() {

### 4\. Create an HTML element and add it to DOM​

Add the angular-element-component custom element to Creatio page DOM

    /** * @inheritDoc Terrasoft.BaseModule#render * @override */
    render: function(renderTo) {
        this.callParent(arguments);
        const component = document.createElement("angular-element-component");
        component.setAttribute("id", this.id);
        renderTo.appendChild(component);
    }


## Work with data​

The Angular component receives data using the public properties/fields marked
with the `@Input` decorator.

Important

The properties described in camelCase without the explicit name specified in the
decorator will be transformed into HTML attributes in kebab-case.

Create the app.component.ts component property

    private _value: string;

    @Input('value')
    public set value(value: string) {
       this._value = value;
    }

Pass data to the component (CustomModule.js)

    /** * @inheritDoc Terrasoft.BaseModule#render * @override
    */
    render: function(renderTo) {
        this.callParent(arguments);
        const component = document.createElement("angular-element-component");
        component.setAttribute("value", 'Hello');
        renderTo.appendChild(component);
    }

Data retrieval is implemented via the event functionality. To do this, mark the
public field of the `EventEmiter<T>` type with the `@Output` decorator. To
initialize an event, call the `emit(T)` field method and pass the required data.

Implement the event in the component (app.component.ts)

    /**
     * Emits btn click.
     */
    @Output() btnClicked = new EventEmitter<any>();

    /**
     * Handles btn click.
     * @param eventData - Event data.
     */
    public onBtnClick(eventData: any) {
       this.btnClicked.emit(eventData);
    }

Add a button to `angular-element.component.html`.

Add a button to angular-element.component.html

    <button (click)="onBtnClick()">Click me</button>

Process the event in Creatio (CustomModule.js)

    /**
     * @inheritDoc Terrasoft.Component#initDomEvents
     * @override
     */
    initDomEvents: function() {
        this.callParent(arguments);
        const el = this.component;
        if (el) {
            el.on("itemClick", this.onItemClickHandler, this);
        }
    }

## Use Shadow DOM​

Use Shadow DOM to block certain components created using Angular and installed
in Creatio off the external environment.  
The Shadow DOM mechanism encapsulates components within DOM. This mechanism adds
a "shadow" DOM tree to the component, which cannot be addressed from the main
document via the standard options. The tree may have isolated CSS rules, etc.

To toggle on Shadow DOM, add the `encapsulation: ViewEncapsulation.ShadowDom`
property to the component decorator.

angular-element.component.ts

    import { Component, OnInit, ViewEncapsulation } from "@angular/core";

    @Component({
        selector: "angular-element-component",
        templateUrl: "./angular-element-component.html",
        styleUrls: ["./angular-element-component.scss"],
        encapsulation: ViewEncapsulation.ShadowDom,
    })
    export class AngularElementComponent implements OnInit {}

## Create Acceptance Tests for Shadow DOM​

Shadow DOM creates test problems for application components using cucumber
acceptance tests. It is not possible to address the components within Shadow DOM
from the root document via the standard selectors. Instead, use `shadow root` as
the root document and address the component elements through it.

**Shadow root** – the root component node within Shadow DOM.

**Shadow host** – the component node that contains Shadow DOM.

The `BPMonline.BaseItem` class implements the base Shadow DOM operation methods.

Important

You must pass the selector of the component that contains Shadow DOM -
`shadow host` – in most methods.

| Method | Description | clickShadowItem() | Click an element within the Shadow DOM component. | getShadowRootElement() | Returns the `shadow root` of the Angular component by the CSS selector. Use the shadow root to select other elements. | getShadowWebElement() | Returns the instance of the element within Shadow DOM by the CSS selector. Use the `waitForVisible` parameter to specify whether to wait for the instance to become visible. | getShadowWebElements() | Returns the instances of elements within Shadow DOM by the CSS selector. | mouseOverShadowItem() | Hover over the element within Shadow DOM. | waitForShadowItem() | Waits until the element within the Shadow DOM component becomes visible and returns its instance. | waitForShadowItemExist() | Waits until the element within the Shadow DOM component becomes visible. | waitForShadowItemHide() | Waits until the element within the Shadow DOM component becomes hidden. |
| ------ | ----------- | ----------------- | ------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------ | --------------------- | ----------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------ | ----------------------- | ----------------------------------------------------------------------- |

note

Review the method use examples in the `BPMonline.pages.ForecastTabUIV2` class.

---

## Resources​

[Node.js® and npm package manager](https://nodejs.org/en/)

[Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM)

- Create a custom Angular component
  - 1\. Set up the Angular CLI development environment
  - 2\. Create an Angular application
  - 3\. Install the Angular Elements package
  - 4\. Create an Angular component
  - 5\. Register the component as a Custom Element
  - 6\. Build the application
- Connect the Custom Element to Creatio
  - 1\. Place the file in the package static content
  - 2\. Install the build in Creatio
  - 3\. Load the component to the required schema/module
  - 4\. Create an HTML element and add it to DOM
- Work with data
- Use Shadow DOM
- Create Acceptance Tests for Shadow DOM
- Resources
