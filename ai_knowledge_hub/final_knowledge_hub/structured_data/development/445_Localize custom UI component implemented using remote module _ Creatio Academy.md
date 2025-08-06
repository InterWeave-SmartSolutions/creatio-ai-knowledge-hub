# Localize custom UI component implemented using remote module | Creatio Academy

**Category:** development **Difficulty:** advanced **Word Count:** 1581 **URL:**
https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/8.1/front-end-development/freedom-ui/remote-module/localize-remote-module

## Description

Localize custom UI components implemented using remote module during development
to save time spent on translating the ready-to-use custom UI component.

## Key Concepts

freedom ui, package

## Use Cases

building applications, custom development, API integration, system
administration, user management

## Content

This is documentation for Creatio **8.1**.

For up-to-date documentation, see the
**[latest version](/docs/8.x/dev/development-on-creatio-platform/front-end-development/freedom-ui/remote-module/localize-remote-module)**
(8.3).

Version: 8.1

On this page

Level: intermediate

Localize custom UI components implemented using remote module during development
to save time spent on translating the ready-to-use custom UI component.

## Localize custom validators, converters and request handlers​

Localize custom validators, converters and request handlers using Angular DI
(dependency injection). To do this:

1. **Retrieve the Creatio UI language of the current user** from the
   `userCulture` system variable. We recommend using a dedicated function. To do
   this, import the `SysValuesService` functionality from the
   `@creatio-devkit/common` library into the component. `@creatio-devkit/common`
   includes the `SysValuesService` service to localize system variables.

View the example that retrieves the Creatio UI language of the current user in
the custom UI component implemented using remote module below.

some-component.component.ts

         /* Import the required functionality from the libraries. */
         import { SysValuesService } from '@creatio-devkit/common';
         ...
         constructor() {}

         async function getUserCulture(): Promise<void> {
           /* Create an instance of the "SysValuesService" service from "@creatio-devkit/common." */
           const sysValuesService = new SysValuesService();
           /* Upload the system variable values. */
           const sysValues = await sysValuesService.loadSysValues();
           return sysValues.userCulture.displayValue;
         }


2. **Use an external library or implement the custom service** to localize
   custom UI component. We recommend using `@ngx-translate` external library to
   localize custom UI components. Learn more:
   [official vendor documentation](https://github.com/ngx-translate/core?tab=readme-ov-file)
   (GitHub).

For example, `SomeTranslationService` is an external library or custom service
to localize custom UI components.

3. If needed, **enable support for emitting type metadata for decorators** that
   works with the `reflect-metadata` module.
   1. Install the `reflect-metadata` npm package if needed. To do this, run the
      `npm i reflect-metadata` command at the command line terminal of Microsoft
      Visual Studio Code. The installation might take some time.

   2. Open the `tsconfig.json` file of the Angular project and make sure the
      `experimentalDecorators` and `emitDecoratorMetadata` properties are set to
      `true`.

tsconfig.json file

            {
              ...,
              "compilerOptions": {
                ...,
                "experimentalDecorators": true,
                "emitDecoratorMetadata": true,
                ...,
              },
            }


4. **Receive the dependencies** of the validator, converter, or request handler.
   1. Open the `app.module.ts` file.
   2. If needed, implement the `resolveDependency()` method in the
      `bootstrapCrtModule()` method. The `bootstrapCrtModule()` method registers
      the custom validator, converter, or request handler flagged using the
      `CrtModule` decorator. The `resolveDependency()` method receives the
      dependencies of the validator, converter, or request handler.
   3. Import the required functionality from the libraries into the class.
   4. Save the file.

View an example that receives the dependencies of the custom validator,
converter, or request handler using the `resolveDependency()` method below.

app.module.ts file

    /* Import the required functionality from the libraries. */
    import { DoBootstrap, Injector, ProviderToken } from '@angular/core';
    import { bootstrapCrtModule } from '@creatio-devkit/common';

    ...

    export class AppModule implements DoBootstrap {
      constructor(private _injector: Injector) {}

      ngDoBootstrap(): void {

        /* Bootstrap "CrtModule" definitions. */
        bootstrapCrtModule('some_package', AppModule, {
          /* Receive the dependencies. */
          resolveDependency: (token) => this._injector.get(<ProviderToken<unknown>>token),
        });
      }
    }

5. **Retrieve the instance of the translation service**.
   1. Open the file that implements a custom validator, converter or request
      handler. For example, open the `some-handler.handler.ts` file that
      implements a custom request handler.
   2. Receive the instant translated value using the `instant()` method.
   3. Import the required functionality from the libraries into the class.
   4. Save the file.

View an example that retrieves the instance of the `SomeTranslationService`
using Angular DI (dependency injection) below.

some-handler.handler.ts file

    /* Import the required functionality from the libraries. */
    import { BaseRequestHandler, CrtRequestHandler } from "@creatio-devkit/common";
    import { SomeRequest } from "./some-request.request";
    import { SomeTranslationService } from "./some-translation-service.service";

    /* Add the "CrtRequestHandler" decorator to the "SomeHandler" class. */
    @CrtRequestHandler({
      type: 'usr.SomeHandler',
      requestType: 'usr.SomeRequest',
    })

    export class SomeHandler extends BaseRequestHandler{
      constructor(private _someTranslationService: SomeTranslationService) {
        super();
      }
      public async handle(request: SomeRequest): Promise<void> {
        /* Receive the instant translated value. */
        const localizedMessage = this._someTranslationService.instant('SomeRequest.Message');
        alert(localizedMessage);
      }
    }

## Localize properties of custom UI component​

1. **Retrieve the Creatio UI language of the current user** from the
   `userCulture` system variable. We recommend using a dedicated function. To do
   this, import the `SysValuesService` functionality from the
   `@creatio-devkit/common` library into the component. `@creatio-devkit/common`
   includes the `SysValuesService` service to localize system variables.

View the example that retrieves the Creatio UI language of the current user in
the custom UI component implemented using remote module below.

some-component.component.ts

         /* Import the required functionality from the libraries. */
         import { SysValuesService } from '@creatio-devkit/common';
         ...
         constructor() {}

         async function getUserCulture(): Promise<void> {
           /* Create an instance of the "SysValuesService" service from "@creatio-devkit/common." */
           const sysValuesService = new SysValuesService();
           /* Upload the system variable values. */
           const sysValues = await sysValuesService.loadSysValues();
           return sysValues.userCulture.displayValue;
         }


2. **Use an external library or implement the custom service** to localize
   custom UI component. We recommend using `@ngx-translate` external library to
   localize custom UI component. Learn more:
   [official vendor documentation](https://github.com/ngx-translate/core?tab=readme-ov-file)
   (GitHub).

For example, `SomeTranslationService` is an external library or custom service
to localize custom UI components.

3. **Flag the properties to localize**.
   1. Open the `some_component.component.ts` file.
   2. Flag the component using the `CrtInterfaceDesignerItem` decorator that has
      the `toolbarConfig` property. The property manages the element layout in
      the library of the Freedom UI Designer.
   3. Import the functionality of the `CrtInterfaceDesignerItem` decorator from
      the `@creatio-devkit/common` library into the component.
   4. Mark the properties to localize using the `localize()` method.
   5. Save the file.

View the example that flags the `Caption` property of the `SomeComponent` custom
UI component implemented using remote module below.

some_component.component.ts file

    /* Import the required functionality from the libraries. */
    import { CrtInterfaceDesignerItem } from '@creatio-devkit/common';
    ...
    /* Add the "CrtInterfaceDesignerItem" decorator to the "SomeComponent" component. */
    @CrtInterfaceDesignerItem({
      /* Manage the element layout in the library of the Freedom UI Designer. */
      toolbarConfig: {
        /* The localizable name of the component. */
        caption: localize('SomeComponent.Caption'),
        ...
      }
    })
    ...

4. **Translate the localizable values** of the validator, converter or request
   handler.
   1. Open the `app.module.ts` file.
   2. Call the `localizeMetadata()` method in the `bootstrapCrtModule()` method.
      The `localizeMetadata()` method is required to translate the properties
      flagged using the `localize()` method. The key to translate the value is
      an incoming parameter of the `localizeMetadata()` method. The method
      returns the translated value.
   3. Import the required functionality from the libraries into the class.
   4. Save the file.

View an example that calls the `localizeMetadata()` method below.

app.module.ts file

    /* Import the required functionality from the libraries. */
    import { DoBootstrap, Injector } from '@angular/core';
    import { bootstrapCrtModule } from '@creatio-devkit/common';
    import { SomeTranslationService } from "./some-translation-service.service";

    ...

    export class AppModule implements DoBootstrap {
      constructor(private _injector: Injector) {}

      ngDoBootstrap(): void {

        const translationService = this._injector.get(SomeTranslationService);
        /* Bootstrap "CrtModule" definitions. */
        bootstrapCrtModule('some_package', AppModule, {
          localizeMetadata: (key: string) => translationService.instant(key),
        });
      }
    }

## Upload the translations of custom UI component from static content​

1. **Find the URL to upload the translations**. To do this, use the
   `__webpack_public_path__` global variable. Learn more:
   [official webpack documentation](https://webpack.js.org/guides/public-path/).
2. **Open the** `app.module.ts` **file**.
3. **Add app initializer** that requests the Creatio UI language of the current
   user and saves the value to the external library or custom service to
   localize custom UI component.
4. **Implement the mechanism that uploads translations**.
5. **Save the file**.

View an example that uploads the translations of custom UI component from static
content below.

app.module.ts

    /* Import the required functionality from the libraries. */
    import { BrowserModule } from "@angular/platform-browser";
    import { HttpClient } from '@angular/core';
    import { HttpClientModule } from '@creatio-devkit/common';
    import { NgModule } from "@angular/core";
    import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
    import { TranslateHttpLoader } from '@ngx-translate/http-loader';
    import { SomeTranslationService } from "./some-translation-service.service";

    declare const __webpack_public_path__: string;

    @NgModule({
      providers: [{
        provide: APP_INITIALIZER,
        useFactory: (someTranslationService) => async () => {
          const culture = await getUserCulture();
          someTranslationService.use(culture)
        },
        multi: true,
        deps: [SomeTranslationService],
      }],
      imports: [
        BrowserModule,
        HttpClientModule,
        TranslateModule.forRoot({
          defaultLanguage: 'en-US',
          loader: {
            provide: TranslateLoader,
            useFactory: (httpClient: HttpClient) => {
              return new TranslateHttpLoader(
                httpClient,
                __webpack_public_path__ + '/assets/i18n/',
                '.json'
              );
            },
            deps: [HttpClient],
          },
        }),
      ],
      ...
    })

---

## See also​

[Custom UI component implemented using remote module](https://academy.creatio.com/documents?ver=8.1&id=15017)

[Custom validator implemented using remote module](https://academy.creatio.com/documents?ver=8.1&id=15040)

[Custom converter implemented using remote module](https://academy.creatio.com/documents?ver=8.1&id=15035)

[Custom request handler implemented using remote module](https://academy.creatio.com/documents?ver=8.1&id=15037)

---

## Resources​

[`__webpack_public_path__` global variable](https://webpack.js.org/guides/public-path/)
(official webpack documentation)

- Localize custom validators, converters and request handlers
- Localize properties of custom UI component
- Upload the translations of custom UI component from static content
- See also
- Resources
